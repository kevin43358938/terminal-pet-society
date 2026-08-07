"""
Terminal Pet Society - Terminal UI
Beautiful curses-based interface with animated pets, particles, and stats.
"""

import curses
import math
import random
import time
from typing import Optional

from pet import Pet, PetSociety, TRAIT_ICONS, MOOD_EMOJIS
from ascii_art import get_art, get_frame_count
from persistence import save_pet, list_saved_pets
from network import scan_network, PetClient, DEFAULT_PORT, DiscoveryService
from watcher import get_recent_commands


# ─── Color constants ───
C_PET_TITLE = 5
C_GREEN = 2
C_YELLOW = 3
C_RED = 4
C_MAGENTA = 5
C_BLUE = 6
C_WHITE = 7
C_CYAN = 1

# These return actual curses attributes; initialized lazily in _init_colors
MOOD_COLOR_IDS = {
    "happy":    (C_GREEN, False),
    "excited":  (C_MAGENTA, True),
    "hungry":   (C_YELLOW, False),
    "sad":      (C_RED, False),
    "sleepy":   (C_BLUE, False),
    "coding":   (C_CYAN, False),
    "idle":     (C_WHITE, False),
    "playful":  (C_GREEN, True),
    "sick":     (C_RED, True),
}


# ─── Main UI ───

class TerminalUI:
    def __init__(self, pet: Pet, society: PetSociety):
        self.pet = pet
        self.society = society
        self.screen: Optional[curses.window] = None
        self.running = False
        self.max_y = self.max_x = 0
        self.messages: list = []
        self.input_buffer = ""
        self.input_mode = False
        self.last_tick = time.time()
        self.particles = ParticleSystem()
        # Pet wandering
        self.px = self.py = 10.0
        self.pvx = self.pvy = 0.0
        self.ptx = self.pty = 10.0
        self.art_w = self.art_h = 40
        # Cooldowns
        self._last_save = time.time()
        self._last_discovery = 0.0
        self._discovery_svc: Optional[DiscoveryService] = None

    def log(self, msg: str):
        ts = time.strftime("%H:%M:%S")
        self.messages.append(f"[{ts}] {msg}")
        if len(self.messages) > 200:
            self.messages = self.messages[-200:]

    def run(self):
        curses.wrapper(self._loop)

    def _loop(self, screen):
        self.screen = screen
        self.running = True
        curses.curs_set(0)
        screen.nodelay(True)
        self._init_colors()
        self.last_tick = time.time()
        self.px = self.ptx = 10
        self.py = self.pty = 5
        self._last_save = time.time()

        # Start auto-discovery
        self._discovery_svc = DiscoveryService(self._on_discover)
        self._discovery_svc.start()

        self.log(f"🌟 {self.pet.name} the {self.pet.species} has been born!")
        self.log(f"   {self.pet.get_personality_description()}")
        self.log("? help | f feed | p play | s sleep | v visit | q quit")

        while self.running:
            self.max_y, self.max_x = screen.getmaxyx()
            self._handle_input()
            dt = min(time.time() - self.last_tick, 0.1)
            self.last_tick = time.time()
            self.pet.tick(dt)
            self._wander(dt)
            self.particles.update(dt)
            # Autosave every ~30s
            if time.time() - self._last_save > 30:
                save_pet(self.pet)
                self._last_save = time.time()
            self._render()
            time.sleep(0.04)

    def _on_discover(self, host: str, port: int, pet_name: str):
        self.society.add_discovered(host, port, pet_name)
        self.log(f"🔍 Discovered {pet_name} at {host}:{port}")

    # ── Colors ──

    def _init_colors(self):
        curses.start_color()
        curses.use_default_colors()
        for n, (fg, bg) in enumerate([
            (curses.COLOR_CYAN, -1), (curses.COLOR_GREEN, -1),
            (curses.COLOR_YELLOW, -1), (curses.COLOR_RED, -1),
            (curses.COLOR_MAGENTA, -1), (curses.COLOR_BLUE, -1),
            (curses.COLOR_WHITE, -1),
        ], 1):
            curses.init_pair(n, fg, bg)
        # Build actual mood color map
        self._mood_colors = {}
        for mood, (cid, bold) in MOOD_COLOR_IDS.items():
            attr = curses.color_pair(cid)
            if bold:
                attr |= curses.A_BOLD
            self._mood_colors[mood] = attr

    # ── Input ──

    def _handle_input(self):
        try:
            ch = self.screen.getch()
        except Exception:
            return
        if ch == -1:
            return

        if self.input_mode:
            self._input_mode_key(ch)
            return

        key = chr(ch).lower() if 32 <= ch <= 126 else None
        if key is None:
            return

        actions = {
            'q': lambda: self._quit(),
            'f': lambda: self._do_action(self.pet.feed, "🍽️"),
            'p': lambda: self._do_action(self.pet.play, "✨"),
            's': lambda: self._do_action(self.pet.sleep, "", particles=False),
            'v': self._start_visit,
            '?': self._show_help,
            'l': self._list_pets,
            't': self._train,
            'd': self._show_discovered,
        }
        action = actions.get(key)
        if action:
            action()

    def _input_mode_key(self, ch: int):
        if ch == 10:  # Enter
            cmd = self.input_buffer.strip()
            self.input_buffer = ""
            self.input_mode = False
            if cmd:
                self._process_command(cmd)
        elif ch == 27:  # Esc
            self.input_buffer = ""
            self.input_mode = False
        elif ch in (127, 8):  # Backspace
            self.input_buffer = self.input_buffer[:-1]
        elif 32 <= ch <= 126:
            self.input_buffer += chr(ch)

    def _do_action(self, action_fn, particle_char: str, particles: bool = True):
        msg = action_fn()
        self.log(msg)
        if particles:
            self.particles.spawn(self.px, self.py, particle_char, 4)

    def _quit(self):
        self.running = False
        self.log("💾 Saving pet... Goodbye!")
        save_pet(self.pet)
        if self._discovery_svc:
            self._discovery_svc.stop()

    def _start_visit(self):
        self.input_mode = True
        self.input_buffer = ""
        # Show discovered hosts
        if self.society.discovered_hosts:
            self.log("Discovered pets nearby:")
            for addr, name in list(self.society.discovered_hosts.items())[:5]:
                self.log(f"  {name} @ {addr}")
        self.log("Enter address (host:port) or /scan:")

    def _show_help(self):
        for line in [
            "── Controls ──",
            " f feed  p play  s sleep  v visit  t learn",
            " d discovered  l saved pets  ? help  q quit",
            "── Visit ──",
            " host:port  visit pet    /scan  scan network",
        ]:
            self.log(line)

    def _list_pets(self):
        pets = list_saved_pets()
        self.log("── Saved Pets ──")
        for name, updated in pets:
            ts = time.strftime("%Y-%m-%d %H:%M", time.localtime(updated))
            self.log(f"  🐾 {name} (last: {ts})")

    def _train(self):
        cmds = get_recent_commands(15)
        self.log(f"📚 {self.pet.name} learns from {len(cmds)} recent commands...")
        for cmd in cmds:
            result = self.pet.learn_command(cmd)
            if result:
                self.log(f"  {result}")

    def _show_discovered(self):
        if not self.society.discovered_hosts:
            self.log("No pets discovered yet. Use /scan or wait for auto-discovery.")
            return
        self.log("── Discovered Pets ──")
        for addr, name in self.society.discovered_hosts.items():
            self.log(f"  🐾 {name} @ {addr}")

    # ── Commands ──

    def _process_command(self, cmd: str):
        self.log(f"> {cmd}")
        if cmd == "/scan":
            self.log("🔍 Scanning network...")
            hosts = scan_network(timeout=2.0)
            if hosts:
                for h in hosts:
                    self.log(f"  🟢 Found pet server at {h}:{DEFAULT_PORT}")
            else:
                self.log("  No pet servers found nearby.")
        elif cmd.startswith("/"):
            self.log(f"Unknown command: {cmd}")
        else:
            self.log(f"🚀 Traveling to {cmd}...")
            self._visit_pet(cmd)

    def _visit_pet(self, address: str):
        import asyncio
        host, _, port_str = address.partition(":")
        port = int(port_str) if port_str.isdigit() else DEFAULT_PORT

        try:
            loop = asyncio.new_event_loop()
            result = loop.run_until_complete(
                PetClient().visit_pet(host, port, self.pet.to_dict(), timeout=3.0))
            loop.close()

            if result and "error" not in result:
                rp = result.get("pet", {})
                self.society.add_visitor(rp)
                self.pet.visit_count += 1
                self.pet.xp += 25
                self.log(f"🎉 Met {rp.get('name','?')} the {rp.get('species','?')}! XP +25")
            else:
                err = (result or {}).get("error", "No response") if result else "No response"
                self.log(f"❌ {err}")
        except Exception as e:
            self.log(f"❌ Connection failed: {e}")

    # ── Movement ──

    def _wander(self, dt: float):
        if random.random() < 0.02:
            self.ptx = random.uniform(3, max(3, self.art_w - 3))
            self.pty = random.uniform(2, max(2, self.art_h - 2))
        dx, dy = self.ptx - self.px, self.pty - self.py
        self.pvx += dx * 0.08 * dt
        self.pvy += dy * 0.08 * dt
        self.pvx *= 0.92
        self.pvy *= 0.92
        self.px += self.pvx
        self.py += self.pvy
        self.px = max(0, min(self.px, max(0, self.art_w - 1)))
        self.py = max(0, min(self.py, max(0, self.art_h - 1)))

    # ── Rendering ──

    def _render(self):
        if not self.screen:
            return
        self.screen.erase()
        h, w = self.max_y, self.max_x
        pet_w = int(w * 0.55)
        side_w = w - pet_w - 1
        self.art_w, self.art_h = pet_w - 2, h - 5

        # Left: pet area
        self._draw_pet_area(pet_w, h)
        # Right: stats + traits
        sx = pet_w + 1
        self._draw_stats(sx, side_w, h)
        self._draw_traits(sx, side_w, h)
        # Bottom: log
        self._draw_log(w, h)
        # Particles
        self._draw_particles()
        # Input bar
        self._draw_input_bar(w, h)
        # Visitors
        if self.society.visiting_pets:
            txt = " 🐾 " + ", ".join(self.society.visiting_pets.keys())
            self._safe_add(0, max(0, w - len(txt) - 2), txt,
                           curses.color_pair(C_GREEN) | curses.A_BOLD)
        self.screen.refresh()

    def _draw_pet_area(self, pet_w: int, h: int):
        box = self.screen.subwin(h - 4, pet_w, 0, 0)
        box.box()
        self._safe_add(box, 0, 2, f"{self.pet.get_species_emoji()} {self.pet.name}  ",
                       curses.color_pair(C_PET_TITLE) | curses.A_BOLD)

        art = get_art(self.pet.species, self.pet.mood, self.pet.anim_frame)
        lines = art.strip("\n").split("\n")
        float_y = int(math.sin(time.time() * 2.0) * 1.5)
        start_y = max(1, (h - 6) // 2 - len(lines) // 2 + float_y)

        for i, line in enumerate(lines):
            x = max(1, (pet_w - len(line)) // 2)
            y = start_y + i
            if 1 <= y < h - 5:
                color = self._mood_colors.get(self.pet.mood, curses.color_pair(C_WHITE))
                self._safe_add(box, y, x, line, color)

    def _draw_stats(self, sx: int, side_w: int, h: int):
        stats_h = 11
        box = self.screen.subwin(stats_h, side_w, 0, sx)
        box.box()
        self._safe_add(box, 0, 2, " Stats ", curses.color_pair(C_MAGENTA) | curses.A_BOLD)

        lines = [
            f"  {self.pet.get_evolution_name()}",
            f"  Lv.{self.pet.level}  XP: {self.pet.xp}",
            f"  {MOOD_EMOJIS.get(self.pet.mood, '😐')} {self.pet.mood}",
            "",
        ]
        for i, line in enumerate(lines):
            self._safe_add(box, i + 1, 1, line[:side_w - 2])

        bars = [
            ("🍖 Hunger", self.pet.hunger, True,   # inverted: low=good
             [(50, C_GREEN), (80, C_YELLOW), (100, C_RED)]),
            ("😊 Happy",  self.pet.happiness, False,
             [(50, C_RED), (100, C_GREEN)]),
            ("⚡ Energy", self.pet.energy, False,
             [(50, C_YELLOW), (100, C_CYAN)]),
            ("🧠 Brain",  self.pet.intelligence, False,
             [(100, C_MAGENTA)]),
        ]
        bar_w = side_w - 16
        for i, (label, val, invert, thresholds) in enumerate(bars):
            y = i + 5
            if y >= stats_h - 1:
                break
            pct = (100 - val) / 100 if invert else val / 100
            filled = max(0, min(bar_w, int(bar_w * pct)))
            bar = "█" * filled + "░" * max(0, bar_w - filled)
            # Find color for current value
            color = C_WHITE
            for thresh, c in thresholds:
                if val < thresh:
                    color = c
                    break
            self._safe_add(box, y, 1, f" {label[:10]:10s}")
            self._safe_add(box, y, 14, bar, curses.color_pair(color) | curses.A_BOLD)

    def _draw_traits(self, sx: int, side_w: int, h: int):
        ty = 12
        trait_h = 9
        box = self.screen.subwin(trait_h, side_w, ty, sx)
        box.box()
        self._safe_add(box, 0, 2, " Traits ", curses.color_pair(C_MAGENTA) | curses.A_BOLD)

        order = ["discipline", "creativity", "social", "curiosity", "aggression", "laziness"]
        bar_w = side_w - 16
        for i, trait in enumerate(order):
            val = self.pet.traits.get(trait, 0)
            icon = TRAIT_ICONS.get(trait, "•")
            filled = int(bar_w * val / 100) if bar_w > 0 else 0
            bar = "█" * filled + "░" * max(0, bar_w - filled)
            self._safe_add(box, i + 1, 1, f" {icon} {trait[:8]:8s}{bar}")

    def _draw_log(self, w: int, h: int):
        log_y = h - 10
        log_h = h - log_y - 1
        if log_h < 3:
            return
        box = self.screen.subwin(log_h, w, log_y, 0)
        box.box()
        self._safe_add(box, 0, 2, " Log ", curses.color_pair(C_MAGENTA) | curses.A_BOLD)
        visible = log_h - 2
        recent = self.messages[-visible:]
        for i, msg in enumerate(recent):
            self._safe_add(box, i + 1, 1, msg[:w - 2])

    def _draw_particles(self):
        for p in self.particles.particles:
            x, y = int(p["x"]), int(p["y"])
            if 0 <= x < self.max_x and 0 <= y < self.max_y:
                alpha = int(p["life"] * 5) % 7 + 1
                try:
                    self.screen.addstr(y, x, p["char"], curses.color_pair(alpha))
                except curses.error:
                    pass

    def _draw_input_bar(self, w: int, h: int):
        if self.input_mode:
            prompt = f"> {self.input_buffer}_"
            self._safe_add(h - 1, 1, prompt[:w - 2], curses.A_REVERSE)
        else:
            self._safe_add(h - 1, 1,
                          " f:feed p:play s:sleep v:visit t:learn d:discovered ?:help q:quit "[:w - 2],
                          curses.color_pair(C_WHITE))

    def _safe_add(self, win, y: int, x: int, text: str, attr=0):
        """Add string to a curses window, silently handling boundary errors."""
        try:
            if isinstance(win, int):
                self.screen.addstr(win, x, text, attr)
            else:
                win.addstr(y, x, text, attr)
        except curses.error:
            pass


# ─── Particles ───

class ParticleSystem:
    def __init__(self):
        self.particles: list = []

    def spawn(self, x: float, y: float, char: str, count: int = 3):
        for _ in range(count):
            self.particles.append({
                "x": x + random.uniform(-2, 2),
                "y": y,
                "char": char,
                "vx": random.uniform(-3, 3),
                "vy": random.uniform(-5, -2),
                "life": 1.0,
                "decay": random.uniform(0.3, 0.6),
            })

    def update(self, dt: float):
        for p in self.particles[:]:
            p["x"] += p["vx"] * dt
            p["y"] += p["vy"] * dt
            p["vy"] += 1.5 * dt
            p["life"] -= p["decay"] * dt
            if p["life"] <= 0:
                self.particles.remove(p)

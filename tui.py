"""
Terminal Pet Society — Rich-based Terminal UI
Beautiful bordered cards, dynamic mood colors, animated progress bars.
"""

import asyncio
import math
import random
import time
from typing import Optional

from rich.console import Console, RenderableType
from rich.live import Live
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.progress_bar import ProgressBar
from rich.style import Style
from rich.align import Align
from rich.box import Box, ROUNDED, HEAVY, DOUBLE, SQUARE
from rich.color import Color

from pet import Pet, PetSociety, TRAIT_ICONS, MOOD_EMOJIS
from ascii_art import get_art, get_frame_count
from persistence import save_pet, list_saved_pets
from network import scan_network, PetClient, DEFAULT_PORT, DiscoveryService
from watcher import get_recent_commands


# ═══════════════════════════════════════════════════════════════
# Mood → Rich color mapping
# ═══════════════════════════════════════════════════════════════

MOOD_STYLE = {
    "happy":   Style(color="green", bold=True),
    "excited": Style(color="magenta", bold=True),
    "hungry":  Style(color="yellow"),
    "sad":     Style(color="red"),
    "sleepy":  Style(color="blue"),
    "coding":  Style(color="cyan"),
    "idle":    Style(color="white"),
    "playful": Style(color="green"),
    "sick":    Style(color="red", bold=True),
    "dead":    Style(color="grey50", dim=True),
}

MOOD_BORDER_COLOR = {
    "happy":   "green",
    "excited": "magenta",
    "hungry":  "yellow",
    "sad":     "red",
    "sleepy":  "blue",
    "coding":  "cyan",
    "idle":    "white",
    "playful": "green",
    "sick":    "red",
    "dead":    "grey50",
}

MOOD_BAR_COLOR = {
    "happy":   "green",
    "excited": "magenta",
    "hungry":  "yellow",
    "sad":     "red",
    "sleepy":  "blue",
    "coding":  "cyan",
    "idle":    "grey70",
    "playful": "green",
    "sick":    "red",
    "dead":    "grey50",
}


# ═══════════════════════════════════════════════════════════════
# Terminal UI (Rich-based)
# ═══════════════════════════════════════════════════════════════

class TerminalUI:
    def __init__(self, pet: Pet, society: PetSociety):
        self.pet = pet
        self.society = society
        self.console = Console()
        self.running = False
        self.messages: list = []
        self.input_buffer = ""
        self.input_mode = False
        self.last_tick = time.time()
        self.live: Optional[Live] = None
        self.anim_frame = 0
        self.anim_timer = 0.0
        self._last_save = time.time()
        self._discovery_svc: Optional[DiscoveryService] = None

    def log(self, msg: str):
        ts = time.strftime("%H:%M:%S")
        self.messages.append(f"[dim]{ts}[/dim] {msg}")
        if len(self.messages) > 100:
            self.messages = self.messages[-100:]

    def run(self):
        self._discovery_svc = DiscoveryService(self._on_discover)
        self._discovery_svc.start()
        self.log(f"🌟 {self.pet.name} the {self.pet.species} has been born!")
        self.log(f"   {self.pet.get_personality_description()}")
        self.log("Press keys: [bold]f[/]eed [bold]p[/]lay [bold]s[/]leep [bold]v[/]isit [bold]t[/]rain [bold]?[/]help [bold]q[/]uit")

        self.running = True
        self.last_tick = time.time()
        self._last_save = time.time()

        with Live(self._build_layout(), console=self.console, refresh_per_second=15,
                  screen=True, transient=False) as live:
            self.live = live
            while self.running:
                self._handle_input()
                dt = min(time.time() - self.last_tick, 0.1)
                self.last_tick = time.time()
                self.pet.tick(dt)
                # Animation
                self.anim_timer += dt
                if self.anim_timer > 1.5:
                    self.anim_timer = 0.0
                    fc = get_frame_count(self.pet.species, self.pet.mood)
                self.anim_frame = (self.anim_frame + 1) % max(fc, 1)
                # Autosave
                if time.time() - self._last_save > 30:
                    save_pet(self.pet)
                    self._last_save = time.time()
                live.update(self._build_layout())
                time.sleep(0.06)

    def _on_discover(self, host: str, port: int, pet_name: str):
        self.society.add_discovered(host, port, pet_name)
        self.log(f"🔍 Discovered {pet_name} at {host}:{port}")

    # ── Input ──

    def _handle_input(self):
        import sys, termios, tty, select
        if not sys.stdin.isatty():
            return
        try:
            fd = sys.stdin.fileno()
            old = termios.tcgetattr(fd)
            tty.setcbreak(fd)
            r, _, _ = select.select([sys.stdin], [], [], 0.01)
            ch = sys.stdin.read(1) if r else None
            termios.tcsetattr(fd, termios.TCSADRAIN, old)
        except Exception:
            return
        if not ch:
            return

        if self.input_mode:
            if ch == '\n' or ch == '\r':
                cmd = self.input_buffer.strip()
                self.input_buffer = ""
                self.input_mode = False
                if cmd:
                    self._process_command(cmd)
            elif ch == '\x1b':
                self.input_buffer = ""
                self.input_mode = False
            elif ch in ('\x7f', '\x08'):
                self.input_buffer = self.input_buffer[:-1]
            elif ch.isprintable():
                self.input_buffer += ch
            return

        key = ch.lower()
        actions = {
            'q': self._quit,
            'f': self._feed,
            'p': self._play,
            's': self._sleep,
            'v': self._start_visit,
            '?': self._show_help,
            'l': self._list_pets,
            't': self._train,
            'd': self._show_discovered,
        }
        action = actions.get(key)
        if action:
            action()

    def _feed(self):
        self.log(self.pet.feed())

    def _play(self):
        self.log(self.pet.play())

    def _sleep(self):
        self.log(self.pet.sleep())

    def _quit(self):
        self.running = False
        save_pet(self.pet)
        if self._discovery_svc:
            self._discovery_svc.stop()

    def _start_visit(self):
        self.input_mode = True
        self.input_buffer = ""
        if self.society.discovered_hosts:
            self.log("[bold]Discovered nearby:[/bold]")
            for addr, name in list(self.society.discovered_hosts.items())[:5]:
                self.log(f"  {name} @ {addr}")
        self.log("Enter [bold]host:port[/bold] or [bold]/scan[/bold]:")

    def _show_help(self):
        for line in [
            "[bold]── Controls ──[/bold]",
            "[bold]f[/] feed  [bold]p[/] play  [bold]s[/] sleep  [bold]v[/] visit  [bold]t[/] train",
            "[bold]d[/] discovered  [bold]l[/] saved  [bold]?[/] help  [bold]q[/] quit",
            "[bold]── Visit ──[/bold]",
            "  host:port  visit pet   [bold]/scan[/]  scan network",
        ]:
            self.log(line)

    def _list_pets(self):
        pets = list_saved_pets()
        self.log("[bold]── Saved Pets ──[/bold]")
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
            self.log("No pets discovered yet. Use [bold]/scan[/bold] or wait.")
            return
        self.log("[bold]── Discovered ──[/bold]")
        for addr, name in self.society.discovered_hosts.items():
            self.log(f"  🐾 {name} @ {addr}")

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

    # ── Layout Builder ──

    def _build_layout(self) -> Table:
        """Build the full Rich renderable layout."""
        mood = self.pet.mood
        border = MOOD_BORDER_COLOR.get(mood, "white")
        style = MOOD_STYLE.get(mood, Style())

        main = Table.grid(padding=0)
        main.add_column(ratio=1)  # Left: pet art
        main.add_column(ratio=1)  # Right: stats + traits

        # ── Left: Pet Art Panel ──
        art = get_art(self.pet.species, mood, self.anim_frame)
        art_text = Text(art.strip(), style=style, justify="center")
        title = f"{self.pet.get_species_emoji()} {self.pet.name}"
        pet_panel = Panel(
            Align.center(art_text, vertical="middle"),
            title=title,
            title_align="left",
            border_style=border,
            box=ROUNDED,
            padding=(1, 2),
        )
        main.add_row(pet_panel, self._build_right_panel(border, mood))

        # ── Bottom: Log ──
        log_lines = "\n".join(self.messages[-8:]) if self.messages else "No messages yet"
        log_panel = Panel(
            Text(log_lines, style="dim"),
            title="📋 Log",
            title_align="left",
            border_style="grey50",
            box=ROUNDED,
            height=10,
        )
        main.add_row(log_panel, None)  # span both columns would be nice but grid doesn't support colspan

        return main

    def _build_right_panel(self, border: str, mood: str) -> Panel:
        """Build the right-side panel with stats and traits."""
        bar_color = MOOD_BAR_COLOR.get(mood, "grey70")

        right_table = Table.grid(padding=(0, 1))
        right_table.add_column(style="bold")
        right_table.add_column()

        # ── Stage & Level ──
        stage_text = Text()
        stage_text.append(self.pet.get_evolution_name(), style=MOOD_STYLE.get(mood, Style()))
        stage_text.append(f"  Lv.{self.pet.level}  ")
        stage_text.append(f"XP: {self.pet.xp}", style="dim")
        right_table.add_row("", stage_text)
        right_table.add_row("", Text(f"{MOOD_EMOJIS.get(mood, '😐')} {mood}", style=MOOD_STYLE.get(mood, Style())))

        right_table.add_row("", "")

        # ── Stat bars ──
        for icon, label, val, inverted, thresholds in [
            ("🍖", "Hunger", self.pet.hunger, True,
             [(50, "green"), (80, "yellow"), (100, "red")]),
            ("😊", "Happy",  self.pet.happiness, False,
             [(50, "red"), (100, "green")]),
            ("⚡", "Energy", self.pet.energy, False,
             [(50, "yellow"), (100, "cyan")]),
            ("🧠", "Brain",  self.pet.intelligence, False,
             [(100, "magenta")]),
        ]:
            pct = (100 - val) / 100 if inverted else val / 100
            # Find bar color
            bcol = bar_color
            for thresh, c in thresholds:
                if val < thresh:
                    bcol = c
                    break
            bar = ProgressBar(total=100, completed=int(pct * 100), width=20)
            bar.style = Style(color=bcol)
            right_table.add_row(
                Text(f" {icon} {label}", style="bold"),
                bar,
            )

        right_table.add_row("", "")

        # ── Traits ──
        order = ["discipline", "creativity", "social", "curiosity", "aggression", "laziness"]
        for trait in order:
            val = self.pet.traits.get(trait, 0)
            icon = TRAIT_ICONS.get(trait, "•")
            bar = ProgressBar(total=100, completed=val, width=15)
            if val > 70:
                bar.style = Style(color="green")
            elif val > 40:
                bar.style = Style(color="yellow")
            else:
                bar.style = Style(color="grey50")
            right_table.add_row(
                Text(f" {icon} {trait[:8]:8s}"),
                bar,
            )

        # ── Visitors ──
        if self.society.visiting_pets:
            right_table.add_row("", "")
            visitors = ", ".join(self.society.visiting_pets.keys())
            right_table.add_row("", Text(f"🐾 Visitors: {visitors}", style="green"))

        # Input bar
        right_table.add_row("", "")
        if self.input_mode:
            right_table.add_row("",
                Panel(Text(f"> {self.input_buffer}_"), border_style="yellow", box=ROUNDED))
        else:
            right_table.add_row("",
                Text("f:feed p:play s:sleep v:visit ?:help q:quit", style="dim"))

        return Panel(
            right_table,
            title="📊 Stats",
            title_align="left",
            border_style=border,
            box=ROUNDED,
            padding=(1, 1),
        )

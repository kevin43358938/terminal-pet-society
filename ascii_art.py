"""
Terminal Pet Society — Expressive Line-Art Sprites
Distinct silhouettes per species. Curves, slashes, brackets, dots — not just blocks.
4-frame breathing/movement for idle + playful. 2-frame blink for others.
"""

from enum import Enum
from typing import Dict, List


class Mood(Enum):
    HAPPY = "happy"
    SAD = "sad"
    HUNGRY = "hungry"
    SLEEPY = "sleepy"
    EXCITED = "excited"
    SICK = "sick"
    DEAD = "dead"
    IDLE = "idle"
    PLAYFUL = "playful"
    CODING = "coding"
    TALKATIVE = "talkative"


class Species(Enum):
    CAT = "cat"
    DOG = "dog"
    DRAGON = "dragon"
    SLIME = "slime"
    GHOST = "ghost"
    ROBOT = "robot"
    UNICORN = "unicorn"
    PENGUIN = "penguin"


# ═══════════════════════════════════════════════════════════════
# Faces  ─  (eyes, decor, blink_eyes, blink_decor)
#   idle & playful get 4 frames from _build()
#   all others get 2 frames
# ═══════════════════════════════════════════════════════════════

F = {
    "idle":    ("◉  ◉",  "",     "⊙  ⊙",  ""),       # wide eyes → soft blink
    "happy":   ("^  ▽  ^","♡",   "⌒  ⌒",  "♡"),      # squinty smile
    "hungry":  ("◒  ◒",  "🍖",   "◓  ◓",  "🍖"),      # pleading, then hungrier
    "sleepy":  ("—  —",  "💤",   "‿  ‿",  "💤"),      # flat eyes → content
    "excited": ("★  ★",  "✨",   "☆  ☆",  "✨✨"),     # starry → super sparkle
    "sad":     ("╥  ╥",  "💧",   "╥  _  ╥","💧💧"),    # crying → sobbing
    "coding":  ("◈  ◈",  "💻",   "◉  ◉",  "💻"),      # focused → intense
    "playful": ("▼  ▼",  "🎾",   "▽  ▽",  " 🎾"),     # mischevious → wiggly
    "sick":    ("x  x",  "🤒",   "+  +",  "🤒"),      # dead eyes → dazed
    "dead":    ("✝  ✝",  "👼",   "✝  _  ✝",""),       # RIP → eternal rest
}


# ═══════════════════════════════════════════════════════════════
# Bodies  ─  {eyes} = face, {decor} = mood decor
#   Distinct silhouettes: ears, wings, tails, fins, horns.
#   Mixed character palette: / \ ( ) | . - _ ' ` ~ ^ , ╱ ╲
# ═══════════════════════════════════════════════════════════════

# Backslash without escaping headaches
_ = chr(92)
BODIES = {
    # ── CAT ──
    "cat": [
        f"       /{_}{_}_______{_}{_}/       ",
        f"      / ╲       ╱ {_}      ",
        f"     /   {{eyes}}   {_}     ",
        f"    (      ω        )    ",
        f"     {_}    ╰───╯    /     ",
        f"    __{_}___________/__    ",
        f"   ╱                 ╲   ",
        f"  (,,,)           (,,,)  ",
        f"        {{decor}}          ",
    ],

    # ── DOG ──
    "dog": [
        f"       ___     ___       ",
        f"      /   ╲___╱   {_}      ",
        f"     /             {_}     ",
        f"    (    {{eyes}}    )    ",
        f"     {_}     ⌂       /     ",
        f"    __{_}___╰───╯___/__    ",
        f"   ╱                 ╲   ",
        f"  (,,,)           (,,,)  ",
        f"        {{decor}}          ",
    ],

    # ── DRAGON ──
    "dragon": [
        f"       /{_}{_}_____________/{_}{_}       ",
        f"      / ╲             ╱ {_}      ",
        f"     /     {{eyes}}      {_}     ",
        f"    (        ⌂            )    ",
        f"     {_}      ╰───╯        /     ",
        f"   ___{_}╲               ╱/___   ",
        f" ╱    {_} ╲_____________╱ /    ╲ ",
        f"╱ ╱╲   {_}       |       /   ╱╲ ╲",
        f"╲╱    {_}___|_____|_____|___/    ╲╱",
        f"          (,,,)   (,,,)          ",
        f"             {{decor}}             ",
    ],

    # ── SLIME ──
    "slime": [
        f"        .─-──────-─.        ",
        f"      .´            `.      ",
        f"     /     {{eyes}}     {_}     ",
        f"    (         ⌂        )    ",
        f"     {_}      ╰───╯     /     ",
        f"      `.._        _..´      ",
        f"         `─-────-─´         ",
        f"          {{decor}}           ",
    ],

    # ── GHOST ──
    "ghost": [
        f"        .─-──────-─.        ",
        f"      .´            `.      ",
        f"     /     {{eyes}}     {_}     ",
        f"    (         ⌂        )    ",
        f"     {_}      ╰───╯     /     ",
        f"      ╲              ╱      ",
        f"       ~ ~ ~    ~ ~ ~       ",
        f"          {{decor}}           ",
    ],

    # ── ROBOT ──
    "robot": [
        f"         ┌───────┐          ",
        f"     ╔═══╧═══════╧═══╗      ",
        f"     ║    {{eyes}}     ║      ",
        f"     ║      [⌂]      ║      ",
        f"     ╚═══╤═══════╤═══╝      ",
        f"      ___│       │___       ",
        f"     [___]       [___]      ",
        f"          {{decor}}           ",
    ],

    # ── UNICORN ──
    "unicorn": [
        f"              ✦               ",
        f"             / {_}              ",
        f"       /{_}{_}___/ ⌂ {_}{_}___/        ",
        f"      / ╲           ╱ {_}       ",
        f"     /     {{eyes}}      {_}     ",
        f"    (                   )     ",
        f"     {_}       ω         /      ",
        f"      {_}_____╰───╯_____/       ",
        f"          (,,) (,,)           ",
        f"           {{decor}}            ",
    ],

    # ── PENGUIN ──
    "penguin": [
        f"         .─────────.         ",
        f"       .´           `.       ",
        f"      /    {{eyes}}     {_}      ",
        f"     (       ⌂         )     ",
        f"     |╲     ╰───╯     ╱|     ",
        f"     | ╲             ╱ |     ",
        f"     |__╲___________╱__|     ",
        f"         (,,)   (,,)         ",
        f"           {{decor}}           ",
    ],
}


# ═══════════════════════════════════════════════════════════════
# Build the final PET_ART dictionary from templates
# ═══════════════════════════════════════════════════════════════

MULTI_FRAME_MOODS = {"idle", "playful"}

def _build() -> dict:
    art: Dict[str, Dict[str, List[str]]] = {}

    for species, body_lines in BODIES.items():
        art[species] = {}

        for mood, face_data in F.items():
            eyes      = face_data[0]
            decor     = face_data[1]
            blink     = face_data[2] if len(face_data) > 2 else None
            bdecor    = face_data[3] if len(face_data) > 3 else None

            def make(eye_str: str, dec_str: str) -> str:
                lines = []
                for line in body_lines:
                    line = line.replace("{eyes}", eye_str)
                    line = line.replace("{decor}", dec_str or "")
                    lines.append(line)
                # Strip trailing empty lines when no decor
                if not dec_str:
                    while lines and lines[-1].strip() == "":
                        lines.pop()
                return "\n".join(lines)

            if mood in MULTI_FRAME_MOODS:
                # ── 4-frame animation: breathing / movement ──
                frames = [
                    make(eyes, decor),                           # 0: normal
                    make(blink, bdecor or ""),                   # 1: blink / subtle shift
                    make(eyes, decor if decor else " "),         # 2: normal + breath exhale
                    make(blink, bdecor if bdecor else " "),      # 3: blink + breath
                ]
            elif blink:
                frames = [make(eyes, decor), make(blink, bdecor or "")]
            else:
                frames = [make(eyes, decor)]

            art[species][mood] = frames

    return art


PET_ART: Dict[str, Dict[str, List[str]]] = _build()


# ═══════════════════════════════════════════════════════════════
# Public API
# ═══════════════════════════════════════════════════════════════

def get_art(species: str, mood: str, frame: int = 0) -> str:
    """Return the ASCII art string for a given species, mood, and frame index."""
    species_art = PET_ART.get(species, PET_ART["cat"])
    mood_frames = species_art.get(mood, species_art.get("idle", [""]))
    return mood_frames[frame % max(len(mood_frames), 1)]


def get_frame_count(species: str, mood: str) -> int:
    """Return how many animation frames exist for this species/mood combo."""
    species_art = PET_ART.get(species, PET_ART["cat"])
    return len(species_art.get(mood, species_art.get("idle", [""])))


def get_all_species() -> List[str]:
    return [s.value for s in Species]


def get_all_moods() -> List[str]:
    return [m.value for m in Mood]

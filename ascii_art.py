"""
Terminal Pet Society — Minimal Iconic ASCII Art
Classic internet style. 3-4 lines per sprite. Clean, cute, recognizable.
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


# ════════════════════════════════════
# Faces — 10 moods, 2 frames for idle
# ════════════════════════════════════

F = {
    "idle":    ("(◕‿◕)", "(-‿-)"),
    "happy":   ("(^◡^) ♡",),
    "hungry":  ("(;ω;)",),
    "sleepy":  ("(-~-) 💤",),
    "excited": ("(★▽★) ✨",),
    "sad":     ("(;_;) 💧",),
    "coding":  ("(⌨ω⌨) 💻",),
    "playful": ("(▼ᗜ▼)",),
    "sick":    ("(×_×) 🤒",),
    "dead":    ("(✝_✝) 👼",),
}

# Decor below face line (species-specific)
DECOR = {
    "hungry":  {"cat":"🍖","dog":"🦴","dragon":"🍖","slime":"🍽️","ghost":"🍽️","robot":"⚡","unicorn":"🍎","penguin":"🐟"},
    "happy":   {"dragon":"🔥","unicorn":"🌈","robot":"✅"},
    "excited": {"dragon":"🔥🔥","unicorn":"🌈🌈","robot":"⚡"},
}

# ════════════════════════════════════
# Bodies — {face} gets replaced
# ════════════════════════════════════

BODIES = {
    "cat":     "  (\\_/)\n  {face}\n  (\")(\")",
    "dog":     "   /) /)\n  {face}\n  c(\")(\")",
    "dragon":  "   __~@\n  {face}\n  /   \\",
    "slime":   "  .-~~~-.\n  {face}\n  \\___/",
    "ghost":   "  .-~~~-.\n  {face}\n  \\_._/",
    "robot":   "  [{face}]\n  [===]\n  /| |\\",
    "unicorn": "    ✦\n  {face}\n   /|\\",
    "penguin": "   {face}\n   (°°)",
}


def _build() -> dict:
    art = {}
    for sp, body in BODIES.items():
        art[sp] = {}
        for mood, faces in F.items():
            frames = []
            for fi, face in enumerate(faces):
                line = body.replace("{face}", face)
                # Add species-specific decor below last line
                if mood in DECOR and sp in DECOR[mood]:
                    line += " " + DECOR[mood][sp]
                frames.append(line)
            art[sp][mood] = frames
    return art


PET_ART: Dict[str, Dict[str, List[str]]] = _build()


def get_art(species: str, mood: str, frame: int = 0) -> str:
    species_art = PET_ART.get(species, PET_ART["cat"])
    mood_frames = species_art.get(mood, species_art.get("idle", [""]))
    return mood_frames[frame % max(len(mood_frames), 1)] if mood_frames else "  (◕_◕)"


def get_frame_count(species: str, mood: str) -> int:
    species_art = PET_ART.get(species, PET_ART["cat"])
    return len(species_art.get(mood, species_art.get("idle", [""])))


def get_all_species() -> List[str]:
    return [s.value for s in Species]


def get_all_moods() -> List[str]:
    return [m.value for m in Mood]

"""
Terminal Pet Society — Detailed Chunky Pixel Art
6-7 line sprites. Block characters. Ears, wings, tails, paws — all visible.
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
# Faces: (eyes, decor, blink_eyes)
# ════════════════════════════════════

F = {
    "idle":    ("◉ ◉", "",    "⊙ ⊙"),
    "happy":   ("★ ★", "♡",   None),
    "hungry":  ("◎ ◎", "🍖",  None),
    "sleepy":  ("~ ~", "💤",  None),
    "excited": ("☆ ☆", "✨",  None),
    "sad":     ("◒ ◒", "💧",  None),
    "coding":  ("◈ ◈", "💻",  None),
    "playful": ("▼ ▼", "🎾",  None),
    "sick":    ("× ×", "🤒",  None),
    "dead":    ("† †", "👼",  None),
}


# ════════════════════════════════════
# Bodies — {eyes} = face, {decor} = mood icon
# ════════════════════════════════════

BODIES = {
    "cat": [
        "  ▄▀▀▀▀▀▀▄  ",
        " ▐█  {eyes}  █▌ ",
        " ▐█   ⌂   █▌ ",
        "  █▄▄▄▄▄▄█  ",
        "   ▐█  █▌   ",
        "    ▀▄▄▀    ",
        "    {decor}    ",
    ],

    "dog": [
        " ▄▀▀▀▀▀▀▀▀▄ ",
        "▐█   {eyes}   █▌",
        "▐█    ⌂    █▌",
        " █▄▄▄▄▄▄▄▄█ ",
        "  ▐█▄▄▄▄█▌  ",
        "   {decor}   ",
    ],

    "dragon": [
        "    ▄▀▀▀▀▄    ",
        " ▄█▀ {eyes} ▀█▄ ",
        "▐██   ⌂   ██▌",
        " ▀█▄▄▄▄▄▄█▀ ",
        "   ▐█  █▌   ",
        "    ▀▄▄▀    ",
        "    {decor}    ",
    ],

    "slime": [
        "   .-~~~~~-.   ",
        "  (  {eyes}  )  ",
        "   \\   ⌂   /   ",
        "    \\_____/    ",
        "     {decor}     ",
    ],

    "ghost": [
        "   .-~~~~~~-.   ",
        "  (   {eyes}   )  ",
        "   \\   ⌂   /   ",
        "    \\_..._/    ",
        "     ~    ~     ",
        "     {decor}     ",
    ],

    "robot": [
        "   ╔════════╗   ",
        "   ║  {eyes}  ║   ",
        "   ║   [⌂]  ║   ",
        "   ╚══╦══╦══╝   ",
        "     ╔╝  ╚╗     ",
        "     {decor}     ",
    ],

    "unicorn": [
        "      ✦✦✦      ",
        "   ▄█▀ {eyes} ▀█▄   ",
        "  ▐██  ⌂  ██▌  ",
        "   ▀█▄▄▄▄▄█▀   ",
        "     ▐▌  ▐▌    ",
        "     {decor}     ",
    ],

    "penguin": [
        "    ▄▀▀▀▀▀▀▄    ",
        "   █  {eyes}  █   ",
        "   █   ⌂   █   ",
        "   █▄▄▄▄▄▄▄█   ",
        "    ▐█    █▌   ",
        "    {decor}    ",
    ],
}


def _build() -> dict:
    art = {}
    for sp, body_lines in BODIES.items():
        art[sp] = {}
        for mood, face_data in F.items():
            eyes, decor = face_data[0], face_data[1]
            blink = face_data[2] if len(face_data) > 2 else None

            def make(eye_str: str, dec: str) -> str:
                lines = []
                for line in body_lines:
                    line = line.replace("{eyes}", eye_str).replace("{decor}", dec or "")
                    lines.append(line)
                if not dec:
                    while lines and lines[-1].strip() == "":
                        lines.pop()
                return "\n".join(lines)

            frames = [make(eyes, decor)]
            if blink:
                frames.append(make(blink, ""))
            art[sp][mood] = frames
    return art


PET_ART: Dict[str, Dict[str, List[str]]] = _build()


def get_art(species: str, mood: str, frame: int = 0) -> str:
    species_art = PET_ART.get(species, PET_ART["cat"])
    mood_frames = species_art.get(mood, species_art.get("idle", [""]))
    return mood_frames[frame % max(len(mood_frames), 1)] if mood_frames else "  ◉ ◉  "


def get_frame_count(species: str, mood: str) -> int:
    species_art = PET_ART.get(species, PET_ART["cat"])
    return len(species_art.get(mood, species_art.get("idle", [""])))


def get_all_species() -> List[str]:
    return [s.value for s in Species]


def get_all_moods() -> List[str]:
    return [m.value for m in Mood]

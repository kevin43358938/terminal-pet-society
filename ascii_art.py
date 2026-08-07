"""
Terminal Pet Society — Clean, Recognizable ASCII Art
Classic internet ASCII style. Consistent body per species, 10 mood faces.
Uses simple characters: / \ ( ) . - _ ~ ' " | 
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


# ══════════════════════════════════════════════
# Faces — these get inserted into body templates
# Each mood has (eyes, mouth, accessory, alt_eyes) for blink anim
# ══════════════════════════════════════════════

FACES = {
    "idle":     (" ◕ ‿ ◕ ",  " - ‿ - "),
    "happy":    (" ^ ◡ ^ ",  None),    # ♡ added inline
    "hungry":   (" ; ω ; ",  None),
    "sleepy":   (" - ~ - ",  None),
    "excited":  (" ★ ▽ ★ ",  None),
    "sad":      (" ; _ ; ",  None),
    "coding":   (" ⌨ ω ⌨ ",  None),
    "playful":  (" ▼ ᗜ ▼ ",  None),
    "sick":     (" × _ × ",  None),
    "dead":     (" ✝ _ ✝ ",  None),
}

MOOD_DECOR = {
    "happy":   " ♡",
    "hungry":  "",
    "sleepy":  " 💤",
    "excited": " ✨",
    "sad":     " 💧",
    "coding":  " 💻",
    "playful": "",
    "sick":    " 🤒",
    "dead":    " 👼",
    "idle":    "",
}


# ══════════════════════════════════════════════
# Body templates — {eyes} gets replaced
# ══════════════════════════════════════════════

CAT_BODY = r"""
    /\_/\
   ({eyes})
    > ^ <
   /     \ """

DOG_BODY = r"""
     __   __
    /  \_/  \
   ( {eyes} )
    \  ___  /
     \/   \/  """

DRAGON_BODY = r"""
       ___
     _/   \_
    ( {eyes} )
     \ ___ /
      \   /   """

SLIME_BODY = r"""
     .-~~~-.
    ( {eyes} )
     \_   _/
       \ /    """

GHOST_BODY = r"""
     .-~~~-.
    ( {eyes} )
     \_._/
      ~ ~    """

ROBOT_BODY = r"""
    .-------.
    | {eyes} |
    | [===] |
    '---┬---'
       ( )   """

UNICORN_BODY = r"""
       ✦
      /|\
     ( | )
    ( {eyes} )
     \ ___ /
       \ /   """

PENGUIN_BODY = r"""
      .-.
     ( v )
    ( {eyes} )
    (( ___ ))
     '-----'  """


BODIES = {
    "cat":     CAT_BODY,
    "dog":     DOG_BODY,
    "dragon":  DRAGON_BODY,
    "slime":   SLIME_BODY,
    "ghost":   GHOST_BODY,
    "robot":   ROBOT_BODY,
    "unicorn": UNICORN_BODY,
    "penguin": PENGUIN_BODY,
}


# ══════════════════════════════════════════════
# Build PET_ART from templates
# ══════════════════════════════════════════════

def _build_art(species: str, mood: str) -> List[str]:
    body = BODIES.get(species, CAT_BODY)
    face_data = FACES.get(mood, FACES["idle"])
    main_face, alt_face = face_data[0], face_data[1] if len(face_data) > 1 else None
    decor = MOOD_DECOR.get(mood, "")

    def make_frame(face: str, add_decor: bool = True) -> str:
        art = body.replace("{eyes}", face.strip())
        if add_decor and decor:
            lines = art.strip("\n").split("\n")
            # Add decor to last line
            if lines:
                lines[-1] = lines[-1] + decor
            return "\n".join(lines)
        return art

    frames = [make_frame(main_face)]
    if alt_face:
        frames.append(make_frame(alt_face, add_decor=False))
    return frames


PET_ART: Dict[str, Dict[str, List[str]]] = {}
for sp in BODIES:
    PET_ART[sp] = {}
    for mood in FACES:
        PET_ART[sp][mood] = _build_art(sp, mood)


# ══════════════════════════════════════════════
# Public API
# ══════════════════════════════════════════════

def get_art(species: str, mood: str, frame: int = 0) -> str:
    species_art = PET_ART.get(species, PET_ART["cat"])
    mood_frames = species_art.get(mood, species_art.get("idle", [""]))
    if not mood_frames:
        return "  (◕_◕)"
    return mood_frames[frame % len(mood_frames)]


def get_frame_count(species: str, mood: str) -> int:
    species_art = PET_ART.get(species, PET_ART["cat"])
    return len(species_art.get(mood, species_art.get("idle", [""])))


def get_all_species() -> List[str]:
    return [s.value for s in Species]


def get_all_moods() -> List[str]:
    return [m.value for m in Mood]

"""
Terminal Pet Society - ASCII Art Frames
All pet species and their animation frames.
"""

from enum import Enum
from typing import Dict, List, Tuple


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


# Each species has frames for each mood
# Format: {species: {mood: [frame1, frame2, ...]}}
# Frames cycle for animation

PET_ART: Dict[str, Dict[str, List[str]]] = {
    "cat": {
        "idle": [
            """
   /\\_/\\ 
  ( o.o )
   > ^ < 
  /     \\
 """,
            """
   /\\_/\\ 
  ( -.- )
   > ^ < 
  /     \\
 """,
        ],
        "happy": [
            """
   /\\_/\\ 
  ( ^ω^ )
   > ^ < 
  /     \\
  """,
        ],
        "hungry": [
            """
   /\\_/\\ 
  ( ;ω; )
   > ^ < 
  /     \\
  🍽️ 
  """,
        ],
        "sleepy": [
            """
   /\\_/\\ 
  ( - - )
   ~ ~ ~ 
  /     \\
  💤 
  """,
        ],
        "excited": [
            """
   /\\_/\\ 
  ( ★▽★ )
   > ^ < 
  /     \\
  ✨ ✨ ✨
  """,
        ],
        "sad": [
            """
   /\\_/\\ 
  ( ;_; )
   ~ ~ ~ 
  /     \\
  """,
        ],
        "coding": [
            """
   /\\_/\\ 
  ( ⌨.⌨ )
   > ^ < 
  /     \\
  💻 
  """,
        ],
        "playful": [
            """
   /\\_/\\ 
  ( >ω< )
   > ^ < 
  /     \\
  🧶 
  """,
        ],
        "sick": [
            """
   /\\_/\\ 
  ( ×_× )
   ~ ~ ~ 
  /     \\
  🤒 
  """,
        ],
    },
    "dog": {
        "idle": [
            """
   /) /)
  (｡•ㅅ•｡)
  c(\")(\")
   """,
            """
   /) /)
  (｡•ᴗ•｡)
  c(\")(\")
   """,
        ],
        "happy": [
            """
   /) /)
  (ᵔᴥᵔ)
  c(\")(\")
  ʕっ•ᴥ•ʔっ
  """,
        ],
        "hungry": [
            """
   /) /)
  (´;ω;`)
  c(\")(\")
  🦴 
  """,
        ],
        "sleepy": [
            """
   /) /)
  (ᴗ˳ᴗ)
  c(\")(\")
  💤 
  """,
        ],
        "excited": [
            """
   /) /)
  (★ᗜ★)
  c(\")(\")
  ʕノ•ᴥ•ʔノ ︵ ┻━┻
  """,
        ],
        "sad": [
            """
   /) /)
  (´;︵;`)
  c(\")(\")
  """,
        ],
        "coding": [
            """
   /) /)
  (⌨ᗜ⌨)
  c(\")(\")
  ⌨️ ⌨️ ⌨️
  """,
        ],
        "playful": [
            """
   /) /)
  (ᵔᗜᵔ)
  c(\")(\")
  🎾 
  """,
        ],
        "sick": [
            """
   /) /)
  (´;ω;`)
  c(\")(\")
  🤒 
  """,
        ],
    },
    "dragon": {
        "idle": [
            """
      __
     /  \\_
    /\\/\\/\\
   < o  o >
    \\  ^  /
     \\___/
  """,
            """
      __
     /  \\_
    /\\/\\/\\
   < -  - >
    \\  ^  /
     \\___/
  """,
        ],
        "happy": [
            """
      __
     /  \\_
    /\\/\\/\\
   < ^  ^ >
    \\  ^  /
     \\___/
  🔥 🔥 🔥
  """,
        ],
        "hungry": [
            """
      __
     /  \\_
    /\\/\\/\\
   < ;  ; >
    \\  ^  /
     \\___/
  🍖 
  """,
        ],
        "sleepy": [
            """
      __
     /  \\_
    /\\/\\/\\
   < -  - >
    \\  ~  /
     \\___/
  💤 💤
  """,
        ],
        "excited": [
            """
      __
     /  \\_
    /\\/\\/\\
   < ★ ★ >
    \\ ^^ /
     \\___/
  🔥🔥🔥🔥🔥
  """,
        ],
        "coding": [
            """
      __
     /  \\_
    /\\/\\/\\
   < ⌨ ⌨ >
    \\ ^^ /
     \\___/
  💻 
  """,
        ],
        "playful": [
            """
      __
     /  \\_
    /\\/\\/\\
   < ▼ ▼ >
    \\ ^^ /
     \\___/
  🔥🔥
  """,
        ],
        "sick": [
            """
      __
     /  \\_
    /\\/\\/\\
   < × × >
    \\ ~  /
     \\___/
  💨 
  """,
        ],
    },
    "slime": {
        "idle": [
            """
    ___ 
   / ◕ ◕ \\
  (   ‿   )
   \\_____/
   """,
            """
    ___ 
   / ◕ ◕ \\
  (   ω   )
   \\_____/
   """,
        ],
        "happy": [
            """
    ___ 
   / ☆ ☆ \\
  (   ▽   )
   \\_____/
  ﾟ･*:.｡. .｡.:*･゜
  """,
        ],
        "hungry": [
            """
    ___ 
   / > < \\
  (   _   )
   \\_____/
  """,
        ],
        "sleepy": [
            """
    ___ 
   / - - \\
  (   ~   )
   \\_____/
  """,
        ],
        "excited": [
            """
    ___ 
   / ★ ★ \\
  (  ★▽★  )
   \\_____/
  ✨✨✨
  """,
        ],
        "coding": [
            """
    ___ 
   / ⌨ ⌨ \\
  (  ⌨ω⌨  )
   \\_____/
  """,
        ],
        "playful": [
            """
    ___ 
   / ▼ ▼ \\
  (  ▽ ▽  )
   \\_____/
  ﾟ✧
  """,
        ],
        "sick": [
            """
    ___ 
   / × × \\
  (  ~ ~  )
   \\_____/
  🤒
  """,
        ],
    },
    "ghost": {
        "idle": [
            """
    .-.
   ( o o )
   |  O  |
   |     |
   '~~~'
   """,
            """
    .-.
   ( - - )
   |  O  |
   |     |
   '~~~'
   """,
        ],
        "happy": [
            """
    .-.
   ( ^ ^ )
   |  O  |
   |     |
   '~~~'
  👻 boo!
  """,
        ],
        "hungry": [
            """
    .-.
   ( ; ; )
   |  O  |
   |     |
   '~~~'
  🍽️ 
  """,
        ],
        "sleepy": [
            """
    .-.
   ( - - )
   |  ~  |
   |     |
   '~~~'
  💤 
  """,
        ],
        "excited": [
            """
    .-.
   ( ★ ★ )
   |  O  |
   |     |
   '~~~'
  BOO!! 👻
  """,
        ],
        "coding": [
            """
    .-.
   ( ⌨ ⌨ )
   |  O  |
   |     |
   '~~~'
  👻💻
  """,
        ],
        "playful": [
            """
    .-.
   ( ▼ ▼ )
   |  O  |
   |     |
   '~~~'
  boo! 👻
  """,
        ],
        "sick": [
            """
    .-.
   ( × × )
   |  ~  |
   |     |
   '~~~'
  💨 
  """,
        ],
    },
    "robot": {
        "idle": [
            """
   [ = = ]
   | ⊙ ⊙ |
   | [=] |
   /|   |\\
   """,
            """
   [ = = ]
   | - - |
   | [=] |
   /|   |\\
   """,
        ],
        "happy": [
            """
   [ = = ]
   | ★ ★ |
   | [+] |
   /|   |\\
   ✅ SYS OK
   """,
        ],
        "hungry": [
            """
   [ = = ]
   | ; ; |
   | [!] |
   /|   |\\
   ⚡LOW⚡
   """,
        ],
        "sleepy": [
            """
   [ = = ]
   | - - |
   | [~] |
   /|   |\\
   SLEEP MODE
   """,
        ],
        "excited": [
            """
   [ = = ]
   | ☆ ☆ |
   | [!] |
   /|   |\\
   OVERCLOCKED! ⚡
   """,
        ],
        "coding": [
            """
   [ = = ]
   | ⌨ ⌨ |
   | [>] |
   /|   |\\
   01001000 01001001
   """,
        ],
        "playful": [
            """
   [ = = ]
   | ▼ ▼ |
   | [!] |
   /|   |\\
   BEEP BOOP! 🤖
   """,
        ],
        "sick": [
            """
   [ = = ]
   | × × |
   | [x] |
   /|   |\\
   ERROR 503
   """,
        ],
    },
}


def get_art(species: str, mood: str, frame: int = 0) -> str:
    """Get ASCII art for a given species, mood, and frame."""
    species_art = PET_ART.get(species, PET_ART["cat"])
    mood_frames = species_art.get(mood, species_art.get("idle", [""]))
    if not mood_frames:
        return "  (no art)"
    return mood_frames[frame % len(mood_frames)]


def get_frame_count(species: str, mood: str) -> int:
    """Get number of animation frames for a species/mood combo."""
    species_art = PET_ART.get(species, PET_ART["cat"])
    mood_frames = species_art.get(mood, species_art.get("idle", [""]))
    return len(mood_frames)


def get_all_species() -> List[str]:
    return [s.value for s in Species]


def get_all_moods() -> List[str]:
    return [m.value for m in Mood]

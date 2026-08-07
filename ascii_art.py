"""
Terminal Pet Society — Kawaii ASCII Art
8 species × 10 moods. Small, round, adorable. Big eyes required.
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


# ═══════════════════════════════════════════════════════
# 🐱 CAT — soft triangle ears, swishy tail
# ═══════════════════════════════════════════════════════
CAT = {
    "idle": [
        r"""
  /\_/\  
 ( ◕‿◕ )
  > ^ <  
""",
        r"""
  /\_/\  
 ( -‿- )
  > ^ <  
""",
    ],
    "happy": [
        r"""
  /\_/\  
 ( ^ω^ ) ♡
  > ^ <  
""",
    ],
    "hungry": [
        r"""
  /\_/\  
 ( ;ω; )  🍖
  > ^ <  
""",
    ],
    "sleepy": [
        r"""
  /\_/\  
 ( - - )  💤
  ~ ~ ~  
""",
    ],
    "excited": [
        r"""
  /\_/\  
 ( ★▽★ )  ✨
  > ^ <  
""",
    ],
    "sad": [
        r"""
  /\_/\  
 ( ;_; )  💧
  ~ ~ ~  
""",
    ],
    "coding": [
        r"""
  /\_/\    ┌─────┐
 ( ⌨ω⌨ )  │ def │
  > ^ <    └─────┘
""",
    ],
    "playful": [
        r"""
  /\_/\  
 ( ▼ω▼ )  🧶
  > ^ <  
""",
    ],
    "sick": [
        r"""
  /\_/\  
 ( ×_× )  🤒
  ~ ~ ~  
""",
    ],
    "dead": [
        r"""
  /\_/\  
 ( ✝ ✝ )  👼
  ~ ~ ~  
""",
    ],
}

# ═══════════════════════════════════════════════════════
# 🐶 DOG — floppy ears, happy tongue
# ═══════════════════════════════════════════════════════
DOG = {
    "idle": [
        r"""
   /) /)  
  (◕ ᴥ ◕) 
  c(")(")  
""",
        r"""
   /) /)  
  (- ᴥ -) 
  c(")(")  
""",
    ],
    "happy": [
        r"""
   /) /)    ♡
  (^ ᴥ ^)  ʕっ•ᴥ•ʔっ
  c(")(")  
""",
    ],
    "hungry": [
        r"""
   /) /)  
  (; ᴥ ;)  🦴
  c(")(")  
""",
    ],
    "sleepy": [
        r"""
   /) /)    💤
  (- ᴥ -)  
  c(")(")  
""",
    ],
    "excited": [
        r"""
   /) /)  
  (★ ᴥ ★)  ✨ ʕノ•ᴥ•ʔノ
  c(")(")  
""",
    ],
    "sad": [
        r"""
   /) /)  
  (; ᴥ ;)  💧
  c(")(")  
""",
    ],
    "coding": [
        r"""
   /) /)    ┌──────┐
  (⌨ ᴥ ⌨)  │ main │
  c(")(")   └──────┘
""",
    ],
    "playful": [
        r"""
   /) /)  
  (▼ ᴥ ▼)  🎾
  c(")(")  
""",
    ],
    "sick": [
        r"""
   /) /)  
  (× ᴥ ×)  🤒
  c(")(")  
""",
    ],
    "dead": [
        r"""
   /) /)  
  (✝ ᴥ ✝)  👼
  c(")(")  
""",
    ],
}

# ═══════════════════════════════════════════════════════
# 🐉 DRAGON — baby dragon, tiny wings, big eyes
# ═══════════════════════════════════════════════════════
DRAGON = {
    "idle": [
        r"""
    __
  \/  \/
 ( ◕ ‿ ◕ )
  \ __ /
""",
        r"""
    __
  \/  \/
 ( - ‿ - )
  \ __ /
""",
    ],
    "happy": [
        r"""
    __
  \/  \/  ♡
 ( ^ ω ^ )
  \ __ /  🔥
""",
    ],
    "hungry": [
        r"""
    __
  \/  \/
 ( ; ω ; )  🍖
  \ __ /
""",
    ],
    "sleepy": [
        r"""
    __
  \/  \/  💤
 ( ‿ ‿ )
  \ __ /
""",
    ],
    "excited": [
        r"""
    __
  \/  \/  ✨
 ( ★ ▽ ★ )
  \ __ /  🔥🔥
""",
    ],
    "sad": [
        r"""
    __
  \/  \/
 ( ; _ ; )  💧
  \ __ /
""",
    ],
    "coding": [
        r"""
    __    ┌────────┐
  \/  \/  │ class  │
 ( ⌨ ω ⌨ )└────────┘
  \ __ /
""",
    ],
    "playful": [
        r"""
    __
  \/  \/
 ( ▼ ω ▼ )  🔥
  \ __ /
""",
    ],
    "sick": [
        r"""
    __
  \/  \/
 ( × _ × )  🤒
  \ __ /
""",
    ],
    "dead": [
        r"""
    __
  \/  \/
 ( ✝ _ ✝ )  ☠️
  \ __ /
""",
    ],
}

# ═══════════════════════════════════════════════════════
# 🟢 SLIME — bouncy blob, super round
# ═══════════════════════════════════════════════════════
SLIME = {
    "idle": [
        r"""
   .-.
  (◕‿◕)
   `-` 
""",
        r"""
   .-.
  (-‿-)
   `-` 
""",
    ],
    "happy": [
        r"""
   .-.  ♡
  (^▽^)
   `-` 
""",
    ],
    "hungry": [
        r"""
   .-.
  (;‿;)  🍽️
   `-` 
""",
    ],
    "sleepy": [
        r"""
   .-.  💤
  (-~-)
   `-` 
""",
    ],
    "excited": [
        r"""
   .-.  ✨
  (★▽★)
   `-`  ✨
""",
    ],
    "sad": [
        r"""
   .-.
  (;_;)  💧
   `-` 
""",
    ],
    "coding": [
        r"""
   .-.  💻
  (⌨ω⌨)
   `-` 
""",
    ],
    "playful": [
        r"""
   .-.
  (▼▽▼)  ﾟ✧
   `-` 
""",
    ],
    "sick": [
        r"""
   .-.
  (×_×)  🤒
   `-` 
""",
    ],
    "dead": [
        r"""
   .-.
  (✝ ✝)  👼
   `-` 
""",
    ],
}

# ═══════════════════════════════════════════════════════
# 👻 GHOST — sheet ghost, too cute to spook
# ═══════════════════════════════════════════════════════
GHOST = {
    "idle": [
        r"""
   .-.
  (◕ ◕)
   `-` 
""",
        r"""
   .-.
  (- -)
   `-` 
""",
    ],
    "happy": [
        r"""
   .-.  ♡
  (^ ^)
   `-`  boo!
""",
    ],
    "hungry": [
        r"""
   .-.
  (; ;)  🍽️
   `-` 
""",
    ],
    "sleepy": [
        r"""
   .-.
  (‿ ‿)  💤
   `-` 
""",
    ],
    "excited": [
        r"""
   .-.  ✨
  (☆ ☆)
   `-`  👻!!
""",
    ],
    "sad": [
        r"""
   .-.
  (;_;)  💧
   `-` 
""",
    ],
    "coding": [
        r"""
   .-.  ┌────┐
  (⌨ ⌨) │git │
   `-`   └────┘
""",
    ],
    "playful": [
        r"""
   .-.
  (▼ ▼)  boo!
   `-` 
""",
    ],
    "sick": [
        r"""
   .-.
  (×_×)  🤒
   `-` 
""",
    ],
    "dead": [
        r"""
   .-.
  (✝ ✝)  👼
   `-` 
""",
    ],
}

# ═══════════════════════════════════════════════════════
# 🤖 ROBOT — tiny box bot, friendly antenna
# ═══════════════════════════════════════════════════════
ROBOT = {
    "idle": [
        r"""
  ╔═══╗
  ║◕_◕║
  ║[=]║
  ╚╦═╦╝
   ═╝ ╚═
""",
        r"""
  ╔═══╗
  ║-_─║
  ║[=]║
  ╚╦═╦╝
   ═╝ ╚═
""",
    ],
    "happy": [
        r"""
  ╔═══╗
  ║★ ★║  ✅
  ║[+]║
  ╚╦═╦╝
   ═╝ ╚═
""",
    ],
    "hungry": [
        r"""
  ╔═══╗
  ║; ;║  ⚡LOW
  ║[!]║
  ╚╦═╦╝
   ═╝ ╚═
""",
    ],
    "sleepy": [
        r"""
  ╔═══╗
  ║‿ ‿║  SLEEP
  ║[~]║
  ╚╦═╦╝  💤
   ═╝ ╚═
""",
    ],
    "excited": [
        r"""
  ╔═══╗
  ║☆ ☆║  OVER-
  ║[*]║  CLOCK!
  ╚╦═╦╝  ✨
   ═╝ ╚═
""",
    ],
    "sad": [
        r"""
  ╔═══╗
  ║;_;║  ERR
  ║[x]║  💧
  ╚╦═╦╝
   ═╝ ╚═
""",
    ],
    "coding": [
        r"""
  ╔═══╗
  ║⌨ ⌨║  0100
  ║[>]║  1001
  ╚╦═╦╝
   ═╝ ╚═
""",
    ],
    "playful": [
        r"""
  ╔═══╗
  ║▼ ▼║  BEEP
  ║[*]║  BOOP!
  ╚╦═╦╝
   ═╝ ╚═
""",
    ],
    "sick": [
        r"""
  ╔═══╗
  ║×_×║  ERR503
  ║[x]║  🤒
  ╚╦═╦╝
   ═╝ ╚═
""",
    ],
    "dead": [
        r"""
  ╔═══╗
  ║✝ ✝║  HALT
  ║[ ]║  ☠️
  ╚╦═╦╝
   ═╝ ╚═
""",
    ],
}

# ═══════════════════════════════════════════════════════
# 🦄 UNICORN — tiny, sparkly, magical
# ═══════════════════════════════════════════════════════
UNICORN = {
    "idle": [
        r"""
    ✦
   /|\ 
  (◕◕)
   \ /  
""",
        r"""
    ✦
   /|\ 
  (--)
   \ /  
""",
    ],
    "happy": [
        r"""
    ✦
   /|\  ♡
  (^^)
   \ /  🌈
""",
    ],
    "hungry": [
        r"""
    ✦
   /|\ 
  (;;)  🍎
   \ /  
""",
    ],
    "sleepy": [
        r"""
    ✦
   /|\  💤
  (‿‿)
   \ /  
""",
    ],
    "excited": [
        r"""
   ✦✦
   /|\  ✨
  (☆☆)
   \ /  🌈🌈
""",
    ],
    "sad": [
        r"""
    ✦
   /|\ 
  (;_;) 💧
   \ /  
""",
    ],
    "coding": [
        r"""
    ✦   ┌──────┐
   /|\  │magic│
  (⌨⌨) └──────┘
   \ /  
""",
    ],
    "playful": [
        r"""
    ✦
   /|\ 
  (▼▼)  🌟
   \ /  
""",
    ],
    "sick": [
        r"""
    ✦
   /|\ 
  (××)  🤒
   \ /  
""",
    ],
    "dead": [
        r"""
    ✦
   /|\ 
  (✝✝)  ☠️
   \ /  
""",
    ],
}

# ═══════════════════════════════════════════════════════
# 🐧 PENGUIN — round, waddling, baby
# ═══════════════════════════════════════════════════════
PENGUIN = {
    "idle": [
        r"""
   .-.
  (◕v◕)
  ('_') 
""",
        r"""
   .-.
  (-v-)
  ('_') 
""",
    ],
    "happy": [
        r"""
   .-.  ♡
  (^v^)
  ('▽') 
""",
    ],
    "hungry": [
        r"""
   .-.
  (;v;)  🐟
  ('_') 
""",
    ],
    "sleepy": [
        r"""
   .-.
  (-v-)  💤
  ('~') 
""",
    ],
    "excited": [
        r"""
   .-.  ✨
  (★v★)
  ('▽')  🐧!
""",
    ],
    "sad": [
        r"""
   .-.
  (;_;)  💧
  ('~') 
""",
    ],
    "coding": [
        r"""
   .-.  ┌────┐
  (⌨v⌨) │ 42 │
  ('_') └────┘
""",
    ],
    "playful": [
        r"""
   .-.
  (▼v▼)  🎿
  ('▽') 
""",
    ],
    "sick": [
        r"""
   .-.
  (×v×)  🤒
  ('~') 
""",
    ],
    "dead": [
        r"""
   .-.
  (✝v✝)  👼
  ('_') 
""",
    ],
}


# ─── Master registry ───

PET_ART: Dict[str, Dict[str, List[str]]] = {
    "cat":     CAT,
    "dog":     DOG,
    "dragon":  DRAGON,
    "slime":   SLIME,
    "ghost":   GHOST,
    "robot":   ROBOT,
    "unicorn": UNICORN,
    "penguin": PENGUIN,
}


def get_art(species: str, mood: str, frame: int = 0) -> str:
    species_art = PET_ART.get(species, PET_ART["cat"])
    mood_frames = species_art.get(mood, species_art.get("idle", [""]))
    if not mood_frames:
        return "  (◕_◕)"
    return mood_frames[frame % len(mood_frames)]


def get_frame_count(species: str, mood: str) -> int:
    species_art = PET_ART.get(species, PET_ART["cat"])
    mood_frames = species_art.get(mood, species_art.get("idle", [""]))
    return len(mood_frames)


def get_all_species() -> List[str]:
    return [s.value for s in Species]


def get_all_moods() -> List[str]:
    return [m.value for m in Mood]

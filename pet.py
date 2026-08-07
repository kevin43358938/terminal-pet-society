"""
Terminal Pet Society - Pet Core Engine
Stats, mood, personality, evolution, and command-based learning.
"""

import random
import time
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple
from enum import Enum

from ascii_art import Mood, Species


# ─── Data-driven command classifier ───
# Format: (keyword_patterns, trait, trait_delta, intelligence_delta, reaction_msg)
# Patterns use substring matching - order matters for specificity
COMMAND_RULES: List[Tuple[List[str], str, int, int, str]] = [
    (["git commit", "git push", "git add", "git rebase"], "discipline", 2, 1,
     "nods approvingly. Good dev habits! 📝"),
    (["git", "svn", "hg"], "discipline", 1, 0,
     "watches your version control... 🐱"),
    (["npm install", "npm i ", "pip install", "pip3 install",
      "cargo add", "go get", "yarn add", "pnpm add", "bun add",
      "composer require", "gem install"], "social", 2, 0,
     "makes new friends through dependencies! 📦"),
    (["python", "python3", "node ", "gcc ", "g++ ", "rustc",
      "cargo build", "cargo run", "go build", "go run",
      "make ", "cmake", "javac", "tsc", "npx "], "creativity", 1, 2,
     "learns from your code! Intelligence +2 🧠"),
    (["sudo ", "rm -rf", "rm -r", "kill ", "pkill", "chmod 777",
      "dd if=", ":(){ :|:& };:"], "aggression", 3, 0,
     "looks worried... 😰"),
    (["man ", "help ", "whatis ", "which ", "info ", "tldr", "wtf"],
     "curiosity", 2, 1, "is curious! Knowledge grows... 📚"),
    (["ssh ", "curl ", "wget ", "ping ", "nc ", "telnet ",
      "netcat", "nmap", "dig ", "host ", "traceroute"],
     "social", 2, 0, "reaches out to other pets... 🌐"),
    (["vim ", "nvim ", "emacs", "nano ", "code ", "cursor",
      "helix", "micro", "neovide"], "creativity", 1, 1,
     "watches you code intently... ⌨️"),
    (["docker", "podman", "kubectl", "helm", "terraform",
      "ansible", "vagrant"], "discipline", 1, 0,
     "sees containers! 📦"),
    (["cat ", "less ", "more ", "tail ", "head ",
      "grep ", "find ", "awk ", "sed ", "jq ", "rg "],
     "curiosity", 1, 0, None),
    (["cowsay", "fortune", "sl", "cmatrix", "lolcat",
      "figlet", "toilet", "nyancat", "asciiquarium"],
     "laziness", 2, 0, "appreciates your taste in terminal fun! 🎨"),
    (["sleep", "wait", "idle"], "laziness", 2, 0, None),
    (["npm ", "yarn ", "pnpm ", "bun ", "node ", "deno "],
     "social", 1, 0, "enjoys the JavaScript ecosystem..."),
    (["cargo ", "rustup"], "discipline", 1, 1, "🦀 Rustacean energy!"),
]


def classify_command(cmd: str) -> Optional[Tuple[str, int, int, Optional[str]]]:
    """Classify a shell command and return (trait, trait_delta, intel_delta, msg)."""
    cmd_lower = cmd.lower().strip()
    for patterns, trait, t_delta, i_delta, msg in COMMAND_RULES:
        if any(p in cmd_lower for p in patterns):
            return (trait, t_delta, i_delta, msg)
    return None


# ─── Evolution ───

class EvolutionStage(Enum):
    EGG = (0, "🥚 Egg", 0)
    BABY = (1, "👶 Baby", 50)
    CHILD = (2, "🧒 Child", 150)
    TEEN = (3, "🧑 Teen", 400)
    ADULT = (4, "🧑‍💻 Adult", 1000)
    MASTER = (5, "👑 Master", 2500)
    LEGENDARY = (6, "🌟 Legendary", 5000)

    @property
    def label(self) -> str:
        return self.value[1]

    @property
    def xp_threshold(self) -> int:
        return self.value[2]

    @classmethod
    def for_xp(cls, xp: int) -> "EvolutionStage":
        best = cls.EGG
        for stage in cls:
            if xp >= stage.xp_threshold:
                best = stage
        return best


# ─── Pet ───

TRAIT_DEFAULTS = {
    "discipline": 20, "creativity": 20, "social": 20,
    "curiosity": 20, "aggression": 10, "laziness": 10,
}

TRAIT_ICONS = {
    "discipline": "📐", "creativity": "🎨", "social": "💬",
    "curiosity": "🔍", "aggression": "💢", "laziness": "🦥",
}

PERSONALITY_DESCRIPTIONS = {
    "discipline": "a disciplined, hardworking companion",
    "creativity": "a creative, artistic soul",
    "social": "a friendly, outgoing buddy",
    "curiosity": "an endlessly curious explorer",
    "aggression": "a bit of a chaotic gremlin",
    "laziness": "a chill, relaxed friend",
}

SPECIES_EMOJIS = {
    "cat": "🐱", "dog": "🐶", "dragon": "🐉",
    "slime": "🟢", "ghost": "👻", "robot": "🤖",
    "unicorn": "🦄", "penguin": "🐧",
}

MOOD_EMOJIS = {
    "happy": "😊", "sad": "😢", "hungry": "🍽️",
    "sleepy": "💤", "excited": "🤩", "idle": "😐",
    "coding": "💻", "sick": "🤒", "playful": "😜",
}


@dataclass
class Pet:
    name: str
    species: str = "cat"

    hunger: int = 50
    happiness: int = 50
    energy: int = 70
    intelligence: int = 10

    traits: Dict[str, int] = field(default_factory=lambda: dict(TRAIT_DEFAULTS))

    level: int = 1
    xp: int = 0
    evolution_stage: str = "egg"

    mood: str = "idle"
    mood_timer: float = 0.0
    last_fed: float = 0.0
    last_played: float = 0.0
    last_slept: float = 0.0
    birth_time: float = 0.0
    commands_learned: List[str] = field(default_factory=list)
    visit_count: int = 0
    nicknames: List[str] = field(default_factory=list)

    anim_frame: int = 0
    anim_timer: float = 0.0
    status_effects: List[str] = field(default_factory=list)

    _evolution_log: List[str] = field(default_factory=list)

    def __post_init__(self):
        now = time.time()
        for attr in ("birth_time", "last_fed", "last_played", "last_slept", "mood_timer"):
            if getattr(self, attr) == 0.0:
                setattr(self, attr, now)
        for k, v in TRAIT_DEFAULTS.items():
            if k not in self.traits:
                self.traits[k] = v

    # ── Core loop ──

    def tick(self, dt: float):
        self.hunger = min(100, max(0, self.hunger + dt * 0.5))
        self.happiness = min(100, max(0, self.happiness - dt * 0.2))
        self.energy = min(100, max(0, self.energy - dt * 0.3))
        self.anim_timer += dt
        if self.anim_timer > 1.5:
            self.anim_timer = 0.0
            from ascii_art import get_frame_count
            self.anim_frame = (self.anim_frame + 1) % max(get_frame_count(self.species, self.mood), 1)
        self._update_mood()
        if self.hunger < 80 and self.happiness > 20:
            self.xp += int(dt * 0.5)
        self._check_evolution()

    def _update_mood(self):
        if self.hunger > 95:
            self.mood = "sick"
        elif self.hunger > 85:
            self.mood = "hungry"
        elif self.energy < 15:
            self.mood = "sleepy"
        elif self.happiness < 10:
            self.mood = "sad"
        elif self.happiness > 85 and self.energy > 50:
            self.mood = "excited"
        elif self.intelligence > 60 and random.random() < 0.25:
            self.mood = "coding"
        elif self.happiness > 65 and random.random() < 0.15:
            self.mood = "playful"
        else:
            self.mood = "happy" if self.happiness > 50 else "idle"

    # ── Actions ──

    def feed(self) -> str:
        self.hunger = max(0, self.hunger - 30)
        self.happiness = min(100, self.happiness + 5)
        self.xp += 5
        self.last_fed = time.time()
        if self.mood == "hungry":
            self.mood = "happy"
        return f"{self.name} eats happily! 🍽️  Hunger -30"

    def play(self) -> str:
        self.happiness = min(100, self.happiness + 20)
        self.energy = max(0, self.energy - 15)
        self.hunger = min(100, self.hunger + 10)
        self.xp += 10
        self.last_played = time.time()
        return f"{self.name} plays excitedly! 🎾 Happiness +20"

    def sleep(self) -> str:
        self.energy = min(100, self.energy + 50)
        self.hunger = min(100, self.hunger + 5)
        self.xp += 3
        self.last_slept = time.time()
        self.mood = "sleepy"
        return f"{self.name} goes to sleep... 💤 Energy +50"

    # ── Learning ──

    def learn_command(self, command: str) -> Optional[str]:
        if command in self.commands_learned:
            return None
        self.commands_learned.append(command)
        if len(self.commands_learned) > 500:
            self.commands_learned = self.commands_learned[-500:]

        result = classify_command(command)
        msg = None
        if result:
            trait, t_delta, i_delta, reaction = result
            self.traits[trait] = min(100, self.traits.get(trait, 0) + t_delta)
            self.intelligence = min(100, self.intelligence + i_delta)
            if reaction:
                msg = f"{self.name} {reaction}"
                if i_delta > 0:
                    msg += f" Intelligence +{i_delta} 🧠"

        self.xp += 2
        return msg

    # ── Evolution ──

    def _check_evolution(self):
        new_stage = EvolutionStage.for_xp(self.xp)
        if new_stage != EvolutionStage[self.evolution_stage.upper()] if self.evolution_stage.upper() in EvolutionStage.__members__ else True:
            try:
                old_idx = EvolutionStage[self.evolution_stage.upper()].value[0]
                new_idx = new_stage.value[0]
                if new_idx > old_idx:
                    self.evolution_stage = new_stage.name.lower()
                    self.level = new_idx + 1
                    self.intelligence = min(100, self.intelligence + 5)
                    self._evolution_log.append(
                        f"{time.strftime('%H:%M')} Evolved to {new_stage.label}!"
                    )
            except KeyError:
                pass

    def get_stage(self) -> EvolutionStage:
        try:
            return EvolutionStage[self.evolution_stage.upper()]
        except KeyError:
            return EvolutionStage.EGG

    def get_evolution_name(self) -> str:
        return self.get_stage().label

    # ── Queries ──

    def get_dominant_trait(self) -> str:
        return max(self.traits, key=self.traits.get)

    def get_personality_description(self) -> str:
        return PERSONALITY_DESCRIPTIONS.get(self.get_dominant_trait(),
                                            "a mysterious creature")

    def get_species_emoji(self) -> str:
        return SPECIES_EMOJIS.get(self.species, "🐾")

    def get_status_line(self) -> str:
        return (f"{self.get_species_emoji()} {self.name} | "
                f"{self.get_evolution_name()} | "
                f"{MOOD_EMOJIS.get(self.mood, '😐')} {self.mood} | "
                f"Lv.{self.level} XP:{self.xp}")

    # ── Serialization ──

    def to_dict(self) -> dict:
        return {
            "name": self.name, "species": self.species,
            "hunger": self.hunger, "happiness": self.happiness,
            "energy": self.energy, "intelligence": self.intelligence,
            "traits": self.traits, "level": self.level, "xp": self.xp,
            "evolution_stage": self.evolution_stage, "mood": self.mood,
            "last_fed": self.last_fed, "last_played": self.last_played,
            "last_slept": self.last_slept, "birth_time": self.birth_time,
            "commands_learned": self.commands_learned[-200:],
            "visit_count": self.visit_count, "nicknames": self.nicknames,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Pet":
        pet = cls(
            name=data["name"],
            species=data.get("species", "cat"),
            hunger=data.get("hunger", 50),
            happiness=data.get("happiness", 50),
            energy=data.get("energy", 70),
            intelligence=data.get("intelligence", 10),
            traits=data.get("traits", {}),
            level=data.get("level", 1),
            xp=data.get("xp", 0),
            evolution_stage=data.get("evolution_stage", "egg"),
            mood=data.get("mood", "idle"),
            last_fed=data.get("last_fed", time.time()),
            last_played=data.get("last_played", time.time()),
            last_slept=data.get("last_slept", time.time()),
            birth_time=data.get("birth_time", time.time()),
            commands_learned=data.get("commands_learned", []),
            visit_count=data.get("visit_count", 0),
            nicknames=data.get("nicknames", []),
        )
        for k, v in TRAIT_DEFAULTS.items():
            if k not in pet.traits:
                pet.traits[k] = v
        return pet


# ─── Pet Society ───

class PetSociety:
    def __init__(self):
        self.local_pet: Optional[Pet] = None
        self.visiting_pets: Dict[str, dict] = {}
        self.visitor_messages: List[str] = []
        self.discovered_hosts: Dict[str, str] = {}  # host:port -> name

    def set_local_pet(self, pet: Pet):
        self.local_pet = pet

    def add_visitor(self, pet_data: dict):
        name = pet_data.get("name", "Unknown")
        self.visiting_pets[name] = pet_data
        self.visitor_messages.append(
            f"🐾 {name} (a {pet_data.get('species','?')}) has arrived!"
        )
        if len(self.visitor_messages) > 50:
            self.visitor_messages = self.visitor_messages[-50:]

    def remove_visitor(self, name: str):
        if name in self.visiting_pets:
            del self.visiting_pets[name]
            self.visitor_messages.append(f"👋 {name} has left.")

    def get_local_pet_data(self) -> Optional[dict]:
        return self.local_pet.to_dict() if self.local_pet else None

    def add_discovered(self, host: str, port: int, pet_name: str):
        key = f"{host}:{port}"
        self.discovered_hosts[key] = pet_name

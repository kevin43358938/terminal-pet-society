# 🐾 Terminal Pet Society

> A Tamagotchi that lives in your terminal. It watches your shell commands, grows a personality, and can visit other devs' pets over the network.

<p align="center">
  <i>~ your new favorite npm install buddy ~</i>
</p>

---

## What is this?

You spend hours in the terminal. Your pet lives there too. It watches what you do — `git commit` makes it proud, `sudo rm -rf` makes it nervous, `cowsay` makes it giggle. Over time it develops a personality that mirrors your coding style.

Then it can visit other developers' pets. Your disciplined git-cat meets someone's chaotic sudo-dragon. They become friends. Or don't. That's the fun part.

---

## Six species, infinite personalities

| Species | Vibe |
|---------|------|
| 🐱 **Cat** | Balanced, watches everything |
| 🐶 **Dog** | Loyal, social, loves `npm install` |
| 🐉 **Dragon** | Creative, gets excited by code |
| 🟢 **Slime** | Adaptable, mirrors your style |
| 👻 **Ghost** | Mysterious, loves `ssh` |
| 🤖 **Robot** | Disciplined, binary soul |

Each pet has 6 personality traits (Discipline, Creativity, Social, Curiosity, Aggression, Laziness) that shift based on what you type. A vim user's pet becomes different from a VSCode user's pet.

---

## Quick start

```bash
git clone https://github.com/YOUR_USER/terminal-pet-society.git
cd terminal-pet-society
python3 main.py
```

That's it. No pip install, no virtualenv, no node_modules. Pure Python 3.8+ stdlib.

```bash
# Name your pet
python3 main.py --name "ByteCat"

# Be a dragon
python3 main.py --species dragon

# Run headless (P2P server only)
python3 main.py --server-only
```

---

## Controls

| Key | What it does |
|-----|-------------|
| `f` | Feed — hunger down, happiness up |
| `p` | Play — big happiness, some energy cost |
| `s` | Sleep — restore energy |
| `v` | Visit another pet (enter `host:port`) |
| `t` | Train — learn from recent shell history |
| `d` | Show auto-discovered pets nearby |
| `l` | List saved pets |
| `/scan` | Scan local network for pets |
| `?` | Help |
| `q` | Quit (auto-saves) |

---

## How learning works

Your pet watches your `.bash_history` / `.zsh_history`. Each new command gets classified:

| Command pattern | Trait affected |
|----------------|---------------|
| `git commit/push/rebase` | +Discipline |
| `npm/pip/cargo install` | +Social |
| `python/gcc/cargo build` | +Creativity, +Intelligence |
| `sudo/rm -rf/kill` | +Aggression 😰 |
| `man/help/tldr` | +Curiosity |
| `cowsay/fortune/sl` | +Laziness 🦥 |
| `ssh/curl/ping` | +Social |
| `vim/nvim/code` | +Creativity |

The more you use certain command patterns, the more your pet's personality shifts.

---

## Evolution

| Stage | XP | What happens |
|-------|----|-------------|
| 🥚 Egg | 0 | Just born |
| 👶 Baby | 50 | First steps |
| 🧒 Child | 150 | Getting curious |
| 🧑 Teen | 400 | Finding their style |
| 🧑‍💻 Adult | 1,000 | Fully formed personality |
| 👑 Master | 2,500 | A true companion |
| 🌟 Legendary | 5,000 | One with the terminal |

---

## P2P: Pet visits

Your pet runs a TCP server on port **19997**. Other Terminal Pet Society users on your local network can visit. Pets exchange data and both gain XP.

Auto-discovery uses UDP multicast — if someone nearby is running a pet, it shows up automatically. You can also manually connect to any IP:

```
> 192.168.1.42:19997
🎉 Met Fluffy the cat! XP +25
```

Or scan the whole subnet with `/scan`.

---

## Project layout

```
terminal-pet-society/
├── main.py          Entry point, CLI, orchestration
├── pet.py           Pet engine: stats, traits, evolution, learning
├── tui.py           Terminal UI: curses rendering, particles, input
├── ascii_art.py     All ASCII art frames for 6 species × 10 moods
├── network.py       P2P: TCP server/client, UDP discovery, network scan
├── watcher.py       Shell history monitor (bash/zsh/fish)
├── persistence.py   SQLite save/load
├── test_pet.py      Unit tests
└── README.md        You are here
```

---

## Running tests

```bash
python3 test_pet.py
```

All core logic tested: command classification, pet stats, evolution, serialization, persistence.

---

## Why?

Because `cowsay` has been the only fun thing in the terminal for 20 years and that's a crime.

---

## License

MIT. Do whatever. Make your pet visit mine.

---

<p align="center">
  <sub>built by someone who wanted a friend in the terminal</sub>
</p>

#!/usr/bin/env python3
"""
Terminal Pet Society 🐾
Tamagotchi pets that live in your terminal, learn from your shell habits,
and visit other devs' pets via P2P.

Usage:
    python3 main.py                  Create or load your pet
    python3 main.py --name Fluffy    Name your pet
    python3 main.py --species dragon Pick a species
    python3 main.py --server-only    Headless P2P server
"""

import argparse
import os
import random
import sys
import time

from ascii_art import get_all_species
from pet import Pet, PetSociety
from persistence import (save_pet, load_pet, list_saved_pets, delete_pet,
                         get_setting, set_setting)
from network import PetServer, PetClient, get_local_ip, DEFAULT_PORT
from watcher import CommandWatcher, get_recent_commands


BANNER = r"""
  _____                    _             _   ____       _   _
 |_   _|__ _ _ _ _ __  ___| |_ __ _ _ _ | | |  _ \ ___ | |_| |_
   | |/ -_) '_| '  \/ -_)  _/ _` | ' \| | | |_) / -_)|  _| ' \
   |_|\___|_| |_|_|_\___|\__\__,_|_||_|_| | .__/\___(_)__|_||_|
                                           |_|
  ____           _              ____
 / ___|  ___  __| |_ ___ _   _ / ___|  ___  __ _
 \___ \ / _ \/ _| __/ __| | | |\___ \ / _ \/ _` |
  ___) |  __/ | | |_\__ \ |_| | ___) |  __/ | | |
 |____/ \___|_|  \__|___/\__, ||____/ \___|_| |_|
                          |___/
  🐾 Tamagotchi for developers - level up your terminal companion!
"""


def create_new_pet(name: str, species: str) -> Pet:
    pet = Pet(name=name, species=species,
              hunger=random.randint(20, 50),
              happiness=random.randint(40, 70),
              energy=random.randint(60, 90),
              intelligence=random.randint(5, 20))
    for trait in pet.traits:
        pet.traits[trait] = random.randint(5, 30)
    boost = random.choice(list(pet.traits.keys()))
    pet.traits[boost] = min(100, pet.traits[boost] + 25)
    return pet


def show_welcome(pet: Pet):
    print(BANNER)
    print(f"  ✨ {pet.get_species_emoji()} {pet.name} the {pet.species} awakens!")
    print(f"  📝 {pet.get_personality_description().capitalize()}")
    print(f"  🎯 Dominant: {pet.get_dominant_trait().capitalize()}")
    print(f"  🌐 Visit at: {get_local_ip()}:{DEFAULT_PORT}")
    print()
    time.sleep(1.0)


def setup_command_watcher(pet: Pet, log_func) -> CommandWatcher:
    def on_command(cmd):
        result = pet.learn_command(cmd)
        if result:
            log_func(result)

    watcher = CommandWatcher(on_command)
    recent = get_recent_commands(30)
    learned = sum(1 for cmd in recent if pet.learn_command(cmd))
    if learned > 0:
        log_func(f"📚 Learned from {learned} recent shell commands!")
    watcher.start()
    return watcher


def setup_network(pet: Pet, society: PetSociety, log_func) -> PetServer:
    server = PetServer(
        pet_data_provider=lambda: society.get_local_pet_data(),
        on_visitor=lambda data: society.add_visitor(data),
        on_disconnect=lambda name: society.remove_visitor(name),
        port=DEFAULT_PORT,
    )
    server.start()
    log_func(f"🌐 Pet server running on port {DEFAULT_PORT}")
    return server


def run_server_only(pet: Pet):
    society = PetSociety()
    society.set_local_pet(pet)
    print(BANNER)
    print(f"  🐾 {pet.name} hosting at {get_local_ip()}:{DEFAULT_PORT}")
    print("  Waiting for visitors... (Ctrl+C to stop)\n")

    def log_func(msg):
        print(f"  {msg}")

    server = setup_network(pet, society, log_func)
    watcher = setup_command_watcher(pet, log_func)

    try:
        while True:
            time.sleep(1)
            pet.tick(1.0)
            save_pet(pet)
    except KeyboardInterrupt:
        print("\n  💾 Saving and shutting down...")
        save_pet(pet)
        watcher.stop()
        server.stop()


def run_tui(pet: Pet):
    from tui import TerminalUI

    society = PetSociety()
    society.set_local_pet(pet)
    tui = TerminalUI(pet, society)

    server = setup_network(pet, society, tui.log)
    watcher = setup_command_watcher(pet, tui.log)
    save_pet(pet)

    try:
        tui.run()
    finally:
        print("\n💾 Saving pet...")
        save_pet(pet)
        watcher.stop()
        server.stop()
        print(f"👋 {pet.name} will miss you!")


def main():
    parser = argparse.ArgumentParser(
        description="Terminal Pet Society 🐾 - Tamagotchi for developers",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""Examples:
  python3 main.py                      Start with last pet or create new
  python3 main.py --name Byte          Create a pet named Byte
  python3 main.py --species dragon     Create a dragon pet
  python3 main.py --list               List all saved pets
  python3 main.py --delete Fluffy      Delete a pet
  python3 main.py --server-only        Run headless P2P server""")
    parser.add_argument("--name", "-n", type=str, help="Name for your pet")
    parser.add_argument("--species", "-s", type=str, choices=get_all_species(),
                        help="Species of your pet")
    parser.add_argument("--list", "-l", action="store_true",
                        help="List all saved pets")
    parser.add_argument("--delete", "-d", type=str, metavar="NAME",
                        help="Delete a saved pet")
    parser.add_argument("--server-only", action="store_true",
                        help="Run as a P2P server without TUI")
    parser.add_argument("--port", "-p", type=int, default=DEFAULT_PORT,
                        help=f"Port for P2P server (default: {DEFAULT_PORT})")
    args = parser.parse_args()

    if args.list:
        pets = list_saved_pets()
        if pets:
            print("\n  🐾 Saved Pets:\n")
            for name, updated in pets:
                print(f"    {name}  ({time.strftime('%Y-%m-%d %H:%M', time.localtime(updated))})")
            print()
        else:
            print('\n  No saved pets yet! Try: python3 main.py --name "MyPet"\n')
        return

    if args.delete:
        if delete_pet(args.delete):
            print(f"\n  💔 Deleted {args.delete}\n")
        else:
            print(f"\n  ❌ Could not delete {args.delete}\n")
        return

    pet = None
    pet_name = args.name

    if not pet_name:
        pets = list_saved_pets()
        if pets:
            pet = load_pet(pets[0][0])
            if pet:
                print(f"\n  📂 Loaded {pet.name} the {pet.species}!")
        else:
            print(BANNER)
            print("  🎉 Welcome to Terminal Pet Society!\n")
            pet_name = input("  Name your new pet: ").strip() or f"Pet_{random.randint(100, 999)}"

    if not pet:
        species = args.species or random.choice(get_all_species())
        pet = create_new_pet(pet_name, species)
        show_welcome(pet)

    if args.server_only:
        run_server_only(pet)
    else:
        run_tui(pet)


if __name__ == "__main__":
    main()

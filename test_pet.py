#!/usr/bin/env python3
"""Unit tests for Terminal Pet Society."""

import json
import os
import sys
import tempfile
import time
import unittest
from unittest.mock import patch, MagicMock

sys.path.insert(0, os.path.dirname(__file__))

from pet import (Pet, PetSociety, classify_command, EvolutionStage,
                 TRAIT_DEFAULTS, COMMAND_RULES)
from persistence import save_pet, load_pet, list_saved_pets, delete_pet, _ensure_db


class TestClassifyCommand(unittest.TestCase):
    def test_git_commit_is_discipline(self):
        result = classify_command("git commit -m 'fix bug'")
        self.assertIsNotNone(result)
        self.assertEqual(result[0], "discipline")

    def test_npm_install_is_social(self):
        result = classify_command("npm install react")
        self.assertIsNotNone(result)
        self.assertEqual(result[0], "social")

    def test_sudo_is_aggression(self):
        result = classify_command("sudo rm -rf /")
        self.assertIsNotNone(result)
        self.assertEqual(result[0], "aggression")

    def test_man_is_curiosity(self):
        result = classify_command("man ls")
        self.assertIsNotNone(result)
        self.assertEqual(result[0], "curiosity")

    def test_python_is_creativity(self):
        result = classify_command("python3 main.py")
        self.assertIsNotNone(result)
        self.assertEqual(result[0], "creativity")

    def test_cowsay_is_laziness(self):
        result = classify_command("cowsay hello")
        self.assertIsNotNone(result)
        self.assertEqual(result[0], "laziness")

    def test_unknown_command_returns_none(self):
        result = classify_command("xyzzy123")
        self.assertIsNone(result)

    def test_docker_is_discipline(self):
        result = classify_command("docker compose up")
        self.assertIsNotNone(result)
        self.assertEqual(result[0], "discipline")

    def test_empty_string(self):
        result = classify_command("")
        self.assertIsNone(result)


class TestPet(unittest.TestCase):
    def setUp(self):
        self.pet = Pet(name="TestPet", species="cat")

    def test_initial_stats(self):
        self.assertEqual(self.pet.name, "TestPet")
        self.assertEqual(self.pet.species, "cat")
        self.assertEqual(self.pet.hunger, 50)
        self.assertEqual(self.pet.happiness, 50)
        self.assertEqual(self.pet.energy, 70)
        self.assertEqual(self.pet.mood, "idle")

    def test_feed_reduces_hunger(self):
        before = self.pet.hunger
        msg = self.pet.feed()
        self.assertLess(self.pet.hunger, before)
        self.assertIn("eats happily", msg)

    def test_play_increases_happiness(self):
        before = self.pet.happiness
        msg = self.pet.play()
        self.assertGreater(self.pet.happiness, before)
        self.assertIn("plays", msg)

    def test_sleep_restores_energy(self):
        before = self.pet.energy
        msg = self.pet.sleep()
        self.assertGreater(self.pet.energy, before)
        self.assertEqual(self.pet.mood, "sleepy")

    def test_learn_command_trait_change(self):
        disc_before = self.pet.traits["discipline"]
        self.pet.learn_command("git commit -m test")
        self.assertGreater(self.pet.traits["discipline"], disc_before)

    def test_learn_command_duplicate(self):
        self.pet.learn_command("git push origin main")
        xp_after_first = self.pet.xp
        self.pet.learn_command("git push origin main")
        self.assertEqual(self.pet.xp, xp_after_first)  # No XP for duplicates

    def test_learn_command_gains_xp(self):
        before = self.pet.xp
        self.pet.learn_command("echo hello world")
        self.assertGreater(self.pet.xp, before)

    def test_tick_decays_stats(self):
        self.pet.hunger = 20
        self.pet.tick(10.0)  # 10 seconds
        self.assertGreater(self.pet.hunger, 20)  # Gets hungrier

    def test_evolution(self):
        self.assertEqual(self.pet.evolution_stage, "egg")
        # Give enough XP to evolve
        self.pet.xp = 60
        self.pet.tick(0.1)
        self.assertEqual(self.pet.evolution_stage, "baby")
        self.assertEqual(self.pet.level, 2)

    def test_mood_hungry(self):
        self.pet.hunger = 96
        self.pet._update_mood()
        self.assertEqual(self.pet.mood, "sick")

    def test_mood_excited(self):
        self.pet.happiness = 90
        self.pet.energy = 80
        self.pet._update_mood()
        # Due to randomness in excited, just check it's reasonable
        self.assertIn(self.pet.mood, ["excited", "happy", "playful"])

    def test_get_dominant_trait(self):
        self.pet.traits["discipline"] = 80
        self.assertEqual(self.pet.get_dominant_trait(), "discipline")

    def test_personality_description(self):
        self.pet.traits["aggression"] = 90
        self.assertIn("gremlin", self.pet.get_personality_description())

    def test_serialization_roundtrip(self):
        self.pet.feed()
        self.pet.learn_command("git status")
        data = self.pet.to_dict()
        loaded = Pet.from_dict(data)
        self.assertEqual(loaded.name, self.pet.name)
        self.assertEqual(loaded.hunger, self.pet.hunger)
        self.assertEqual(loaded.traits["discipline"], self.pet.traits["discipline"])
        self.assertEqual(loaded.commands_learned, self.pet.commands_learned)


class TestEvolutionStage(unittest.TestCase):
    def test_for_xp(self):
        self.assertEqual(EvolutionStage.for_xp(0), EvolutionStage.EGG)
        self.assertEqual(EvolutionStage.for_xp(60), EvolutionStage.BABY)
        self.assertEqual(EvolutionStage.for_xp(200), EvolutionStage.CHILD)
        self.assertEqual(EvolutionStage.for_xp(600), EvolutionStage.TEEN)
        self.assertEqual(EvolutionStage.for_xp(2000), EvolutionStage.ADULT)
        self.assertEqual(EvolutionStage.for_xp(3000), EvolutionStage.MASTER)
        self.assertEqual(EvolutionStage.for_xp(9999), EvolutionStage.LEGENDARY)


class TestPetSociety(unittest.TestCase):
    def setUp(self):
        self.society = PetSociety()
        self.pet = Pet("Local", "dog")
        self.society.set_local_pet(self.pet)

    def test_visitor_add_remove(self):
        self.society.add_visitor({"name": "RemoteCat", "species": "cat"})
        self.assertIn("RemoteCat", self.society.visiting_pets)
        self.society.remove_visitor("RemoteCat")
        self.assertNotIn("RemoteCat", self.society.visiting_pets)

    def test_get_local_pet_data(self):
        data = self.society.get_local_pet_data()
        self.assertEqual(data["name"], "Local")

    def test_discovered_hosts(self):
        self.society.add_discovered("10.0.0.5", 19997, "NeighborPet")
        self.assertIn("10.0.0.5:19997", self.society.discovered_hosts)


class TestPersistence(unittest.TestCase):
    def setUp(self):
        # Use a temp DB
        self._old_path = __import__('persistence').DB_PATH
        self.tmp = tempfile.NamedTemporaryFile(delete=False)
        __import__('persistence').DB_PATH = self.tmp.name
        self.tmp.close()

    def tearDown(self):
        __import__('persistence').DB_PATH = self._old_path
        if os.path.exists(self.tmp.name):
            os.unlink(self.tmp.name)

    def test_save_and_load(self):
        p = Pet("SaveTest", "robot")
        p.feed()
        self.assertTrue(save_pet(p))
        loaded = load_pet("SaveTest")
        self.assertIsNotNone(loaded)
        self.assertEqual(loaded.name, "SaveTest")
        self.assertEqual(loaded.species, "robot")

    def test_list_pets(self):
        p1 = Pet("Pet1"); p2 = Pet("Pet2")
        save_pet(p1); save_pet(p2)
        pets = list_saved_pets()
        names = [n for n, _ in pets]
        self.assertIn("Pet1", names)
        self.assertIn("Pet2", names)

    def test_delete_pet(self):
        save_pet(Pet("DelMe"))
        self.assertTrue(delete_pet("DelMe"))
        self.assertIsNone(load_pet("DelMe"))

    def test_load_nonexistent(self):
        self.assertIsNone(load_pet("GhostPet"))


class TestCommandRules(unittest.TestCase):
    def test_all_rules_have_required_fields(self):
        for rule in COMMAND_RULES:
            self.assertEqual(len(rule), 5)
            patterns, trait, t_delta, i_delta, msg = rule
            self.assertIsInstance(patterns, list)
            self.assertIn(trait, TRAIT_DEFAULTS)
            self.assertIsInstance(t_delta, int)
            self.assertIsInstance(i_delta, int)
            self.assertTrue(msg is None or isinstance(msg, str))

    def test_git_takes_priority_over_generic_git(self):
        # "git commit" should match the specific rule, not the generic "git" rule
        result = classify_command("git commit -m test")
        self.assertEqual(result[1], 2)  # trait_delta should be 2, not 1


if __name__ == "__main__":
    unittest.main(verbosity=2)

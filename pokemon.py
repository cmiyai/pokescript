import numpy as np
import math
class Pokemon:
    def __init__(self, name, level, types, nature, evs, ivs, base_stats, moves, item, ability, tera_type):
        self.name = name
        self.level = level
        self.types = types  # e.g. ["Electric", "Fighting"]
        self.nature = nature
        self.evs = evs
        self.ivs = ivs
        self.base_stats = base_stats
        stat_map = {
            "hp": "HP",
            "atk": "Atk",
            "def": "Def",
            "spa": "SpA",
            "spd": "SpD",
            "spe": "Spe"
        }
        self.base_stats = {stat_map[k]: v for k, v in base_stats.items()}
        self.moves = moves  # list of Move objects
        self.item = item
        self.ability = ability
        self.tera_type=tera_type
        self.stats = self.calculate_stats()
        # Battle Stats: Dynamic
        self.current_hp = self.stats["HP"]  # Set at battle start
        self.status = None  # Optional: Burn, Paralyze, etc.
        self.boosts = {
            "Atk": 0, "Def": 0, "SpA": 0, "SpD": 0, "Spe": 0,
            "Accuracy": 0, "Evasion": 0
        }
        self.is_terastallized = False
    
    def reset_battle_state(self):
        self.current_hp = self.stats["HP"]
        self.status = None
        self.boosts = {k: 0 for k in self.boosts}
        self.is_terastallized = False

    
    @staticmethod
    def get_nature_modifiers(nature):
        """Returns a dictionary with stat multipliers based on Pokémon nature."""
        boost_map = {
            "Adamant": ("Atk", "SpA"),
            "Modest": ("SpA", "Atk"),
            "Timid": ("Spe", "Atk"),
            "Jolly": ("Spe", "SpA"),
            "Impish": ("Def", "SpA"),
            "Calm": ("SpD", "Atk"),
            "Bold": ("Def", "Atk"),
            "Careful": ("SpD", "SpA"),
            "Relaxed": ("Def", "Spe"),
            "Brave": ("Atk", "Spe"),
            "Sassy": ("SpD", "Spe"),
            "Quiet": ("SpA", "Spe"),
            "Hardy": (None, None),  # Neutral
            "Docile": (None, None),
            "Serious": (None, None),
            "Bashful": (None, None),
            "Quirky": (None, None),
        }

        stats = ['HP', 'Atk', 'Def', 'SpA', 'SpD', 'Spe']
        modifiers = {stat: 1.0 for stat in stats}

        if nature in boost_map:
            inc, dec = boost_map[nature]
            if inc: modifiers[inc] = 1.1
            if dec: modifiers[dec] = 0.9

        return modifiers

    
    def calculate_stats(self):
        ''' Caclulate pokemon stats (vectorized)'''
        keys = ['HP', 'Atk', 'Def', 'SpA', 'SpD', 'Spe']
        base = np.array([self.base_stats[k] for k in keys])
        iv = np.array([self.ivs[k] for k in keys])
        ev = np.array([self.evs[k] for k in keys])
        nature_mods = self.get_nature_modifiers(self.nature)
        nat = np.array([nature_mods[k] for k in keys])


        stats = ((2 * base + iv + ev // 4) * self.level // 100) + 5
        stats = stats * nat
        stats[0] = math.floor((2 * base[0] + iv[0] + ev[0] // 4) * self.level / 100) + self.level + 10  # HP
        
        return dict(zip(keys, stats.astype(int)))
    
    def __str__(self):
        ''' String Representation of pokemon'''
        return (
            f"{self.name} @ {self.item}\n"
            f"  Level: {self.level}    Tera Type: {self.tera_type}\n"
            f"  Ability: {self.ability}\n"
            f"  Types: {', '.join(self.types)}\n"
            f"  Nature: {self.nature}\n"
            f"  EVs: " + ", ".join([f"{k} {v}" for k, v in self.evs.items() if v > 0]) + "\n"
            f"  IVs: " + ", ".join([f"{k} {v}" for k, v in self.ivs.items() if v < 31]) + "\n"
            f"  Moves:\n    - " + "\n    - ".join(move.name for move in self.moves) + "\n"
            f"  Stats:\n    - " + "\n    - ".join(f"{k}: {v}" for k, v in self.stats.items())
        )
    
class Move:
    def __init__(self, name, type, category, power, crit_rate):
        self.name = name
        self.type = type  # e.g. "Electric"
        self.category = category  # "Physical" or "Special"
        self.power = power
        self.crit_rate = crit_rate #critical hit ratio


    def __str__(self):
        return (f"{self.name} ({self.type}) {self.category}: {self.power} ")
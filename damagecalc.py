from pokemon import Pokemon, Move
import json
import math
import random

with open("poke_data/type_chart_gen9.json", "r") as f:
    type_chart = json.load(f)

#ABILITY
#ITEM

#crit chance
def crit_chance(stage: int) -> float:
    if stage <= 0:
        return 1 / 24
    elif stage == 1:
        return 1 / 8
    elif stage == 2:
        return 1 / 2
    else:
        return 1.0 

TYPE_IMMUNITIES = {
    "Normal": ["Ghost"],
    "Fighting": ["Ghost"],
    "Ground": ["Flying"],
    "Psychic": ["Dark"],
    "Electric": ["Ground"],
    "Dragon": ["Fairy"],
    "Poison": ["Steel"],
    "Ghost": ["Normal"],
}

def is_immune(move_type, target_types):
    """Returns True if the move_type is completely immune against any of the target's types."""
    return any(t in TYPE_IMMUNITIES.get(move_type, []) for t in target_types)

def damage_range(attacker, defender, move, type_chart):
    '''computes min/max considering random factor for pokemon moves'''
    return [
        calculate_damage(attacker, defender, move, type_chart, random_factor=0.85),
        calculate_damage(attacker, defender, move, type_chart, random_factor=1.0),
        calculate_damage(attacker, defender, move, type_chart, random_factor=1.5),
    ]


def calculate_damage(attacker, defender, move, type_chart, random_factor=1):
    if is_immune(move.type, defender.types):
        print(f"{defender.name} is immune to {move.name}!")
        return 0
    level = attacker.level
    power = move.power

    atk_stat = attacker.stats['Atk'] if move.category == "Physical" else attacker.stats['SpA']
    def_stat = defender.stats['Def'] if move.category == "Physical" else defender.stats['SpD']

    #calculate stab
    type_effectiveness = 1.0
    if attacker.is_terastallized:
        if move.type == attacker.tera_type and move.type in attacker.types:
            stab = 2.0  # Same as base type and tera
        elif move.type == attacker.tera_type:
            stab = 1.5  # Tera-only STAB
        elif move.type in attacker.types:
            stab = 1.5  # Base STAB only
        else:
            stab = 1.0
    else:
        stab = 1.5 if move.type in attacker.types else 1.0
    for defender_type in defender.types:
        type_effectiveness *= type_chart.get(move.type, {}).get(defender_type, 1.0)

    modifier = stab * type_effectiveness * random_factor

    damage = math.floor((((((2 * level) / 5 + 2) * power * atk_stat / def_stat) / 50) + 2) * modifier)
    return int(damage)
from damagecalc import calculate_damage, type_chart, damage_range, crit_chance
import json
from pokemon import Pokemon, Move
from parse_team import parse_pokepaste

# Opens and reads our pokemon team
with open("team.txt") as f:
    raw = f.read()

parsed = parse_pokepaste(raw) #parse our pokemon team
#print(parsed)


def load_pokedex(path="poke_data/pokedex.json"):
    ''' Opens and reads our json file containg every pokemon'''
    with open(path, "r", encoding="utf-8") as g:
        return json.load(g)

def normalize(name):
    ''' Normalizes pokemon name so we can access the json'''
    return name.lower().replace(" ", "").replace("-", "").replace(".", "")

pokedex = load_pokedex("poke_data/pokedex.json")

def load_flattened_move_db(raw_move_data):
    """Flatten nested move dicts from parsed JSON (e.g., 'acidarmor': {'acidarmor': {...}})."""
    flattened = {}
    for key, inner in raw_move_data.items():
        if isinstance(inner, dict) and key in inner:
            flattened[key] = inner[key]
        else:
            flattened[key] = inner  # fallback in case it's already flat
    return flattened

with open("poke_data/moves.json", "r") as h:
    raw_moves = json.load(h)


move_db = load_flattened_move_db(raw_moves)

def get_moves_from_names(move_names, move_db):
    moves = []
    for name in move_names:
        key = normalize(name)
        move_info = move_db.get(key)

        if not move_info:
            print(f"⚠️ Move '{name}' → key '{key}' not found in move_db")
            continue

        moves.append(Move(
            name=move_info.get("name", name),
            type=move_info.get("type", "Normal"),
            category=move_info.get("category", "Status"),
            power=move_info.get("basePower", 0),
            crit_rate=move_info.get("critRatio", 0)
        ))
    return moves


team = []

for mon in parsed:
    Newmoves = get_moves_from_names(mon["Moves"], move_db)
    key = normalize(mon["Name"])
    data = pokedex.get(key)
    #print(key)

    if not data:
        print(f"{mon['Name']} not found in Pokedex!")
        continue

    p = Pokemon(
        name=mon["Name"],
        level=mon["Level"],
        base_stats=data["baseStats"],
        evs=mon["EVs"],
        ivs=mon["IVs"],
        nature=mon["Nature"],
        types=data["types"],
        moves=Newmoves,
        item=mon["Item"],
        ability=mon["Ability"],
        tera_type=mon["Tera Type"]
    )
    team.append(p)
print(team[1])
attacker = team[0]
defender = team[1]
attacker.is_terastallized = True
damage = damage_range(team[0], team[5], Move("Thunderbolt", "Electric", "Special", 90, 0), type_chart)
print(f"Damage dealt: between {damage[0]} to {damage[1]}")
print(attacker.moves[2])
print(attacker.tera_type)
move1 = attacker.moves[0]
min_dmg, max_dmg, crit_dmg = damage_range(attacker, defender, move1, type_chart)
percent_min = round(min_dmg / defender.stats["HP"] * 100, 1)
percent_max = round(max_dmg / defender.stats["HP"] * 100, 1)
percent_crit = round(crit_dmg / defender.stats["HP"] * 100, 1)
crit_prob = round(crit_chance(move1.crit_rate) * 100, 3)
print(f"{attacker.name}'s {move1} deals {percent_min}% – {percent_max}% of {defender.name}'s HP.\n Worst Case Critical Hit: {percent_crit}% dmg ({crit_prob}%)")
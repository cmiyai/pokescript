from parse_team import parse_pokepaste
import json
from pokemon import Pokemon

# Opens and reads our pokemon team
with open("team.txt") as f:
    raw = f.read()

parsed = parse_pokepaste(raw) #parse our pokemon team
print(parsed)


def load_pokedex(path="poke_data/pokedex.json"):
    ''' Opens and reads our json file containg every pokemon'''
    with open(path, "r", encoding="utf-8") as g:
        return json.load(g)

def normalize(name):
    ''' Normalizes pokemon name so we can access the json'''
    return name.lower().replace(" ", "").replace("-", "").replace(".", "")

pokedex = load_pokedex("poke_data/pokedex.json")
team = []

for mon in parsed:
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
        moves=mon["Moves"],
        item=mon["Item"],
        ability=mon["Ability"],
        tera_type=mon["Tera Type"]
    )
    team.append(p)

for p in team:
    print(p)
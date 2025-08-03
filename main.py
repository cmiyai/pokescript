from parse_team import parse_pokepaste
import json
import os
from pokemon import Pokemon

# Opens and reads our pokemon team
with open("team.txt") as f:
    raw = f.read()

# Opens and reads our Pokémon team from ``team.txt`` if it exists
if os.path.exists("team.txt"):
    with open("team.txt", "r", encoding="utf-8") as f:
        raw = f.read()
    parsed = parse_pokepaste(raw)  # parse our PokéPaste team
else:
    print("team.txt not found. Run fetch_pokepaste.py to download a team.")
    parsed = []

def load_pokedex(path: str = "poke_data/pokedex.json"):
    """Opens and reads our JSON file containing every Pokémon."""
    with open(path, "r", encoding="utf-8") as g:
        return json.load(g)

def normalize(name: str) -> str:
    """Normalizes a Pokémon name so we can access the JSON."""
    return name.lower().replace(" ", "").replace("-", "").replace(".", "")

pokedex = load_pokedex("poke_data/pokedex.json")
team: list[Pokemon] = []

for mon in parsed:
    key = normalize(mon["Name"])
    data = pokedex.get(key)

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
        tera_type=mon["Tera Type"],
    )
    team.append(p)

for p in team:
    print(p)
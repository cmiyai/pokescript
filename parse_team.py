import copy


def parse_pokepaste(text):
    '''takes pokepaste txt file and parses into readable data'''
    team = []
    current = {
        "Name": "",
        "Item": "",
        "Ability": "",
        "Level": 50,
        "Tera Type": "",
        "Nature": "",
        "EVs": dict.fromkeys(['HP', 'Atk', 'Def', 'SpA', 'SpD', 'Spe'], 0),
        "IVs": dict.fromkeys(['HP', 'Atk', 'Def', 'SpA', 'SpD', 'Spe'], 31),
        "Moves": []
    }

    lines = text.strip().splitlines()
    for line in lines + [""]:  # Add blank line to trigger final append
        line = line.strip()
        if not line:
            if current["Name"]:
                team.append(copy.deepcopy(current))
                current = {
                    "Name": "", "Item": "", "Ability": "", "Level": 50, "Tera Type": "", "Nature": "",
                    "EVs": dict.fromkeys(['HP', 'Atk', 'Def', 'SpA', 'SpD', 'Spe'], 0),
                    "IVs": dict.fromkeys(['HP', 'Atk', 'Def', 'SpA', 'SpD', 'Spe'], 31),
                    "Moves": []
                }
            continue
        if "@" in line:
            name, item = line.split("@", 1)
            current["Name"] = name.strip()
            current["Item"] = item.strip()
        elif line.startswith("Ability:"):
            current["Ability"] = line.split(":")[1].strip()
        elif line.startswith("Level:"):
            current["Level"] = int(line.split(":")[1])
        elif line.startswith("Tera Type:"):
            current["Tera Type"] = line.split(":")[1].strip()
        elif "Nature" in line:
            current["Nature"] = line.split()[0]
        elif line.startswith("EVs:"):
            for part in line[5:].split("/"):
                val, stat = part.strip().split()
                current["EVs"][stat] = int(val)
        elif line.startswith("IVs:"):
            for part in line[5:].split("/"):
                val, stat = part.strip().split()
                current["IVs"][stat] = int(val)
        elif line.startswith("- "):
            current["Moves"].append(line[2:].strip())

    return team
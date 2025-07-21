import requests
'''Takes pokepaste url and parses into raw txt format'''

#paste_id = input("Input pokepaste id: ")  # change to your Pokepaste ID
# will ad user input later
paste_id = "c0c48c7544b895f4"  # change to your Pokepaste ID
url = f"https://pokepast.es/{paste_id}/raw"

response = requests.get(url)
if response.ok:
    with open("team.txt", "w", encoding="utf-8") as f:
        f.write(response.text)
    print("Team saved as team.txt")
else:
    print("Could not fetch the Pokepaste.")

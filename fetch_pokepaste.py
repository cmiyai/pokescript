"""Fetch a PokéPaste team and save it to ``team.txt``.

The script prompts for a PokéPaste ID and handles network errors gracefully so
that failures do not crash the program or leave ``team.txt`` in an inconsistent
state.
"""

from __future__ import annotations
import requests
'''Takes pokepaste url and parses into raw txt format'''

def fetch_pokepaste(paste_id: str) -> bool:
    """Download the PokéPaste text and write it to ``team.txt``.

    Returns ``True`` on success and ``False`` if the request failed for any
    reason (network issues, invalid ID, etc.).
    """

    url = f"https://pokepast.es/{paste_id}/raw"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
    except requests.RequestException as exc:  # pragma: no cover - network
        print(f"Could not fetch the PokéPaste: {exc}")
        return False
    return True


if __name__ == "__main__":
    paste_id = input("Input PokéPaste ID: ").strip()
    if not paste_id:
        print("No PokéPaste ID provided.")
    else:
        fetch_pokepaste(paste_id)

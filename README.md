# 🧠 pokeCalc: Competitive Pokémon Meta + Damage Analysis Toolkit

**pokeCalc** is a modular Python project that combines competitive meta usage stats with in-battle simulation tools. It aims to help players analyze team viability, simulate stat changes, and study popular Pokémon builds using real-world data.

---

## 🚀 Current Features

### 📊 Meta Usage Integration
- Pulls real-time usage data from **Smogon** and **Pikalytics**
- Supports formats like **OU**, **VGC 2025 Regulation I**, and **Battle Stadium Singles**
- Extracts moves, teammates, items, spreads, and more

### 🧠 Stat Calculation Engine
- Models Pokémon base stats and stat stage boosts (`-6` to `+6`)
- Computes modified stats using official formulas
- Designed to simulate Showdown-style stat changes and battle behavior

### 🧰 Utility Tools
- Parses TypeScript-based data (e.g. `items.ts`, `abilities.ts`) from Showdown repos
- Converts Pokédex entries and ability data into clean JSON

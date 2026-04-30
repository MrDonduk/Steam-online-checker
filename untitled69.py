

import requests
import re

# Banner
print("=" * 50)
print("STEAM ONLINE CHECKER 🔧")
print("=" * 50)

# Search for game
search_query = input("Enter game link, ID or full name: ").strip()

# Search via Steam API
search_url = f"https://store.steampowered.com/api/storesearch/?term={search_query}&cc=us&l=english"
response = requests.get(search_url)
data = response.json()

# If nothing found
if not data['items']:
    print("\n❌ Game not found")
    print("Try one of these:")
    print("   1. Use English name (e.g., 'Counter-Strike 2')")
    print("   2. Use short name (e.g., 'CS2')")
    print("   3. Enter game ID manually")

    choice = input("\nEnter 0 to use game ID, or anything else to quit: ").strip()

    if choice == "0":
        game_id = int(input("Enter game ID from Steam (e.g., 730 for CS2): "))
        print(f"\n✅ Selected: ID {game_id}")
        print("=" * 50)
    else:
        print("❌ Exiting...")
        exit()
else:
    # Show results
    print("\n🔍 Found:")
    for i, item in enumerate(data['items'][:5], 1):
        print(f"   {i}. {item['name']} (ID: {item['id']})")

    # Choose game
    choice = input("\nEnter game number (1-5), or paste ID directly: ").strip()

    if choice.isdigit():
        choice_num = int(choice)
        if 1 <= choice_num <= 5:
            game_id = data['items'][choice_num - 1]['id']
        else:
            game_id = choice_num
    else:
        print("❌ Invalid input")
        exit()

    print(f"\n✅ Selected: ID {game_id}")
    print("=" * 50)

# Get prices from different regions
url_us = f"https://store.steampowered.com/api/appdetails?appids={game_id}&cc=us"
response_us = requests.get(url_us)
data_us = response_us.json()

url_ua = f"https://store.steampowered.com/api/appdetails?appids={game_id}&cc=ua"
response_ua = requests.get(url_ua)
data_ua = response_ua.json()

url_de = f"https://store.steampowered.com/api/appdetails?appids={game_id}&cc=de"
response_de = requests.get(url_de)
data_de = response_de.json()

url_gb = f"https://store.steampowered.com/api/appdetails?appids={game_id}&cc=gb"
response_gb = requests.get(url_gb)
data_gb = response_gb.json()

url_tr = f"https://store.steampowered.com/api/appdetails?appids={game_id}&cc=tr"
response_tr = requests.get(url_tr)
data_tr = response_tr.json()

# Game title
if data_us[str(game_id)]['success']:
    name = data_us[str(game_id)]['data']['name']
    print(f"\n🎮 {name}")
    print("=" * 50)

    # Получаем онлайн (количество игроков сейчас)
online_url = f"https://api.steampowered.com/ISteamUserStats/GetNumberOfCurrentPlayers/v1/?appid={game_id}"
online_response = requests.get(online_url)
online_data = online_response.json()

if online_data.get('response', {}).get('result') == 1:
    online_players = online_data['response']['player_count']
    print(f"👥 Online now: {online_players:,} players")
else:
    print(f"👥 Online now: N/A (no data)")
print("=" * 50)

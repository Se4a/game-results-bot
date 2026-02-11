import asyncio
import aiohttp
import os
from dotenv import load_dotenv

load_dotenv()

async def test_api(name, url, headers=None, params=None):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers, params=params) as response:
                if response.status == 200:
                    return True, f"✅ {name}: Работает"
                else:
                    return False, f"❌ {name}: Ошибка {response.status}"
    except Exception as e:
        return False, f"❌ {name}: {str(e)}"

async def main():
    print("🧪 Тестирование API подключений...")
    print("=" * 50)
    
    tests = []
    
    # Steam API
    steam_key = os.getenv('STEAM_API_KEY')
    if steam_key:
        url = f"https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v2/"
        params = {'key': steam_key, 'steamids': '76561197960435530'}
        tests.append(test_api("Steam API", url, params=params))
    
    # Riot API
    riot_key = os.getenv('RIOT_API_KEY')
    if riot_key:
        headers = {'X-Riot-Token': riot_key}
        url = "https://europe.api.riotgames.com/riot/account/v1/accounts/by-riot-id/Player/1234"
        tests.append(test_api("Riot API", url, headers=headers))
    
    # WoT API
    wot_app_id = os.getenv('WOT_APPLICATION_ID')
    if wot_app_id:
        url = "https://api.worldoftanks.eu/wot/account/list/"
        params = {'application_id': wot_app_id, 'search': 'test'}
        tests.append(test_api("WoT API", url, params=params))
    
    # PUBG API
    pubg_key = os.getenv('PUBG_API_KEY')
    if pubg_key:
        headers = {
            'Authorization': f'Bearer {pubg_key}',
            'Accept': 'application/vnd.api+json'
        }
        url = "https://api.pubg.com/shards/steam/players"
        tests.append(test_api("PUBG API", url, headers=headers))
    
    # OpenAI API
    openai_key = os.getenv('OPENAI_API_KEY')
    if openai_key:
        headers = {'Authorization': f'Bearer {openai_key}'}
        url = "https://api.openai.com/v1/models"
        tests.append(test_api("OpenAI API", url, headers=headers))
    
    results = await asyncio.gather(*tests)
    
    for success, message in results:
        print(message)
    
    print("=" * 50)
    
    success_count = sum(1 for success, _ in results if success)
    total_count = len(results)
    
    print(f"\n📊 Итог: {success_count}/{total_count} API работают")

if __name__ == "__main__":
    asyncio.run(main())
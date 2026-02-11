import re
from typing import Optional, Tuple
from datetime import datetime
import aiohttp
from bot.config import config

class ValidationError(Exception):
    """Исключение при валидации"""
    pass

async def validate_steam_id(steam_id: str) -> Tuple[bool, str]:
    """
    Валидация Steam ID
    
    Args:
        steam_id: Steam ID для проверки
    
    Returns:
        Tuple[bool, str]: (успех, сообщение об ошибке/никнейм)
    """
    # Проверка формата
    if not steam_id.isdigit():
        return False, "Steam ID должен содержать только цифры"
    
    if len(steam_id) != 17:
        return False, "Steam ID должен быть 17 цифр"
    
    # Проверка через Steam API
    try:
        url = "https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v2/"
        params = {
            'key': config.STEAM_API_KEY,
            'steamids': steam_id
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    players = data.get('response', {}).get('players', [])
                    
                    if not players:
                        return False, "Steam аккаунт не найден"
                    
                    player = players[0]
                    nickname = player.get('personaname', f'Steam_{steam_id[-8:]}')
                    
                    # Проверяем, не забанен ли аккаунт
                    if player.get('communitybanned') or player.get('vacbanned'):
                        return False, "Steam аккаунт имеет ограничения"
                    
                    return True, nickname
                
                return False, f"Ошибка Steam API: {response.status}"
    
    except Exception as e:
        return False, f"Ошибка при проверке Steam ID: {str(e)}"

async def validate_riot_id(riot_id: str, game: str = 'valorant') -> Tuple[bool, str]:
    """
    Валидация Riot ID (Valorant/LoL)
    
    Args:
        riot_id: Riot ID в формате username#tag
        game: 'valorant' или 'lol'
    
    Returns:
        Tuple[bool, str]: (успех, сообщение об ошибке)
    """
    if not riot_id or '#' not in riot_id:
        return False, "Riot ID должен быть в формате username#tag"
    
    username, tag = riot_id.split('#', 1)
    
    if not username or not tag:
        return False, "Riot ID должен содержать username и tag"
    
    if len(username) < 3 or len(username) > 16:
        return False, "Username должен быть от 3 до 16 символов"
    
    if len(tag) < 3 or len(tag) > 5:
        return False, "Tag должен быть от 3 до 5 символов"
    
    # Проверка через Riot API
    try:
        # Для Valorant используем сторонний API (т.к. официальный требует авторизации)
        if game == 'valorant':
            url = f"https://api.henrikdev.xyz/valorant/v1/account/{username}/{tag}"
            
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    if response.status == 200:
                        data = await response.json()
                        if data.get('status') == 200:
                            return True, f"{username}#{tag}"
                        else:
                            return False, "Riot аккаунт не найден"
                    else:
                        return False, f"Ошибка Valorant API: {response.status}"
        
        # Для LoL
        elif game == 'lol':
            # Здесь будет проверка через Riot API
            # Пока возвращаем успех для тестирования
            return True, f"{username}#{tag}"
        
        else:
            return False, f"Неподдерживаемая игра: {game}"
    
    except Exception as e:
        return False, f"Ошибка при проверке Riot ID: {str(e)}"

async def validate_wot_id(wot_id: str, region: str = 'ru') -> Tuple[bool, str]:
    """
    Валидация World of Tanks Player ID
    
    Args:
        wot_id: Player ID WoT
        region: Регион ('ru', 'eu', 'na', 'asia')
    
    Returns:
        Tuple[bool, str]: (успех, сообщение об ошибке/никнейм)
    """
    if not wot_id.isdigit():
        return False, "Player ID должен содержать только цифры"
    
    if len(wot_id) < 6 or len(wot_id) > 10:
        return False, "Player ID должен быть от 6 до 10 цифр"
    
    # Проверка через WoT API
    try:
        regions = {
            'ru': 'https://api.worldoftanks.ru/wot/',
            'eu': 'https://api.worldoftanks.eu/wot/',
            'na': 'https://api.worldoftanks.com/wot/',
            'asia': 'https://api.worldoftanks.asia/wot/'
        }
        
        base_url = regions.get(region, regions['ru'])
        url = f"{base_url}account/info/"
        
        params = {
            'application_id': config.WOT_APPLICATION_ID,
            'account_id': wot_id,
            'fields': 'nickname,account_id'
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    if data.get('status') == 'ok':
                        account_data = data.get('data', {}).get(wot_id, {})
                        if account_data:
                            nickname = account_data.get('nickname', f'WoT_{wot_id[-6:]}')
                            return True, nickname
                        else:
                            return False, "Аккаунт WoT не найден"
                    else:
                        return False, f"Ошибка WoT API: {data.get('error', {}).get('message', 'Unknown error')}"
                
                return False, f"Ошибка HTTP: {response.status}"
    
    except Exception as e:
        return False, f"Ошибка при проверке WoT ID: {str(e)}"

async def validate_pubg_id(pubg_id: str, platform: str = 'steam') -> Tuple[bool, str]:
    """
    Валидация PUBG Player ID или имени
    
    Args:
        pubg_id: Player ID или имя игрока PUBG
        platform: Платформа ('steam', 'xbox', 'psn', 'kakao')
    
    Returns:
        Tuple[bool, str]: (успех, сообщение об ошибке/никнейм)
    """
    if not pubg_id:
        return False, "Player ID не может быть пустым"
    
    # PUBG принимает как ID, так и имена игроков
    # Проверяем через PUBG API
    try:
        url = f"https://api.pubg.com/shards/{platform}/players"
        params = {'filter[playerNames]': pubg_id}
        headers = {
            'Authorization': f'Bearer {config.PUBG_API_KEY}',
            'Accept': 'application/vnd.api+json'
        }
        
        async with aiohttp.ClientSession(headers=headers) as session:
            async with session.get(url, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    if data.get('data'):
                        player = data['data'][0]
                        nickname = player.get('attributes', {}).get('name', pubg_id)
                        return True, nickname
                    else:
                        return False, "Игрок PUBG не найден"
                elif response.status == 404:
                    return False, "Игрок PUBG не найден"
                else:
                    return False, f"Ошибка PUBG API: {response.status}"
    
    except Exception as e:
        return False, f"Ошибка при проверке PUBG ID: {str(e)}"

def validate_email(email: str) -> bool:
    """Валидация email адреса"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_telegram_id(tg_id: str) -> bool:
    """Валидация Telegram ID"""
    return tg_id.isdigit() and len(tg_id) >= 5 and len(tg_id) <= 12

def validate_date(date_str: str, format: str = '%d.%m.%Y') -> bool:
    """Валидация даты"""
    try:
        datetime.strptime(date_str, format)
        return True
    except ValueError:
        return False

def validate_time(time_str: str) -> bool:
    """Валидация времени"""
    pattern = r'^([01]?[0-9]|2[0-3]):[0-5][0-9]$'
    return re.match(pattern, time_str) is not None

def validate_compare_depth(depth: int) -> Tuple[bool, str]:
    """Валидация глубины сравнения"""
    if depth < 1:
        return False, "Глубина сравнения должна быть не менее 1"
    if depth > config.MAX_COMPARE_DEPTH:
        return False, f"Максимальная глубина сравнения: {config.MAX_COMPARE_DEPTH}"
    return True, ""

def validate_subscription_plan(plan: str) -> bool:
    """Валидация типа подписки"""
    valid_plans = ['1_month', '3_months', '6_months', '12_months', 'infinite']
    return plan in valid_plans

def validate_payment_method(method: str) -> bool:
    """Валидация способа оплаты"""
    valid_methods = ['crypto', 'telegram_stars', 'admin']
    return method in valid_methods

def validate_crypto_address(address: str) -> Tuple[bool, str]:
    """Валидация криптоадреса"""
    if not address:
        return False, "Адрес не может быть пустым"
    
    # Базовые проверки для разных криптовалют
    # BTC: начинается с 1, 3 или bc1, 26-35 символов
    # ETH: начинается с 0x, 42 символа
    # USDT (TRC20): начинается с T, 34 символа
    
    address = address.strip()
    
    # Проверка для BTC
    if address.startswith(('1', '3', 'bc1')):
        if len(address) < 26 or len(address) > 42:
            return False, "Неверная длина BTC адреса"
        return True, "BTC"
    
    # Проверка для ETH
    elif address.startswith('0x'):
        if len(address) != 42:
            return False, "Неверная длина ETH адреса"
        return True, "ETH"
    
    # Проверка для TRC20 (USDT)
    elif address.startswith('T'):
        if len(address) != 34:
            return False, "Неверная длина TRC20 адреса"
        return True, "TRC20"
    
    else:
        return False, "Неизвестный формат криптоадреса"

def sanitize_input(text: str, max_length: int = 255) -> str:
    """Очистка и обрезка пользовательского ввода"""
    if not text:
        return ""
    
    # Удаляем опасные символы
    text = re.sub(r'[<>"\']', '', text)
    
    # Обрезаем до максимальной длины
    if len(text) > max_length:
        text = text[:max_length]
    
    return text.strip()

def validate_game_name(game: str) -> bool:
    """Валидация названия игры"""
    valid_games = ['csgo', 'dota2', 'valorant', 'lol', 'wot', 'pubg']
    return game in valid_games

def validate_region(game: str, region: str) -> bool:
    """Валидация региона для игры"""
    regions_by_game = {
        'csgo': ['eu', 'na', 'asia', 'ru'],
        'dota2': ['eu', 'na', 'sea', 'cn', 'ru'],
        'valorant': ['eu', 'na', 'ap', 'kr', 'br', 'latam'],
        'lol': ['euw', 'eune', 'na', 'kr', 'br', 'lan', 'las', 'oce', 'ru', 'tr', 'jp'],
        'wot': ['eu', 'ru', 'na', 'asia'],
        'pubg': ['steam', 'xbox', 'psn', 'kakao']
    }
    
    valid_regions = regions_by_game.get(game, [])
    return region in valid_regions
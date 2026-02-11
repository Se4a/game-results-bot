from typing import Dict, List
from datetime import datetime

class GameFormatter:
    @staticmethod
    def format_csgo_match_report(match_data: Dict, language: str = 'en') -> str:
        """Форматирует отчет о матче CS:GO"""
        
        translations = {
            'ru': {
                'match_report': 'ОТЧЕТ О МАТЧЕ',
                'account': 'Аккаунт',
                'result': 'Результат',
                'date': 'Дата',
                'time': 'Время',
                'map': 'Карта',
                'player': 'Игрок',
                'kills': 'Убийства',
                'assists': 'Помощи',
                'deaths': 'Смерти',
                'kd': 'K/D',
                'adr': 'ADR',
                'hs': 'HS%',
                'mvp': 'MVP',
                'rating': 'Рейтинг',
                'avg_kda': 'Средний KDA',
                'avg_adr': 'Средний ADR',
                'avg_hs': 'Средний HS%'
            },
            'en': {
                'match_report': 'MATCH REPORT',
                'account': 'Account',
                'result': 'Result',
                'date': 'Date',
                'time': 'Time',
                'map': 'Map',
                'player': 'Player',
                'kills': 'Kills',
                'assists': 'Assists',
                'deaths': 'Deaths',
                'kd': 'K/D',
                'adr': 'ADR',
                'hs': 'HS%',
                'mvp': 'MVP',
                'rating': 'Rating',
                'avg_kda': 'Average KDA',
                'avg_adr': 'Average ADR',
                'avg_hs': 'Average HS%'
            }
        }
        
        t = translations.get(language, translations['en'])
        
        report = f"""
🎯 <b>CS:GO | {t['match_report']}</b>
👤 {t['account']}: {match_data.get('player_name', 'N/A')}
🏆 {t['result']}: {match_data.get('result', 'N/A')}
📅 {t['date']}: {match_data.get('date', 'N/A')}
⏱️ {t['time']}: {match_data.get('duration', 'N/A')}
🗺️ {t['map']}: {match_data.get('map', 'N/A')}

<b>{t['player']} | {t['kills']} | {t['assists']} | {t['deaths']} | {t['kd']} | {t['adr']} | {t['hs']} | {t['mvp']} | {t['rating']}</b>
<code>
{match_data.get('player_name', 'Player'):<15} | {match_data.get('kills', 0):<2} | {match_data.get('assists', 0):<2} | {match_data.get('deaths', 0):<2} | {match_data.get('kd_ratio', 0):<4.2f} | {match_data.get('adr', 0):<4} | {match_data.get('hs_percentage', 0):<4.1f}% | {match_data.get('mvp', 0):<2} | {match_data.get('rating', 0):<5.2f}
</code>

📊 {t['avg_kda']}: {match_data.get('avg_kda', 'N/A'):.2f}
🎯 {t['avg_adr']}: {match_data.get('avg_adr', 'N/A'):.1f}
🎯 {t['avg_hs']}: {match_data.get('avg_hs_percentage', 'N/A'):.1f}%
"""
        return report
    
    @staticmethod
    def format_dota_match_report(match_data: Dict, language: str = 'en') -> str:
        """Форматирует отчет о матче Dota 2"""
        
        translations = {
            'ru': {
                'match_report': 'ОТЧЕТ О МАТЧЕ',
                'account': 'Аккаунт',
                'result': 'Результат',
                'date': 'Дата',
                'time': 'Время',
                'hero': 'Герой',
                'player': 'Игрок',
                'kills': 'Убийства',
                'deaths': 'Смерти',
                'assists': 'Помощи',
                'kda': 'KDA',
                'gpm': 'GPM',
                'xpm': 'XPM',
                'last_hits': 'Посл. удары',
                'denies': 'Денаи',
                'hero_damage': 'Урон героям',
                'tower_damage': 'Урон башням',
                'net_worth': 'Стоимость',
                'role': 'Роль',
                'avg_kda': 'Средний KDA',
                'avg_gpm': 'Средний GPM',
                'avg_xpm': 'Средний XPM'
            },
            'en': {
                'match_report': 'MATCH REPORT',
                'account': 'Account',
                'result': 'Result',
                'date': 'Date',
                'time': 'Time',
                'hero': 'Hero',
                'player': 'Player',
                'kills': 'Kills',
                'deaths': 'Deaths',
                'assists': 'Assists',
                'kda': 'KDA',
                'gpm': 'GPM',
                'xpm': 'XPM',
                'last_hits': 'Last Hits',
                'denies': 'Denies',
                'hero_damage': 'Hero Damage',
                'tower_damage': 'Tower Damage',
                'net_worth': 'Net Worth',
                'role': 'Role',
                'avg_kda': 'Average KDA',
                'avg_gpm': 'Average GPM',
                'avg_xpm': 'Average XPM'
            }
        }
        
        t = translations.get(language, translations['en'])
        
        report = f"""
⚔️ <b>Dota 2 | {t['match_report']}</b>
👤 {t['account']}: {match_data.get('player_name', 'N/A')}
🏆 {t['result']}: {match_data.get('result', 'N/A')}
📅 {t['date']}: {match_data.get('date', 'N/A')}
⏱️ {t['time']}: {match_data.get('duration', 'N/A')}
🎭 {t['hero']}: {match_data.get('hero', 'N/A')}
🎯 {t['role']}: {match_data.get('role', 'N/A')}

<b>{t['player']} | {t['kills']} | {t['deaths']} | {t['assists']} | {t['kda']} | {t['gpm']} | {t['xpm']} | {t['last_hits']} | {t['denies']}</b>
<code>
{match_data.get('player_name', 'Player'):<15} | {match_data.get('kills', 0):<2} | {match_data.get('deaths', 0):<2} | {match_data.get('assists', 0):<2} | {match_data.get('kda', 0):<5.2f} | {match_data.get('gpm', 0):<4} | {match_data.get('xpm', 0):<4} | {match_data.get('last_hits', 0):<3} | {match_data.get('denies', 0):<2}
</code>

💰 {t['net_worth']}: {match_data.get('net_worth', 0):,}
⚔️ {t['hero_damage']}: {match_data.get('hero_damage', 0):,}
🏰 {t['tower_damage']}: {match_data.get('tower_damage', 0):,}

📊 {t['avg_kda']}: {match_data.get('avg_kda', 'N/A'):.2f}
💰 {t['avg_gpm']}: {match_data.get('avg_gpm', 'N/A'):.0f}
⚡ {t['avg_xpm']}: {match_data.get('avg_xpm', 'N/A'):.0f}
"""
        return report
    
    @staticmethod
    def format_valorant_match_report(match_data: Dict, language: str = 'en') -> str:
        """Форматирует отчет о матче Valorant"""
        
        translations = {
            'ru': {
                'match_report': 'ОТЧЕТ О МАТЧЕ',
                'account': 'Аккаунт',
                'result': 'Результат',
                'date': 'Дата',
                'time': 'Время',
                'map': 'Карта',
                'agent': 'Агент',
                'player': 'Игрок',
                'kills': 'Убийства',
                'deaths': 'Смерти',
                'assists': 'Помощи',
                'acs': 'ACS',
                'hs': 'HS%',
                'first_bloods': 'Первая кровь',
                'plants': 'Установки',
                'defuses': 'Обезвреж.',
                'economy': 'Экономика',
                'avg_acs': 'Средний ACS',
                'avg_kd': 'Средний K/D',
                'avg_hs': 'Средний HS%'
            },
            'en': {
                'match_report': 'MATCH REPORT',
                'account': 'Account',
                'result': 'Result',
                'date': 'Date',
                'time': 'Time',
                'map': 'Map',
                'agent': 'Agent',
                'player': 'Player',
                'kills': 'Kills',
                'deaths': 'Deaths',
                'assists': 'Assists',
                'acs': 'ACS',
                'hs': 'HS%',
                'first_bloods': 'First Blood',
                'plants': 'Plants',
                'defuses': 'Defuses',
                'economy': 'Economy',
                'avg_acs': 'Average ACS',
                'avg_kd': 'Average K/D',
                'avg_hs': 'Average HS%'
            }
        }
        
        t = translations.get(language, translations['en'])
        
        report = f"""
🔫 <b>Valorant | {t['match_report']}</b>
👤 {t['account']}: {match_data.get('player_name', 'N/A')}
🏆 {t['result']}: {match_data.get('result', 'N/A')}
📅 {t['date']}: {match_data.get('date', 'N/A')}
⏱️ {t['time']}: {match_data.get('duration', 'N/A')}
🗺️ {t['map']}: {match_data.get('map', 'N/A')}
🕵️ {t['agent']}: {match_data.get('agent', 'N/A')}

<b>{t['player']} | {t['kills']} | {t['deaths']} | {t['assists']} | {t['acs']} | {t['hs']} | {t['first_bloods']} | {t['plants']} | {t['defuses']}</b>
<code>
{match_data.get('player_name', 'Player'):<15} | {match_data.get('kills', 0):<2} | {match_data.get('deaths', 0):<2} | {match_data.get('assists', 0):<2} | {match_data.get('acs', 0):<3} | {match_data.get('hs_percentage', 0):<4.1f}% | {match_data.get('first_bloods', 0):<2} | {match_data.get('plants', 0):<2} | {match_data.get('defuses', 0):<2}
</code>

💰 {t['economy']}: {match_data.get('economy_rating', 0)}/100
🎯 {t['avg_acs']}: {match_data.get('avg_acs', 'N/A'):.0f}
⚔️ {t['avg_kd']}: {match_data.get('avg_kd_ratio', 'N/A'):.2f}
🎯 {t['avg_hs']}: {match_data.get('avg_hs_percentage', 'N/A'):.1f}%
"""
        return report
    
    @staticmethod
    def format_lol_match_report(match_data: Dict, language: str = 'en') -> str:
        """Форматирует отчет о матче League of Legends"""
        
        translations = {
            'ru': {
                'match_report': 'ОТЧЕТ О МАТЧЕ',
                'account': 'Аккаунт',
                'result': 'Результат',
                'date': 'Дата',
                'time': 'Время',
                'champion': 'Чемпион',
                'lane': 'Линия',
                'player': 'Игрок',
                'kills': 'Убийства',
                'deaths': 'Смерти',
                'assists': 'Помощи',
                'kda': 'KDA',
                'cs': 'CS',
                'cs_per_min': 'CS/мин',
                'gold': 'Золото',
                'vision': 'Очки зрения',
                'damage': 'Урон',
                'kill_participation': 'Участие в убийствах',
                'avg_kda': 'Средний KDA',
                'avg_cs_per_min': 'Средний CS/мин',
                'avg_vision': 'Средние очки зрения'
            },
            'en': {
                'match_report': 'MATCH REPORT',
                'account': 'Account',
                'result': 'Result',
                'date': 'Date',
                'time': 'Time',
                'champion': 'Champion',
                'lane': 'Lane',
                'player': 'Player',
                'kills': 'Kills',
                'deaths': 'Deaths',
                'assists': 'Assists',
                'kda': 'KDA',
                'cs': 'CS',
                'cs_per_min': 'CS/min',
                'gold': 'Gold',
                'vision': 'Vision Score',
                'damage': 'Damage',
                'kill_participation': 'Kill Participation',
                'avg_kda': 'Average KDA',
                'avg_cs_per_min': 'Average CS/min',
                'avg_vision': 'Average Vision Score'
            }
        }
        
        t = translations.get(language, translations['en'])
        
        report = f"""
🏆 <b>League of Legends | {t['match_report']}</b>
👤 {t['account']}: {match_data.get('player_name', 'N/A')}
🏆 {t['result']}: {match_data.get('result', 'N/A')}
📅 {t['date']}: {match_data.get('date', 'N/A')}
⏱️ {t['time']}: {match_data.get('duration', 'N/A')}
🎭 {t['champion']}: {match_data.get('champion', 'N/A')}
🛣️ {t['lane']}: {match_data.get('lane', 'N/A')}

<b>{t['player']} | {t['kills']} | {t['deaths']} | {t['assists']} | {t['kda']} | {t['cs']} | {t['cs_per_min']} | {t['gold']} | {t['vision']}</b>
<code>
{match_data.get('player_name', 'Player'):<15} | {match_data.get('kills', 0):<2} | {match_data.get('deaths', 0):<2} | {match_data.get('assists', 0):<2} | {match_data.get('kda', 0):<5.2f} | {match_data.get('cs', 0):<3} | {match_data.get('cs_per_min', 0):<5.1f} | {match_data.get('gold', 0):<6,} | {match_data.get('vision_score', 0):<2}
</code>

⚔️ {t['damage']}: {match_data.get('damage', 0):,}
🎯 {t['kill_participation']}: {match_data.get('kill_participation', 0)}%

📊 {t['avg_kda']}: {match_data.get('avg_kda', 'N/A'):.2f}
🌾 {t['avg_cs_per_min']}: {match_data.get('avg_cs_per_min', 'N/A'):.1f}
👁️ {t['avg_vision']}: {match_data.get('avg_vision_score', 'N/A'):.1f}
"""
        return report
    
    @staticmethod
    def format_wot_match_report(match_data: Dict, language: str = 'en') -> str:
        """Форматирует отчет о бою World of Tanks"""
        
        translations = {
            'ru': {
                'battle_report': 'ОТЧЕТ О БОЮ',
                'account': 'Аккаунт',
                'result': 'Результат',
                'date': 'Дата',
                'time': 'Время',
                'tank': 'Танк',
                'tier': 'Уровень',
                'nation': 'Нация',
                'damage': 'Урон',
                'assisted_damage': 'Урон по разведке',
                'blocked_damage': 'Заблокировано',
                'kills': 'Уничтожено',
                'spotted': 'Обнаружено',
                'xp': 'Опыт',
                'wn8': 'WN8',
                'credits': 'Кредиты',
                'map': 'Карта',
                'survived': 'Выжил',
                'avg_damage': 'Средний урон',
                'avg_kills': 'Среднее уничтожено',
                'avg_wn8': 'Средний WN8'
            },
            'en': {
                'battle_report': 'BATTLE REPORT',
                'account': 'Account',
                'result': 'Result',
                'date': 'Date',
                'time': 'Time',
                'tank': 'Tank',
                'tier': 'Tier',
                'nation': 'Nation',
                'damage': 'Damage',
                'assisted_damage': 'Assisted Damage',
                'blocked_damage': 'Blocked Damage',
                'kills': 'Kills',
                'spotted': 'Spotted',
                'xp': 'XP',
                'wn8': 'WN8',
                'credits': 'Credits',
                'map': 'Map',
                'survived': 'Survived',
                'avg_damage': 'Average Damage',
                'avg_kills': 'Average Kills',
                'avg_wn8': 'Average WN8'
            }
        }
        
        t = translations.get(language, translations['en'])
        
        survived = match_data.get('survived', False)
        survived_text = f"{'✅ ' if survived else '❌ '}{t['survived']}"
        
        report = f"""
🎖️ <b>World of Tanks | {t['battle_report']}</b>
👤 {t['account']}: {match_data.get('player_name', 'N/A')}
🏆 {t['result']}: {match_data.get('result', 'N/A')}
📅 {t['date']}: {match_data.get('date', 'N/A')}
⏱️ {t['time']}: {match_data.get('duration', 'N/A')}
⚙️ {t['tank']}: {match_data.get('tank', 'N/A')}
⭐ {t['tier']}: {match_data.get('tier', 'N/A')}
🇷🇺 {t['nation']}: {match_data.get('nation', 'N/A')}
🗺️ {t['map']}: {match_data.get('map', 'N/A')}

<b>{t['player']} | {t['damage']} | {t['assisted_damage']} | {t['blocked_damage']} | {t['kills']} | {t['spotted']} | {t['xp']} | {t['wn8']}</b>
<code>
{match_data.get('player_name', 'Player'):<15} | {match_data.get('damage', 0):<5} | {match_data.get('assisted_damage', 0):<5} | {match_data.get('blocked_damage', 0):<5} | {match_data.get('kills', 0):<2} | {match_data.get('spotted', 0):<2} | {match_data.get('xp', 0):<4} | {match_data.get('wn8', 0):<4}
</code>

💰 {t['credits']}: {match_data.get('credits', 0):,}
{survived_text}

📊 {t['avg_damage']}: {match_data.get('avg_damage', 'N/A'):.0f}
⚔️ {t['avg_kills']}: {match_data.get('avg_kills', 'N/A'):.1f}
🏆 {t['avg_wn8']}: {match_data.get('avg_wn8', 'N/A'):.0f}
"""
        return report
    
    @staticmethod
    def format_pubg_match_report(match_data: Dict, language: str = 'en') -> str:
        """Форматирует отчет о матче PUBG"""
        
        translations = {
            'ru': {
                'match_report': 'ОТЧЕТ О МАТЧЕ',
                'account': 'Аккаунт',
                'result': 'Результат',
                'date': 'Дата',
                'time': 'Время',
                'map': 'Карта',
                'mode': 'Режим',
                'rank': 'Место',
                'kills': 'Убийства',
                'assists': 'Помощи',
                'damage': 'Урон',
                'headshot_kills': 'Хедшоты',
                'longest_kill': 'Дальний килл',
                'survival_time': 'Время выживания',
                'walk_distance': 'Пройдено пешком',
                'drive_distance': 'Пройдено на ТС',
                'avg_kills': 'Средние убийства',
                'avg_damage': 'Средний урон',
                'avg_survival_time': 'Среднее время выживания'
            },
            'en': {
                'match_report': 'MATCH REPORT',
                'account': 'Account',
                'result': 'Result',
                'date': 'Date',
                'time': 'Time',
                'map': 'Map',
                'mode': 'Mode',
                'rank': 'Rank',
                'kills': 'Kills',
                'assists': 'Assists',
                'damage': 'Damage',
                'headshot_kills': 'Headshots',
                'longest_kill': 'Longest Kill',
                'survival_time': 'Survival Time',
                'walk_distance': 'Walk Distance',
                'drive_distance': 'Drive Distance',
                'avg_kills': 'Average Kills',
                'avg_damage': 'Average Damage',
                'avg_survival_time': 'Average Survival Time'
            }
        }
        
        t = translations.get(language, translations['en'])
        
        rank = match_data.get('rank', 0)
        rank_text = f"#{rank}" if rank > 0 else "N/A"
        
        report = f"""
🌍 <b>PUBG | {t['match_report']}</b>
👤 {t['account']}: {match_data.get('player_name', 'N/A')}
🏆 {t['result']}: {match_data.get('result', 'N/A')}
📅 {t['date']}: {match_data.get('date', 'N/A')}
⏱️ {t['time']}: {match_data.get('duration', 'N/A')}
🗺️ {t['map']}: {match_data.get('map', 'N/A')}
🎮 {t['mode']}: {match_data.get('mode', 'N/A')}
🥇 {t['rank']}: {rank_text}

<b>{t['player']} | {t['kills']} | {t['assists']} | {t['damage']} | {t['headshot_kills']} | {t['longest_kill']}м | {t['survival_time']}мин</b>
<code>
{match_data.get('player_name', 'Player'):<15} | {match_data.get('kills', 0):<2} | {match_data.get('assists', 0):<2} | {match_data.get('damage', 0):<4} | {match_data.get('headshot_kills', 0):<2} | {match_data.get('longest_kill', 0):<5.1f} | {match_data.get('survival_time', 0):<5.1f}
</code>

🚶 {t['walk_distance']}: {match_data.get('walk_distance', 0):.0f}м
🚗 {t['drive_distance']}: {match_data.get('drive_distance', 0):.0f}м

📊 {t['avg_kills']}: {match_data.get('avg_kills', 'N/A'):.1f}
⚔️ {t['avg_damage']}: {match_data.get('avg_damage', 'N/A'):.0f}
⏱️ {t['avg_survival_time']}: {match_data.get('avg_survival_time', 'N/A'):.1f} мин
"""
        return report
    
    @staticmethod
    def format_match_report(game: str, match_data: Dict, language: str = 'en') -> str:
        """Форматирует отчет о матче для любой игры"""
        
        formatters = {
            'csgo': GameFormatter.format_csgo_match_report,
            'dota2': GameFormatter.format_dota_match_report,
            'valorant': GameFormatter.format_valorant_match_report,
            'lol': GameFormatter.format_lol_match_report,
            'wot': GameFormatter.format_wot_match_report,
            'pubg': GameFormatter.format_pubg_match_report
        }
        
        formatter = formatters.get(game)
        if formatter:
            return formatter(match_data, language)
        else:
            return f"<b>{game.upper()} | MATCH REPORT</b>\n\nData: {json.dumps(match_data, indent=2)}"
from typing import Dict
import json

class ExtendedGameFormatter:
    """Расширенные форматтеры для полной статистики"""
    
    @staticmethod
    def format_complete_csgo_report(match_data: Dict, player_stats: Dict, language: str = 'en') -> str:
        """Полный отчет CS:GO со всей статистикой"""
        
        text = f"""
🎯 <b>CS:GO | ПОЛНЫЙ ОТЧЕТ О МАТЧЕ</b>

👤 <b>Игрок:</b> {match_data.get('player_name', 'N/A')}
🏆 <b>Результат:</b> {match_data.get('result', 'N/A')}
📅 <b>Дата:</b> {match_data.get('date', 'N/A')}
⏱️ <b>Время:</b> {match_data.get('duration', 'N/A')}
🗺️ <b>Карта:</b> {match_data.get('map', 'N/A')}

<b>📊 ОСНОВНАЯ СТАТИСТИКА:</b>
<code>
Убийства: {player_stats.get('kills', 0):<3} | Смерти: {player_stats.get('deaths', 0):<3} | Помощи: {player_stats.get('assists', 0):<3}
K/D: {player_stats.get('kd_ratio', 0):<5.2f} | ADR: {player_stats.get('adr', 0):<6.1f} | HS%: {player_stats.get('hs_percentage', 0):<5.1f}%
MVP: {player_stats.get('mvp', 0):<2} | Рейтинг: {player_stats.get('rating', 0):<5.2f} | KAST: {player_stats.get('kast', 0):<5.1f}%
</code>

<b>🎯 БОЕВАЯ ЭФФЕКТИВНОСТЬ:</b>
<code>
Входные киллы: {player_stats.get('entry_kills', 0):<2} | Входные смерти: {player_stats.get('entry_deaths', 0):<2}
Мультикиллы: 1k={player_stats.get('multikills', {}).get('1k', 0):<2} 2k={player_stats.get('multikills', {}).get('2k', 0):<2} 3k={player_stats.get('multikills', {}).get('3k', 0):<2} 4k={player_stats.get('multikills', {}).get('4k', 0):<2}
Клачи: 1v1={player_stats.get('clutches', {}).get('1v1', 0):<2} 1v2={player_stats.get('clutches', {}).get('1v2', 0):<2} 1v3={player_stats.get('clutches', {}).get('1v3', 0):<2}
Impact: {player_stats.get('impact', 0):<5.2f} | Трейд киллы: {player_stats.get('trade_kills', 0):<3}
</code>

<b>💰 ЭКОНОМИКА:</b>
<code>
Средние деньги: ${player_stats.get('avg_money', 0):<6}
Потрачено: ${player_stats.get('money_spent', 0):<7}
Эко-раунды: {player_stats.get('eco_rounds', 0):<3} | Форс-баи: {player_stats.get('force_buys', 0):<3}
</code>

<b>🧨 УТИЛИТЫ:</b>
<code>
HE гранаты: {player_stats.get('he_grenades', {}).get('thrown', 0):<3} (урон: {player_stats.get('he_grenades', {}).get('damage', 0)})
Флешки: {player_stats.get('flashbangs', {}).get('thrown', 0):<3} (ослеплений: {player_stats.get('flashbangs', {}).get('enemies_flashed', 0)})
Дымы: {player_stats.get('smokes', {}).get('thrown', 0):<3} (эффективных: {player_stats.get('smokes', {}).get('effective', 0)})
Молотовы: {player_stats.get('molotovs', {}).get('thrown', 0):<3} (урон: {player_stats.get('molotovs', {}).get('damage', 0)})
</code>

<b>🎯 СТАТИСТИКА ПО ОРУЖИЮ:</b>
"""
        
        # Добавляем статистику по оружию
        for weapon, stats in player_stats.get('weapon_stats', {}).items():
            text += f"<code>{weapon.upper():<8} | Убийств: {stats.get('kills', 0):<3} | HS: {stats.get('headshots', 0):<3} | Точность: {stats.get('accuracy', 0):<5.1f}% | Урон: {stats.get('damage', 0):<6}</code>\n"
        
        text += f"\n📈 <b>СРЕДНИЕ ПОКАЗАТЕЛИ:</b>\n"
        text += f"<code>Средний K/D: {match_data.get('avg_kd', 0):.2f} | Средний ADR: {match_data.get('avg_adr', 0):.1f} | Средний HS%: {match_data.get('avg_hs_percentage', 0):.1f}%</code>"
        
        return text
    
    @staticmethod
    def format_complete_dota_report(match_data: Dict, player_stats: Dict, language: str = 'en') -> str:
        """Полный отчет Dota 2 со всей статистикой"""
        
        text = f"""
⚔️ <b>Dota 2 | ПОЛНЫЙ ОТЧЕТ О МАТЧЕ</b>

👤 <b>Игрок:</b> {match_data.get('player_name', 'N/A')}
🏆 <b>Результат:</b> {match_data.get('result', 'N/A')}
📅 <b>Дата:</b> {match_data.get('date', 'N/A')}
⏱️ <b>Время:</b> {match_data.get('duration', 'N/A')}
🎭 <b>Герой:</b> {match_data.get('hero', 'N/A')}
🎯 <b>Роль:</b> {match_data.get('role', 'N/A')}

<b>📊 ОСНОВНАЯ СТАТИСТИКА:</b>
<code>
K/D/A: {player_stats.get('kills', 0):<2}/{player_stats.get('deaths', 0):<2}/{player_stats.get('assists', 0):<2} | KDA: {player_stats.get('kda', 0):<5.2f}
GPM: {player_stats.get('gpm', 0):<4} | XPM: {player_stats.get('xpm', 0):<4} | NW: {player_stats.get('net_worth', 0):<7,}
LH/D: {player_stats.get('last_hits', 0):<3}/{player_stats.get('denies', 0):<2} | Урон по героям: {player_stats.get('hero_damage', 0):<7,}
Урон по башням: {player_stats.get('tower_damage', 0):<6,} | Станы: {player_stats.get('stuns', 0):<6.1f} сек
</code>

<b>🎯 ЛАЙН-СТАТИСТИКА:</b>
<code>
CS на 10 мин: {player_stats.get('cs_at_10', 0):<3} | Denies на 10 мин: {player_stats.get('denies_at_10', 0):<2}
XP на 10 мин: {player_stats.get('xp_at_10', 0):<5} | Эффективность линии: {player_stats.get('lane_efficiency', 0):<5.1f}%
Урон на харассе: {player_stats.get('harass_damage', 0):<6} | Стаков: {len(player_stats.get('stack_timings', []))}
</code>

<b>👁️ ВИДЕНИЕ И КОНТРОЛЬ:</b>
<code>
Обзерверы: {player_stats.get('observer_wards_placed', 0):<2} | Сентри: {player_stats.get('sentry_wards_placed', 0):<2}
Уничтожено вардов: {player_stats.get('wards_destroyed', 0):<2} | Рун собрано: {player_stats.get('runes_grabbed', 0):<2}
Участие в командных боях: {player_stats.get('teamfight_participation', 0):<5.1f}%
Урон в командных боях: {player_stats.get('damage_in_teamfights', 0):<7,}
</code>

<b>🏰 ОБЪЕКТИВЫ:</b>
<code>
Уничтожено вышек: {player_stats.get('tower_kills', 0):<2} | Рошанов: {player_stats.get('roshan_kills', 0):<2}
Уничтожено бараков: {player_stats.get('barracks_destroyed', 0):<2} | Аутпостов: {player_stats.get('outposts_controlled', 0):<2}
Торментов: {player_stats.get('tormentor_kills', 0):<2} | Вотчер-вардов: {player_stats.get('watcher_wards_placed', 0):<2}
</code>

<b>⏰ ТАЙМИНГИ ИТЕМОВ:</b>
"""
        
        # Добавляем тайминги предметов
        for item in player_stats.get('items_bought', []):
            text += f"<code>{item.get('name', '').upper():<20} на {item.get('time', 0):<5.1f} мин</code>\n"
        
        text += f"\n<b>📈 СРЕДНИЕ ПОКАЗАТЕЛИ:</b>\n"
        text += f"<code>Средний KDA: {match_data.get('avg_kda', 0):.2f} | Средний GPM: {match_data.get('avg_gpm', 0):.0f} | Средний XPM: {match_data.get('avg_xpm', 0):.0f}</code>"
        
        return text
    
    @staticmethod
    def format_complete_valorant_report(match_data: Dict, player_stats: Dict, language: str = 'en') -> str:
        """Полный отчет Valorant со всей статистикой"""
        
        text = f"""
🔫 <b>Valorant | ПОЛНЫЙ ОТЧЕТ О МАТЧЕ</b>

👤 <b>Игрок:</b> {match_data.get('player_name', 'N/A')}
🏆 <b>Результат:</b> {match_data.get('result', 'N/A')}
📅 <b>Дата:</b> {match_data.get('date', 'N/A')}
⏱️ <b>Время:</b> {match_data.get('duration', 'N/A')}
🗺️ <b>Карта:</b> {match_data.get('map', 'N/A')}
🕵️ <b>Агент:</b> {match_data.get('agent', 'N/A')}

<b>📊 ОСНОВНАЯ СТАТИСТИКА:</b>
<code>
K/D/A: {player_stats.get('kills', 0):<2}/{player_stats.get('deaths', 0):<2}/{player_stats.get('assists', 0):<2}
ACS: {player_stats.get('acs', 0):<4} | ADR: {player_stats.get('adr', 0):<5.1f} | HS%: {player_stats.get('hs_percentage', 0):<5.1f}%
First Bloods: {player_stats.get('first_bloods', 0):<2} | First Deaths: {player_stats.get('first_deaths', 0):<2}
Plants: {player_stats.get('plants', 0):<2} | Defuses: {player_stats.get('defuses', 0):<2}
KAST: {player_stats.get('kast', 0):<5.1f}% | Combat Score: {player_stats.get('combat_score', 0):<6}
</code>

<b>🎯 БОЕВАЯ ЭФФЕКТИВНОСТЬ:</b>
<code>
Мультикиллы: 1k={player_stats.get('multikills', {}).get('1k', 0):<2} 2k={player_stats.get('multikills', {}).get('2k', 0):<2} 3k={player_stats.get('multikills', {}).get('3k', 0):<2}
Клачи: 1v1={player_stats.get('clutches', {}).get('1v1', 0):<2} 1v2={player_stats.get('clutches', {}).get('1v2', 0):<2}
Экономический рейтинг: {player_stats.get('economy_rating', 0):<3}/100
</code>

<b>🎯 СТАТИСТИКА ПО ОРУЖИЮ:</b>
"""
        
        # Добавляем статистику по оружию
        for weapon, stats in player_stats.get('weapon_stats', {}).items():
            text += f"<code>{weapon.upper():<10} | Убийств: {stats.get('kills', 0):<3} | HS: {stats.get('headshots', 0):<3} | Точность: {stats.get('accuracy', 0):<5.1f}%</code>\n"
        
        text += f"\n<b>✨ СПОСОБНОСТИ:</b>\n"
        for ability, stats in player_stats.get('ability_stats', {}).items():
            text += f"<code>{ability.upper():<5} | Использований: {stats.get('uses', 0):<3} | Килов: {stats.get('kills', 0):<3}</code>\n"
        
        text += f"\n<b>💰 ЭКОНОМИКА:</b>\n"
        text += f"<code>Средние кредиты: {player_stats.get('avg_credits', 0):<5} | Потрачено: {player_stats.get('credits_spent', 0):<7}</code>\n"
        text += f"<code>Раунды сейва: {player_stats.get('save_rounds', 0):<2} | Эко-раунды: {player_stats.get('eco_rounds', 0):<2} | Фулл-баи: {player_stats.get('full_buy_rounds', 0):<2}</code>"
        
        return text
    
    @staticmethod
    def format_complete_lol_report(match_data: Dict, player_stats: Dict, language: str = 'en') -> str:
        """Полный отчет LoL со всей статистикой"""
        
        text = f"""
🏆 <b>League of Legends | ПОЛНЫЙ ОТЧЕТ О МАТЧЕ</b>

👤 <b>Игрок:</b> {match_data.get('player_name', 'N/A')}
🏆 <b>Результат:</b> {match_data.get('result', 'N/A')}
📅 <b>Дата:</b> {match_data.get('date', 'N/A')}
⏱️ <b>Время:</b> {match_data.get('duration', 'N/A')}
🎭 <b>Чемпион:</b> {match_data.get('champion', 'N/A')}
🛣️ <b>Линия:</b> {match_data.get('lane', 'N/A')}

<b>📊 ОСНОВНАЯ СТАТИСТИКА:</b>
<code>
K/D/A: {player_stats.get('kills', 0):<2}/{player_stats.get('deaths', 0):<2}/{player_stats.get('assists', 0):<2} | KDA: {player_stats.get('kda', 0):<5.2f}
CS: {player_stats.get('cs', 0):<4} ({player_stats.get('cs_per_min', 0):<5.1f}/мин) | Золото: {player_stats.get('gold', 0):<7,}
Урон чемпионам: {player_stats.get('damage_to_champions', 0):<7,} | Полученный урон: {player_stats.get('damage_taken', 0):<7,}
Vision Score: {player_stats.get('vision_score', 0):<3} | Участие в киллах: {player_stats.get('kill_participation', 0):<3}%
Урон по башням: {player_stats.get('turret_damage', 0):<6,} | Урон по объектам: {player_stats.get('objective_damage', 0):<6,}
Время CC: {player_stats.get('time_ccing_others', 0):<5.1f} сек | Лечение: {player_stats.get('healing', 0):<6,}
</code>

<b>👁️ ВИДЕНИЕ:</b>
<code>
Установлено вардов: {player_stats.get('wards_placed', 0):<3} | Уничтожено вардов: {player_stats.get('wards_destroyed', 0):<3}
Контрольных вардов: {player_stats.get('control_wards_placed', 0):<2} | Vision Score/мин: {player_stats.get('vision_score_per_min', 0):<5.2f}
Видение реки: {player_stats.get('river_vision', 0):<5.1f}% | Видение вражеского леса: {player_stats.get('enemy_jungle_vision', 0):<5.1f}%
</code>

<b>🏰 ОБЪЕКТИВЫ:</b>
<code>
Уничтожено вышек: {player_stats.get('turrets_destroyed', 0):<2} | Ингибиторов: {player_stats.get('inhibitors_destroyed', 0):<2}
Драконов: {player_stats.get('drakes_killed', 0):<2} | Геральдов: {player_stats.get('heralds_killed', 0):<2}
Баронов: {player_stats.get('barons_killed', 0):<2} | Элдеров: {player_stats.get('elder_drakes_killed', 0):<2}
Контроль объектов: {player_stats.get('objective_control', 0):<5.1f}%
</code>

<b>⚔️ КОМАНДНЫЕ БОИ:</b>
<code>
Участие в командных боях: {player_stats.get('teamfight_participation', 0):<5.1f}%
Урон в командных боях: {player_stats.get('damage_in_teamfights', 0):<7,}
Участие в киллах: {player_stats.get('kill_participation_in_teamfights', 0):<5.1f}%
Выживаемость: {player_stats.get('survival_in_teamfights', 0):<5.1f}%
</code>

<b>📈 СРЕДНИЕ ПОКАЗАТЕЛИ:</b>
<code>
Средний KDA: {match_data.get('avg_kda', 0):.2f} | Средний CS/мин: {match_data.get('avg_cs_per_min', 0):.1f}
Средний Vision Score: {match_data.get('avg_vision_score', 0):.1f} | Средний GPM: {match_data.get('avg_gpm', 0):.0f}
</code>
"""
        return text
    
    @staticmethod
    def format_complete_wot_report(match_data: Dict, player_stats: Dict, language: str = 'en') -> str:
        """Полный отчет WoT со всей статистикой"""
        
        text = f"""
🎖️ <b>World of Tanks | ПОЛНЫЙ ОТЧЕТ О БОЮ</b>

👤 <b>Игрок:</b> {match_data.get('player_name', 'N/A')}
🏆 <b>Результат:</b> {match_data.get('result', 'N/A')}
📅 <b>Дата:</b> {match_data.get('date', 'N/A')}
⏱️ <b>Время:</b> {match_data.get('duration', 'N/A')}
⚙️ <b>Танк:</b> {match_data.get('tank', 'N/A')}
⭐ <b>Уровень:</b> {match_data.get('tier', 'N/A')}
🗺️ <b>Карта:</b> {match_data.get('map', 'N/A')}

<b>📊 ОСНОВНАЯ СТАТИСТИКА:</b>
<code>
Урон: {player_stats.get('damage_dealt', 0):<6} | Урон по разведке: {player_stats.get('damage_assisted', 0):<6}
Заблокировано: {player_stats.get('damage_blocked', 0):<6} | Получено урона: {player_stats.get('damage_received', 0):<6}
Уничтожено: {player_stats.get('kills', 0):<2} | Обнаружено: {player_stats.get('spotted', 0):<2}
Опыт: {player_stats.get('xp', 0):<5} | WN8: {player_stats.get('wn8', 0):<5}
Попадания: {player_stats.get('hit_rate', 0):<5.1f}% | Пробития: {player_stats.get('penetration_rate', 0):<5.1f}%
</code>

<b>🎯 ЭФФЕКТИВНОСТЬ:</b>
<code>
Средний урон: {player_stats.get('avg_damage', 0):<6.0f} | Среднее уничтожено: {player_stats.get('avg_kills', 0):<5.1f}
Средний опыт: {player_stats.get('avg_xp', 0):<5.0f} | Средний WN8: {player_stats.get('avg_wn8', 0):<5.0f}
Выживаемость: {player_stats.get('survival_rate', 0):<5.1f}% | Win Rate: {player_stats.get('win_rate', 0):<5.1f}%
</code>

<b>🛡️ ВЫЖИВАНИЕ И ПОЗИЦИОНИРОВАНИЕ:</b>
<code>
Выжил: {'✅' if player_stats.get('survived', False) else '❌'}
Среднее время жизни: {player_stats.get('avg_lifetime', 0):<5.1f} сек
Использование брони: {player_stats.get('armor_usage', 0):<5.1f}%
Использование укрытий: {player_stats.get('hull_down_usage', 0):<5.1f}%
Сайдскрейпинг: {player_stats.get('side_scraping', 0):<5.1f}%
Оценка позиционирования: {player_stats.get('positioning_score', 0):<5.1f}/100
</code>

<b>👁️ РАЗВЕДКА И ОБНАРУЖЕНИЕ:</b>
<code>
Среднее обнаружено: {player_stats.get('avg_spotted', 0):<5.1f}
Урон по разведке: {player_stats.get('assisted_damage', 0):<6}
Помощь по обнаружению: {player_stats.get('spotting_assistance', 0):<5.1f}%
Помощь по трекингу: {player_stats.get('track_assistance', 0):<5.1f}%
Использование дальности обзора: {player_stats.get('vision_range_usage', 0):<5.1f}%
</code>

<b>⚔️ ДЕТАЛЬНАЯ СТАТИСТИКА УРОНА:</b>
<code>
Урон за выстрел: {player_stats.get('damage_per_shot', 0):<5.0f}
Урон в минуту: {player_stats.get('damage_per_minute', 0):<6.0f}
Критические попадания: {player_stats.get('critical_hits', 0):<3}
Урон по модулям: {player_stats.get('module_damage', 0):<5}
Урон по экипажу: {player_stats.get('crew_damage', 0):<3}
Соотношение урона: {player_stats.get('damage_ratio', 0):<5.2f}
</code>

<b>🏆 WN8 И РЕЙТИНГИ:</b>
<code>
WN8: {player_stats.get('wn8', 0):<5} | WN7: {player_stats.get('wn7', 0):<5}
WGR: {player_stats.get('wgr', 0):<5} | Эффективность: {player_stats.get('efficiency', 0):<5}
Рейтинг производительности: {player_stats.get('performance_rating', 0):<5}
Персональный рейтинг: {player_stats.get('personal_rating', 0):<5}
</code>

<b>🎯 СТАТИСТИКА ПО ТАНКУ:</b>
"""
        
        # Добавляем статистику по танку
        tank_stats = player_stats.get('tank_stats', {}).get('object_140', {})
        if tank_stats:
            text += f"<code>Боёв: {tank_stats.get('battles', 0):<4} | Побед: {tank_stats.get('wins', 0):<3} | Win Rate: {tank_stats.get('win_rate', 0):<5.1f}%</code>\n"
            text += f"<code>Средний урон: {tank_stats.get('avg_damage', 0):<6.0f} | Среднее уничтожено: {tank_stats.get('avg_kills', 0):<5.1f}</code>\n"
            text += f"<code>Средний опыт: {tank_stats.get('avg_xp', 0):<5.0f} | WN8: {tank_stats.get('wn8', 0):<5} | Попадания: {tank_stats.get('hit_rate', 0):<5.1f}%</code>"
        
        return text
    
    @staticmethod
    def format_complete_pubg_report(match_data: Dict, player_stats: Dict, language: str = 'en') -> str:
        """Полный отчет PUBG со всей статистикой"""
        
        text = f"""
🌍 <b>PUBG | ПОЛНЫЙ ОТЧЕТ О МАТЧЕ</b>

👤 <b>Игрок:</b> {match_data.get('player_name', 'N/A')}
🏆 <b>Результат:</b> #{match_data.get('rank', 0)} (Top {match_data.get('top_percentage', 0):.1f}%)
📅 <b>Дата:</b> {match_data.get('date', 'N/A')}
⏱️ <b>Время:</b> {match_data.get('duration', 'N/A')}
🗺️ <b>Карта:</b> {match_data.get('map', 'N/A')}
🎮 <b>Режим:</b> {match_data.get('mode', 'N/A')}

<b>📊 ОСНОВНАЯ СТАТИСТИКА:</b>
<code>
Убийства: {player_stats.get('kills', 0):<2} | Помощи: {player_stats.get('assists', 0):<2} | Урон: {player_stats.get('damage_dealt', 0):<6}
Хедшоты: {player_stats.get('headshot_kills', 0):<2} | Самый дальний килл: {player_stats.get('longest_kill', 0):<6.1f}м
Время выживания: {player_stats.get('survival_time', 0):<6.1f} мин | K/D: {player_stats.get('kd_ratio', 0):<5.2f}
Walk Distance: {player_stats.get('walk_distance', 0):<6.0f}м | Drive Distance: {player_stats.get('drive_distance', 0):<6.0f}м
Вылечено: {player_stats.get('heals_used', 0):<3} | Бустов: {player_stats.get('boosts_used', 0):<3}
</code>

<b>🎯 БОЕВАЯ ЭФФЕКТИВНОСТЬ:</b>
<code>
Процент хедшотов: {player_stats.get('headshot_percentage', 0):<5.1f}%
Точность: {player_stats.get('accuracy', 0):<5.1f}%
Выстрелов: {player_stats.get('shots_fired', 0):<5} | Попаданий: {player_stats.get('shots_hit', 0):<5}
Урон за матч: {player_stats.get('damage_per_match', 0):<5.0f}
Урон в минуту: {player_stats.get('damage_per_minute', 0):<5.0f}
Килы гранатами: {player_stats.get('grenade_kills', 0):<2} | Мили килы: {player_stats.get('melee_kills', 0):<2}
Килы транспортом: {player_stats.get('vehicle_kills', 0):<2}
</code>

<b>❤️ ВЫЖИВАНИЕ:</b>
<code>
Среднее время выживания: {player_stats.get('avg_survival_time', 0):<5.1f} мин
Оценка выживания: {player_stats.get('survival_score', 0):<5}
Время до первого килла: {player_stats.get('time_before_first_kill', 0):<5.1f} сек
Время до первого урона: {player_stats.get('time_before_first_damage', 0):<5.1f} сек
Время в безопасной зоне: {player_stats.get('safe_zone_time', 0):<5.1f}%
Время в красной зоне: {player_stats.get('red_zone_time', 0):<5.1f}%
Урон от синей зоны: {player_stats.get('blue_zone_damage', 0):<5}
Урон от падения: {player_stats.get('fall_damage', 0):<5} | Утоплений: {player_stats.get('drown_damage', 0):<5}
</code>

<b>🚶 ПЕРЕМЕЩЕНИЕ И ПОЗИЦИОНИРОВАНИЕ:</b>
<code>
Всего пройдено: {player_stats.get('total_distance', 0):<7.0f}м
Использование транспорта: {player_stats.get('vehicle_usage', 0):<5.1f}%
Использование лодок: {player_stats.get('boat_usage', 0):<5.1f}%
Использование дельтапланов: {player_stats.get('glider_usage', 0):<5.1f}%
Смена позиций: {player_stats.get('position_changes', 0):<3} | Ротаций: {player_stats.get('rotations', 0):<3}
Использование возвышенностей: {player_stats.get('high_ground_usage', 0):<5.1f}%
Использование укрытий: {player_stats.get('cover_usage', 0):<5.1f}%
Время в зданиях: {player_stats.get('building_time', 0):<5.1f}%
</code>

<b>📍 ТОЧКИ ДРОПА:</b>
"""
        
        # Добавляем точки дропа
        drop_locations = player_stats.get('drop_locations', {})
        for location, count in drop_locations.items():
            text += f"<code>{location:<15}: {count:<3} раз</code>\n"
        
        text += f"\n<b>🎯 СТАТИСТИКА ПО ОРУЖИЮ:</b>\n"
        
        # Добавляем статистику по оружию
        for weapon, stats in player_stats.get('weapon_stats', {}).items():
            text += f"<code>{weapon.upper():<10} | Килов: {stats.get('kills', 0):<3} | HS: {stats.get('headshots', 0):<3} | Точность: {stats.get('accuracy', 0):<5.1f}% | Урон: {stats.get('damage', 0):<6}</code>\n"
        
        text += f"\n<b>📈 СРЕДНИЕ ПОКАЗАТЕЛИ:</b>\n"
        text += f"<code>Средние убийства: {match_data.get('avg_kills', 0):.1f} | Средний урон: {match_data.get('avg_damage', 0):.0f}</code>\n"
        text += f"<code>Среднее время выживания: {match_data.get('avg_survival_time', 0):.1f} мин | Win Rate: {match_data.get('win_rate', 0):.1f}%</code>"
        
        return text
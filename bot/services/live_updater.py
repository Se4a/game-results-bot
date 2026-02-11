import asyncio
from datetime import datetime, timedelta
from typing import Dict, List
import logging
from bot.database import async_session
from sqlalchemy import select, and_
from bot.models.match import Match, MatchUpdate
from services.extended_stats_collector import ExtendedStatsCollector

logger = logging.getLogger(__name__)

class LiveMatchUpdater:
    """Обновление live-матчей с минимальными интервалами"""
    
    def __init__(self, bot):
        self.bot = bot
        self.stats_collector = ExtendedStatsCollector()
        self.active_tasks = {}
        self.update_intervals = {
            'csgo': 60,      # Каждую минуту
            'dota2': 30,     # Каждые 30 секунд
            'valorant': 45,  # Каждые 45 секунд
            'lol': 60,       # Каждую минуту
            'wot': 20,       # Каждые 20 секунд
            'pubg': 120      # Каждые 2 минуты
        }
    
    async def start_tracking(self, user_id: int, game: str, match_id: str, account_id: str, region: str = None):
        """Начать отслеживание матча"""
        task_key = f"{user_id}_{game}_{match_id}"
        
        if task_key in self.active_tasks:
            # Уже отслеживается
            return
        
        # Создаем задачу обновления
        task = asyncio.create_task(
            self._track_match(user_id, game, match_id, account_id, region)
        )
        self.active_tasks[task_key] = task
    
    async def stop_tracking(self, user_id: int, game: str, match_id: str):
        """Остановить отслеживание матча"""
        task_key = f"{user_id}_{game}_{match_id}"
        task = self.active_tasks.get(task_key)
        
        if task:
            task.cancel()
            del self.active_tasks[task_key]
    
    async def _track_match(self, user_id: int, game: str, match_id: str, account_id: str, region: str = None):
        """Отслеживание матча с обновлениями"""
        interval = self.update_intervals.get(game, 60)
        
        while True:
            try:
                # Получаем live-обновления
                live_data = await self.stats_collector.get_live_match_updates(game, match_id, region)
                
                if live_data:
                    # Сохраняем обновление в базу
                    await self._save_match_update(user_id, game, match_id, live_data)
                    
                    # Отправляем обновление пользователю
                    await self._send_update_to_user(user_id, game, live_data)
                
                # Ждем перед следующим обновлением
                await asyncio.sleep(interval)
                
            except asyncio.CancelledError:
                # Задача отменена
                break
            except Exception as e:
                logger.error(f"Error tracking match {match_id}: {e}")
                await asyncio.sleep(interval)
    
    async def _save_match_update(self, user_id: int, game: str, match_id: str, data: Dict):
        """Сохранить обновление матча в базу"""
        async with async_session() as session:
            # Находим матч
            result = await session.execute(
                select(Match).where(
                    and_(
                        Match.user_id == user_id,
                        Match.game == game,
                        Match.match_id == match_id,
                        Match.is_completed == False
                    )
                )
            )
            match = result.scalar_one_or_none()
            
            if match:
                # Создаем запись об обновлении
                update = MatchUpdate(
                    match_id=match.id,
                    update_time=datetime.now(),
                    stats=data
                )
                session.add(update)
                await session.commit()
    
    async def _send_update_to_user(self, user_id: int, game: str, data: Dict):
        """Отправить обновление пользователю"""
        try:
            # Форматируем обновление
            update_text = self._format_live_update(game, data)
            
            # Отправляем сообщение
            await self.bot.send_message(
                chat_id=user_id,
                text=update_text,
                parse_mode='HTML'
            )
            
        except Exception as e:
            logger.error(f"Error sending update to user {user_id}: {e}")
    
    def _format_live_update(self, game: str, data: Dict) -> str:
        """Форматировать live-обновление"""
        
        if game == 'csgo':
            return self._format_csgo_live_update(data)
        elif game == 'dota2':
            return self._format_dota_live_update(data)
        elif game == 'valorant':
            return self._format_valorant_live_update(data)
        elif game == 'lol':
            return self._format_lol_live_update(data)
        elif game == 'wot':
            return self._format_wot_live_update(data)
        elif game == 'pubg':
            return self._format_pubg_live_update(data)
        
        return "🔄 Обновление статистики..."
    
    def _format_csgo_live_update(self, data: Dict) -> str:
        """Формат live-обновления CS:GO"""
        score = data.get('score', {})
        round_num = data.get('round', 0)
        
        text = f"""
🎮 <b>CS:GO LIVE UPDATE</b>
📊 Раунд: {round_num}/30
🏆 Счет: {score.get('team1', 0)} - {score.get('team2', 0)}
⏱️ Время: {data.get('time_remaining', 0)} сек

<b>Текущая статистика:</b>
• Экономика: ${data.get('economy', 0)}
• Убийства: {data.get('kills', 0)}
• Смерти: {data.get('deaths', 0)}
• ADR: {data.get('adr', 0)}
• HS%: {data.get('hs_percentage', 0):.1f}%
"""
        return text
    
    def _format_dota_live_update(self, data: Dict) -> str:
        """Формат live-обновления Dota 2"""
        text = f"""
⚔️ <b>Dota 2 LIVE UPDATE</b>
🏆 Счет: {data.get('radiant_score', 0)} - {data.get('dire_score', 0)}
⏱️ Время: {data.get('game_time', 0)} мин
🏰 Башни: ⚡ {data.get('radiant_tower_state', 0)} | 👿 {data.get('dire_tower_state', 0)}

<b>Ваша статистика:</b>
• K/D/A: {data.get('kills', 0)}/{data.get('deaths', 0)}/{data.get('assists', 0)}
• GPM: {data.get('gold_per_min', 0)}
• XPM: {data.get('xp_per_min', 0)}
• Net Worth: {data.get('net_worth', 0):,}
"""
        return text
    
    def _format_valorant_live_update(self, data: Dict) -> str:
        """Формат live-обновления Valorant"""
        text = f"""
🔫 <b>Valorant LIVE UPDATE</b>
🎮 Раунд: {data.get('round', 0)}/25
🏆 Счет: {data.get('team1_score', 0)} - {data.get('team2_score', 0)}

<b>Ваша статистика:</b>
• Убийства: {data.get('kills', 0)}
• Смерти: {data.get('deaths', 0)}
• ACS: {data.get('acs', 0)}
• Экономика: {data.get('credits', 0)} кредитов
"""
        return text
    
    def _format_lol_live_update(self, data: Dict) -> str:
        """Формат live-обновления LoL"""
        text = f"""
🏆 <b>LoL LIVE UPDATE</b>
🏆 Счет: {data.get('team1_kills', 0)} - {data.get('team2_kills', 0)}
⏱️ Время: {data.get('game_time', 0)} мин
🏰 Башни: {data.get('team1_turrets', 0)} - {data.get('team2_turrets', 0)}

<b>Ваша статистика:</b>
• K/D/A: {data.get('kills', 0)}/{data.get('deaths', 0)}/{data.get('assists', 0)}
• CS: {data.get('cs', 0)} ({data.get('cs_per_min', 0):.1f}/мин)
• Золото: {data.get('gold', 0):,}
• Уровень: {data.get('level', 0)}
"""
        return text
    
    def _format_wot_live_update(self, data: Dict) -> str:
        """Формат live-обновления WoT"""
        text = f"""
🎖️ <b>WoT LIVE UPDATE</b>
⚔️ Уничтожено: {data.get('kills', 0)}
🎯 Урон: {data.get('damage_dealt', 0)}
🛡️ Заблокировано: {data.get('damage_blocked', 0)}
👁️ Обнаружено: {data.get('spotted', 0)}

<b>Текущий бой:</b>
• Оставшееся время: {data.get('time_remaining', 0)} сек
• Очки команды: {data.get('team_score', 0)}
• Ваш танк: {data.get('tank', 'N/A')}
"""
        return text
    
    def _format_pubg_live_update(self, data: Dict) -> str:
        """Формат live-обновления PUBG"""
        text = f"""
🌍 <b>PUBG LIVE UPDATE</b>
🥇 Место: #{data.get('rank', 0)}/{data.get('total_players', 100)}
⚔️ Убийства: {data.get('kills', 0)}
🎯 Урон: {data.get('damage_dealt', 0)}
❤️ Выживших: {data.get('players_alive', 0)}
⏱️ Время: {data.get('time_survived', 0):.1f} мин

<b>Зона:</b>
• Текущая: {data.get('current_zone', 'N/A')}
• Следующая через: {data.get('next_zone_time', 0)} сек
"""
        return text
    
    async def cleanup(self):
        """Очистка ресурсов"""
        # Отменяем все задачи
        for task in self.active_tasks.values():
            task.cancel()
        
        # Ожидаем завершения задач
        if self.active_tasks:
            await asyncio.gather(*self.active_tasks.values(), return_exceptions=True)
        
        # Закрываем коллектор
        await self.stats_collector.close()
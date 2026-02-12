try:
    import openai
    OPENAI_AVAILABLE = True
except ImportError:
    openai = None
    OPENAI_AVAILABLE = False
import json
from typing import List, Dict, Optional
from datetime import datetime
from bot.config import config
from bot.database import async_session
from sqlalchemy import select

class AIAnalyzer:
    def __init__(self):
        self.api_key = config.OPENAI_API_KEY
        self.openai_client = openai.AsyncOpenAI(api_key=self.api_key) if self.api_key else None
        self.analysis_cache = {}  # Кэш для анализа
    
    async def analyze_player_performance(
        self, 
        game: str, 
        player_stats: List[Dict], 
        language: str = 'en'
    ) -> Optional[str]:
        """
        Анализирует производительность игрока и дает рекомендации
        
        Args:
            game: Название игры
            player_stats: Статистика последних матчей
            language: Язык ответа
        
        Returns:
            Текст анализа или None если AI недоступен
        """
        
        if not self.openai_client or len(player_stats) < 3:
            return None
        
        try:
            # Подготавливаем промпт в зависимости от игры
            system_prompt, user_prompt = self._prepare_prompts(game, player_stats, language)
            
            response = await self.openai_client.chat.completions.create(
                model="gpt-4-turbo-preview",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                max_tokens=1000,
                temperature=0.7
            )
            
            analysis = response.choices[0].message.content
            
            # Кэшируем анализ
            cache_key = f"ai_analysis:{game}:{hash(str(player_stats))}"
            self.analysis_cache[cache_key] = {
                'analysis': analysis,
                'timestamp': datetime.now().timestamp()
            }
            
            return analysis
            
        except Exception as e:
            print(f"AI Analysis Error: {e}")
            return None
    
    def _prepare_prompts(self, game: str, player_stats: List[Dict], language: str):
        """Подготовка промптов для разных игр"""
        
        language_names = {
            'ru': 'русском',
            'en': 'English',
            'uk': 'українській',
            'de': 'Deutsch',
            'fr': 'français',
            'it': 'italiano',
            'pl': 'polski',
            'nl': 'Nederlands',
            'zh': '中文',
            'ko': '한국어',
            'pt': 'português',
            'es': 'español'
        }
        
        lang_name = language_names.get(language, 'English')
        
        system_prompt = f"""Ты профессиональный киберспортивный аналитик. 
        Анализируй статистику игрока и давай конкретные, полезные советы для улучшения.
        Отвечай на {lang_name} языке. Будь конструктивным и конкретным."""
        
        # Формируем статистику для анализа
        stats_summary = self._format_stats_for_ai(game, player_stats)
        
        user_prompt = f"""Проанализируй игровую статистику и дай рекомендации:

Игра: {game.upper()}
Статистика последних {len(player_stats)} матчей:
{stats_summary}

Проанализируй:
1. Сильные стороны игрока
2. Слабые места, которые нужно улучшить
3. Конкретные советы для следующих матчей
4. Рекомендации по тренировкам
5. Анализ прогресса/регресса

Отвечай структурированно, используй маркеры и будь конкретен."""
        
        return system_prompt, user_prompt
    
    def _format_stats_for_ai(self, game: str, player_stats: List[Dict]) -> str:
        """Форматирует статистику для AI анализа"""
        
        if game == 'csgo':
            return self._format_csgo_stats(player_stats)
        elif game == 'dota2':
            return self._format_dota_stats(player_stats)
        elif game == 'valorant':
            return self._format_valorant_stats(player_stats)
        elif game == 'lol':
            return self._format_lol_stats(player_stats)
        elif game == 'wot':
            return self._format_wot_stats(player_stats)
        elif game == 'pubg':
            return self._format_pubg_stats(player_stats)
        else:
            return str(player_stats)
    
    def _format_csgo_stats(self, stats: List[Dict]) -> str:
        formatted = []
        for i, match in enumerate(stats, 1):
            formatted.append(f"""
Матч {i}:
- Результат: {match.get('result', 'N/A')}
- Убийства: {match.get('kills', 0)}
- Смерти: {match.get('deaths', 0)}
- Помощи: {match.get('assists', 0)}
- K/D: {match.get('kd_ratio', 0):.2f}
- ADR: {match.get('adr', 0)}
- HS%: {match.get('hs_percentage', 0):.1f}%
- MVP: {match.get('mvp', 0)}
            """)
        return "\n".join(formatted)
    
    def _format_dota_stats(self, stats: List[Dict]) -> str:
        formatted = []
        for i, match in enumerate(stats, 1):
            formatted.append(f"""
Матч {i}:
- Герой: {match.get('hero', 'N/A')}
- Результат: {match.get('result', 'N/A')}
- Убийства/Смерти/Помощи: {match.get('kills', 0)}/{match.get('deaths', 0)}/{match.get('assists', 0)}
- KDA: {match.get('kda', 0):.2f}
- GPM: {match.get('gpm', 0)}
- XPM: {match.get('xpm', 0)}
- Урон по героям: {match.get('hero_damage', 0)}
- Урон по башням: {match.get('tower_damage', 0)}
- Последние удары: {match.get('last_hits', 0)}
            """)
        return "\n".join(formatted)
    
    def _format_valorant_stats(self, stats: List[Dict]) -> str:
        formatted = []
        for i, match in enumerate(stats, 1):
            formatted.append(f"""
Матч {i}:
- Агент: {match.get('agent', 'N/A')}
- Результат: {match.get('result', 'N/A')}
- Убийства/Смерти/Помощи: {match.get('kills', 0)}/{match.get('deaths', 0)}/{match.get('assists', 0)}
- ACS: {match.get('acs', 0)}
- HS%: {match.get('hs_percentage', 0):.1f}%
- Первая кровь: {match.get('first_bloods', 0)}
- Экономика: {match.get('economy_rating', 0)}
            """)
        return "\n".join(formatted)
    
    def _format_lol_stats(self, stats: List[Dict]) -> str:
        formatted = []
        for i, match in enumerate(stats, 1):
            formatted.append(f"""
Матч {i}:
- Чемпион: {match.get('champion', 'N/A')}
- Результат: {match.get('result', 'N/A')}
- Убийства/Смерти/Помощи: {match.get('kills', 0)}/{match.get('deaths', 0)}/{match.get('assists', 0)}
- KDA: {match.get('kda', 0):.2f}
- CS: {match.get('cs', 0)} ({match.get('cs_per_min', 0):.1f}/мин)
- Золото: {match.get('gold', 0)}
- Очки зрения: {match.get('vision_score', 0)}
- Урон: {match.get('damage', 0)}
            """)
        return "\n".join(formatted)
    
    def _format_wot_stats(self, stats: List[Dict]) -> str:
        formatted = []
        for i, match in enumerate(stats, 1):
            formatted.append(f"""
Бой {i}:
- Танк: {match.get('tank', 'N/A')}
- Результат: {match.get('result', 'N/A')}
- Урон: {match.get('damage', 0)}
- Урон по разведке: {match.get('assisted_damage', 0)}
- Заблокировано урона: {match.get('blocked_damage', 0)}
- Уничтожено: {match.get('kills', 0)}
- Обнаружено: {match.get('spotted', 0)}
- WN8: {match.get('wn8', 0)}
- XP: {match.get('xp', 0)}
            """)
        return "\n".join(formatted)
    
    def _format_pubg_stats(self, stats: List[Dict]) -> str:
        formatted = []
        for i, match in enumerate(stats, 1):
            formatted.append(f"""
Матч {i}:
- Место: #{match.get('rank', 0)}
- Убийства: {match.get('kills', 0)}
- Помощи: {match.get('assists', 0)}
- Урон: {match.get('damage', 0)}
- Убийства в голову: {match.get('headshot_kills', 0)}
- Самый дальний килл: {match.get('longest_kill', 0):.1f}м
- Время выживания: {match.get('survival_time', 0):.1f} мин
            """)
        return "\n".join(formatted)
    
    async def get_cached_analysis(self, cache_key: str) -> Optional[str]:
        """Получить кэшированный анализ"""
        cached = self.analysis_cache.get(cache_key)
        if cached and (datetime.now().timestamp() - cached['timestamp']) < 3600:  # 1 час
            return cached['analysis']
        return None

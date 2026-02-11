from datetime import datetime
from typing import Dict, List

class StatsProcessor:
    @staticmethod
    def calculate_kda(kills: int, deaths: int, assists: int) -> float:
        if deaths == 0:
            return kills + assists
        return (kills + assists) / deaths
    
    @staticmethod
    def calculate_win_rate(wins: int, total: int) -> float:
        if total == 0:
            return 0.0
        return (wins / total) * 100
    
    @staticmethod
    def format_match_table(match_data: Dict, players: List[Dict]) -> str:
        """Format match data into a text table"""
        table = "Player | Kills | Assists | Deaths | K/D | ADR\n"
        table += "-" * 50 + "\n"
        
        for player in players:
            table += f"{player.get('name', 'Unknown'):<15} | "
            table += f"{player.get('kills', 0):<5} | "
            table += f"{player.get('assists', 0):<7} | "
            table += f"{player.get('deaths', 0):<6} | "
            table += f"{player.get('kd', 0):<4.1f} | "
            table += f"{player.get('adr', 0):<4}\n"
        
        return table
    
    @staticmethod
    def compare_with_history(current_stats: Dict, history_stats: List[Dict]) -> Dict:
        """Compare current match stats with historical data"""
        if not history_stats:
            return {}
        
        avg_kills = sum(m.get('kills', 0) for m in history_stats) / len(history_stats)
        avg_deaths = sum(m.get('deaths', 0) for m in history_stats) / len(history_stats)
        avg_assists = sum(m.get('assists', 0) for m in history_stats) / len(history_stats)
        avg_adr = sum(m.get('adr', 0) for m in history_stats) / len(history_stats)
        
        comparison = {
            'kills': {
                'current': current_stats.get('kills', 0),
                'average': avg_kills,
                'difference': current_stats.get('kills', 0) - avg_kills
            },
            'adr': {
                'current': current_stats.get('adr', 0),
                'average': avg_adr,
                'difference': current_stats.get('adr', 0) - avg_adr
            }
        }
        
        return comparison
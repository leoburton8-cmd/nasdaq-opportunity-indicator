#!/usr/bin/env python3
"""
NASDAQ Opportunity Indicator
=============================
Real-time momentum indicator tracking big opportunities and optimal entry points.
Uses live market data to generate actionable trading signals.

Author: leoburton8-cmd
Repository: https://github.com/leoburton8-cmd/nasdaq-opportunity-indicator
"""

import requests
import json
from datetime import datetime
from typing import List, Dict, Tuple
import csv


class NASDAQIndicator:
    """
    Real-time NASDAQ opportunity indicator
    Tracks momentum, volume surges, and optimal entry points
    """
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.perplexity.ai"
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        # Key NASDAQ components to track
        self.tickers = [
            'QQQ',    # NASDAQ 100 ETF
            'AAPL',   # Apple
            'MSFT',   # Microsoft
            'NVDA',   # NVIDIA
            'GOOGL',  # Alphabet
            'META',   # Meta
            'TSLA',   # Tesla
            'AMZN',   # Amazon
            'AMD',    # AMD
            'NDX'     # NASDAQ 100 Index
        ]
        
        self.signals = []
    
    def fetch_quotes(self, tickers: List[str]) -> List[Dict]:
        """Fetch real-time quotes for tickers"""
        try:
            url = f"{self.base_url}/finance/quotes"
            payload = {
                "ticker_symbols": tickers,
                "fields": ["price", "changesPercentage", "volume", "marketCap", 
                          "dayLow", "dayHigh", "yearLow", "yearHigh", 
                          "previousClose", "open", "avgVolume"]
            }
            
            response = requests.post(url, headers=self.headers, json=payload, timeout=15)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Error fetching quotes: {e}")
            return []
    
    def calculate_momentum_score(self, quote: Dict) -> float:
        """
        Calculate momentum score (0-100) based on:
        - Price position within day's range
        - Price position within 52-week range
        - Daily percentage change
        - Volume vs average
        """
        score = 50.0  # Base score
        
        price = quote.get('price', 0)
        day_low = quote.get('dayLow', price)
        day_high = quote.get('dayHigh', price)
        year_low = quote.get('yearLow', price)
        year_high = quote.get('yearHigh', price)
        change_pct = quote.get('changesPercentage', 0)
        volume = quote.get('volume', 0)
        avg_volume = quote.get('avgVolume', volume)
        
        # Day range position (0-100, where 100 = at high)
        if day_high > day_low:
            day_position = ((price - day_low) / (day_high - day_low)) * 100
            score += (day_position - 50) * 0.3  # ±15 points
        
        # Year range position
        if year_high > year_low:
            year_position = ((price - year_low) / (year_high - year_low)) * 100
            score += (year_position - 50) * 0.2  # ±10 points
        
        # Daily change momentum
        score += min(change_pct * 3, 20)  # Cap at +20
        
        # Volume surge
        if avg_volume > 0 and volume > avg_volume:
            volume_ratio = volume / avg_volume
            if volume_ratio > 2.0:
                score += 10
            elif volume_ratio > 1.5:
                score += 5
        
        return min(max(score, 0), 100)
    
    def detect_entry_zone(self, quote: Dict) -> Dict:
        """Calculate optimal entry zones based on support/resistance"""
        
        price = quote.get('price', 0)
        day_low = quote.get('dayLow', price)
        day_high = quote.get('dayHigh', price)
        prev_close = quote.get('previousClose', price)
        
        # Support levels
        support_1 = day_low
        support_2 = prev_close * 0.98  # 2% below previous close
        support_3 = price * 0.95  # 5% pullback
        
        # Resistance levels
        resistance_1 = day_high
        resistance_2 = prev_close * 1.02  # 2% above previous close
        resistance_3 = price * 1.05  # 5% breakout
        
        # Optimal entry zone (buy zone)
        entry_zone_low = support_1 * 0.995  # Just below day low
        entry_zone_high = support_2 * 1.005
        
        # Stop loss
        stop_loss = support_3 * 0.99
        
        # Take profit targets
        tp1 = resistance_2 * 1.01
        tp2 = resistance_3 * 1.02
        tp3 = price * 1.10
        
        return {
            'current_price': price,
            'entry_zone': f"${entry_zone_low:.2f} - ${entry_zone_high:.2f}",
            'stop_loss': f"${stop_loss:.2f}",
            'take_profit_1': f"${tp1:.2f}",
            'take_profit_2': f"${tp2:.2f}",
            'take_profit_3': f"${tp3:.2f}",
            'support_levels': [f"${support_1:.2f}", f"${support_2:.2f}", f"${support_3:.2f}"],
            'resistance_levels': [f"${resistance_1:.2f}", f"${resistance_2:.2f}", f"${resistance_3:.2f}"],
            'risk_reward_ratio': round((tp2 - price) / (price - stop_loss), 2) if price > stop_loss else 0
        }
    
    def generate_signal(self, quote: Dict) -> Dict:
        """Generate trading signal for a ticker"""
        
        ticker = quote.get('symbol', 'UNKNOWN')
        price = quote.get('price', 0)
        change_pct = quote.get('changesPercentage', 0)
        volume = quote.get('volume', 0)
        avg_volume = quote.get('avgVolume', 1)
        
        # Calculate scores
        momentum_score = self.calculate_momentum_score(quote)
        entry_data = self.detect_entry_zone(quote)
        
        # Determine signal type
        if momentum_score >= 75:
            signal_type = "STRONG BUY"
            signal_color = "🟢"
        elif momentum_score >= 60:
            signal_type = "BUY"
            signal_color = "🟡"
        elif momentum_score >= 40:
            signal_type = "HOLD"
            signal_color = "⚪"
        elif momentum_score >= 25:
            signal_type = "SELL"
            signal_color = "🟠"
        else:
            signal_type = "STRONG SELL"
            signal_color = "🔴"
        
        # Volume analysis
        volume_ratio = volume / avg_volume if avg_volume > 0 else 1
        volume_status = "SURGE" if volume_ratio > 2.0 else "ELEVATED" if volume_ratio > 1.5 else "NORMAL"
        
        return {
            'ticker': ticker,
            'timestamp': datetime.now().isoformat(),
            'signal_type': signal_type,
            'signal_color': signal_color,
            'momentum_score': momentum_score,
            'price': price,
            'change_percent': change_pct,
            'volume': volume,
            'avg_volume': avg_volume,
            'volume_ratio': volume_ratio,
            'volume_status': volume_status,
            'entry_data': entry_data,
            'opportunity_rating': self._rate_opportunity(momentum_score, change_pct, volume_ratio)
        }
    
    def _rate_opportunity(self, momentum: float, change: float, volume_ratio: float) -> str:
        """Rate overall opportunity quality"""
        
        score = momentum + min(change * 2, 20) + (10 if volume_ratio > 2 else 0)
        
        if score >= 90:
            return "🔥 EXCEPTIONAL"
        elif score >= 75:
            return "⭐ HIGH"
        elif score >= 60:
            return "📊 MODERATE"
        else:
            return "⚠️ LOW"
    
    def scan_market(self) -> List[Dict]:
        """Scan all tracked tickers and generate signals"""
        
        print(f"\n🔍 NASDAQ Opportunity Indicator")
        print(f"{'='*70}")
        print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"\nScanning {len(self.tickers)} NASDAQ components...\n")
        
        quotes = self.fetch_quotes(self.tickers)
        
        if not quotes:
            print("❌ No data received. Check API key and try again.")
            return []
        
        signals = []
        for quote in quotes:
            signal = self.generate_signal(quote)
            signals.append(signal)
            
            # Print summary
            print(f"{signal['signal_color']} {signal['ticker']:6} | Score: {signal['momentum_score']:5.1f} | "
                  f"Price: ${signal['price']:8.2f} | Change: {signal['change_percent']:6.2f}% | "
                  f"Vol: {signal['volume_status']:8} | Signal: {signal['signal_type']}")
        
        self.signals = signals
        return signals
    
    def get_top_opportunities(self, limit: int = 5) -> List[Dict]:
        """Get top scoring opportunities"""
        
        if not self.signals:
            return []
        
        # Sort by momentum score descending
        sorted_signals = sorted(self.signals, key=lambda x: x['momentum_score'], reverse=True)
        
        return sorted_signals[:limit]
    
    def display_dashboard(self):
        """Display full indicator dashboard"""
        
        if not self.signals:
            print("No signals available. Run scan_market() first.")
            return
        
        print(f"\n{'='*70}")
        print("📊 NASDAQ OPPORTUNITY DASHBOARD")
        print(f"{'='*70}\n")
        
        # Top opportunities
        top = self.get_top_opportunities(5)
        
        print("🎯 TOP 5 OPPORTUNITIES\n")
        print(f"{'Rank':<5} {'Ticker':<8} {'Score':<8} {'Price':<12} {'Change':<10} {'Signal':<15} {'Rating'}")
        print("-" * 70)
        
        for i, signal in enumerate(top, 1):
            print(f"{i:<5} {signal['ticker']:<8} {signal['momentum_score']:<8.1f} "
                  f"${signal['price']:<11.2f} {signal['change_percent']:<9.2f}% "
                  f"{signal['signal_type']:<15} {signal['opportunity_rating']}")
        
        print(f"\n{'='*70}")
        print("📈 DETAILED ANALYSIS - TOP PICK\n")
        
        if top:
            best = top[0]
            print(f"Ticker: {best['ticker']}")
            print(f"Signal: {best['signal_color']} {best['signal_type']}")
            print(f"Momentum Score: {best['momentum_score']:.1f}/100")
            print(f"Opportunity: {best['opportunity_rating']}")
            print(f"\nCurrent Price: ${best['price']:.2f}")
            print(f"Daily Change: {best['change_percent']:.2f}%")
            print(f"Volume: {best['volume']:,} ({best['volume_status']})")
            
            entry = best['entry_data']
            print(f"\n🎯 ENTRY STRATEGY:")
            print(f"  Entry Zone: {entry['entry_zone']}")
            print(f"  Stop Loss: {entry['stop_loss']}")
            print(f"  Take Profit 1: {entry['take_profit_1']}")
            print(f"  Take Profit 2: {entry['take_profit_2']}")
            print(f"  Take Profit 3: {entry['take_profit_3']}")
            print(f"  Risk/Reward: {entry['risk_reward_ratio']}:1")
            
            print(f"\n📊 KEY LEVELS:")
            print(f"  Support: {', '.join(entry['support_levels'])}")
            print(f"  Resistance: {', '.join(entry['resistance_levels'])}")
        
        print(f"\n{'='*70}")
    
    def export_signals(self, filename: str = "nasdaq_signals.csv"):
        """Export signals to CSV"""
        
        if not self.signals:
            print("No signals to export")
            return
        
        with open(filename, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([
                'Ticker', 'Signal', 'Momentum Score', 'Price', 'Change %',
                'Volume', 'Volume Status', 'Opportunity Rating',
                'Entry Zone', 'Stop Loss', 'Take Profit 1', 'Risk/Reward'
            ])
            
            for signal in self.signals:
                entry = signal['entry_data']
                writer.writerow([
                    signal['ticker'],
                    signal['signal_type'],
                    f"{signal['momentum_score']:.1f}",
                    signal['price'],
                    signal['change_percent'],
                    signal['volume'],
                    signal['volume_status'],
                    signal['opportunity_rating'],
                    entry['entry_zone'],
                    entry['stop_loss'],
                    entry['take_profit_1'],
                    entry['risk_reward_ratio']
                ])
        
        print(f"\n✓ Exported {len(self.signals)} signals to {filename}")


def main():
    """Main execution"""
    
    # Initialize with API key
    API_KEY = "YOUR_PERPLEXITY_API_KEY_HERE"  # ← Replace with your key
    
    indicator = NASDAQIndicator(API_KEY)
    
    # Scan market
    indicator.scan_market()
    
    # Display dashboard
    indicator.display_dashboard()
    
    # Export results
    indicator.export_signals()


if __name__ == "__main__":
    main()

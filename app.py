#!/usr/bin/env python3
"""
NASDAQ Opportunity Indicator - Real-Time Web App
================================================
Live dashboard with auto-refresh every 10 seconds.
Deploy on Streamlit Cloud for free: https://streamlit.io/cloud

Run locally: streamlit run app.py
"""

import streamlit as st
import requests
import pandas as pd
from datetime import datetime
import time
import json

# Page config
st.set_page_config(
    page_title="📊 NASDAQ Opportunity Indicator",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 10px;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        margin-bottom: 30px;
    }
    .metric-card {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        border-radius: 15px;
        padding: 25px;
        margin: 10px 0;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    .signal-badge {
        display: inline-block;
        padding: 8px 16px;
        border-radius: 8px;
        font-weight: bold;
        font-size: 14px;
        margin: 10px 0;
    }
    .strong-buy { background: #28a745; color: white; }
    .buy { background: #28a745; color: white; }
    .hold { background: #6c757d; color: white; }
    .sell { background: #fd7e14; color: white; }
    .strong-sell { background: #dc3545; color: white; }
    .opportunity-exceptional { color: #dc3545; font-weight: bold; }
    .opportunity-high { color: #fd7e14; font-weight: bold; }
    .opportunity-moderate { color: #ffc107; font-weight: bold; }
    .opportunity-low { color: #6c757d; font-weight: bold; }
    .refresh-timer {
        position: fixed;
        bottom: 20px;
        right: 20px;
        background: #667eea;
        color: white;
        padding: 10px 20px;
        border-radius: 30px;
        font-weight: bold;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }
</style>
""", unsafe_allow_html=True)


class NASDAQIndicator:
    """Real-time NASDAQ indicator engine"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.perplexity.ai"
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        self.tickers = ['QQQ', 'AAPL', 'MSFT', 'NVDA', 'GOOGL', 'META', 'TSLA', 'AMZN', 'AMD']
    
    def fetch_quotes(self):
        """Fetch real-time quotes"""
        try:
            url = f"{self.base_url}/finance/quotes"
            payload = {
                "ticker_symbols": self.tickers,
                "fields": ["price", "changesPercentage", "volume", "marketCap", 
                          "dayLow", "dayHigh", "yearLow", "yearHigh", "previousClose"]
            }
            
            response = requests.post(url, headers=self.headers, json=payload, timeout=15)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            st.error(f"Error fetching data: {e}")
            return []
    
    def calculate_momentum_score(self, quote):
        """Calculate 0-100 momentum score"""
        score = 50.0
        
        price = quote.get('price', 0)
        day_low = quote.get('dayLow', price)
        day_high = quote.get('dayHigh', price)
        year_low = quote.get('yearLow', price)
        year_high = quote.get('yearHigh', price)
        change_pct = quote.get('changesPercentage', 0)
        
        # Day range position
        if day_high > day_low:
            day_position = ((price - day_low) / (day_high - day_low)) * 100
            score += (day_position - 50) * 0.3
        
        # Year range position
        if year_high > year_low:
            year_position = ((price - year_low) / (year_high - year_low)) * 100
            score += (year_position - 50) * 0.2
        
        # Daily change
        score += min(change_pct * 3, 20)
        
        return min(max(score, 0), 100)
    
    def get_signal_type(self, score):
        """Determine signal type from score"""
        if score >= 75:
            return "STRONG BUY", "strong-buy", "🟢"
        elif score >= 60:
            return "BUY", "buy", "🟢"
        elif score >= 40:
            return "HOLD", "hold", "⚪"
        elif score >= 25:
            return "SELL", "sell", "🟠"
        else:
            return "STRONG SELL", "strong-sell", "🔴"
    
    def calculate_entry_zones(self, quote):
        """Calculate entry/exit levels"""
        price = quote.get('price', 0)
        day_low = quote.get('dayLow', price)
        prev_close = quote.get('previousClose', price)
        
        entry_low = day_low * 0.995
        entry_high = prev_close * 1.005
        stop_loss = price * 0.95
        tp1 = price * 1.03
        tp2 = price * 1.05
        tp3 = price * 1.10
        
        risk = price - stop_loss
        reward = tp2 - price
        rr_ratio = round(reward / risk, 2) if risk > 0 else 0
        
        return {
            'entry': f"${entry_low:.2f} - ${entry_high:.2f}",
            'stop': f"${stop_loss:.2f}",
            'tp1': f"${tp1:.2f}",
            'tp2': f"${tp2:.2f}",
            'tp3': f"${tp3:.2f}",
            'rr': rr_ratio
        }
    
    def scan_market(self):
        """Scan all tickers and return signals"""
        quotes = self.fetch_quotes()
        
        if not quotes:
            return []
        
        signals = []
        for quote in quotes:
            ticker = quote.get('symbol', 'N/A')
            price = quote.get('price', 0)
            change = quote.get('changesPercentage', 0)
            
            score = self.calculate_momentum_score(quote)
            signal_type, signal_class, signal_icon = self.get_signal_type(score)
            entry_data = self.calculate_entry_zones(quote)
            
            # Opportunity rating
            rating_score = score + min(change * 2, 20)
            if rating_score >= 90:
                rating = "🔥 EXCEPTIONAL"
                rating_class = "opportunity-exceptional"
            elif rating_score >= 75:
                rating = "⭐ HIGH"
                rating_class = "opportunity-high"
            elif rating_score >= 60:
                rating = "📊 MODERATE"
                rating_class = "opportunity-moderate"
            else:
                rating = "⚠️ LOW"
                rating_class = "opportunity-low"
            
            signals.append({
                'ticker': ticker,
                'icon': signal_icon,
                'signal': signal_type,
                'signal_class': signal_class,
                'score': score,
                'price': price,
                'change': change,
                'rating': rating,
                'rating_class': rating_class,
                'entry': entry_data
            })
        
        # Sort by score descending
        signals.sort(key=lambda x: x['score'], reverse=True)
        return signals


def main():
    """Main app"""
    
    # Sidebar
    with st.sidebar:
        st.image("https://img.icons8.com/color/96/nasdaq.png", width=80)
        st.title("⚙️ Settings")
        
        api_key = st.text_input(
            "Perplexity API Key",
            type="password",
            help="Get your key: https://www.perplexity.ai/settings/api",
            value=st.session_state.get('api_key', '')
        )
        
        if api_key:
            st.session_state.api_key = api_key
            st.success("✓ API key saved")
        
        st.divider()
        
        refresh_rate = st.slider(
            "Auto-refresh (seconds)",
            min_value=5,
            max_value=60,
            value=10,
            step=5
        )
        
        st.divider()
        
        if st.button("🔄 Refresh Now", use_container_width=True):
            st.session_state.refresh = True
        
        st.markdown("""
        ### 📊 About
        Real-time NASDAQ momentum indicator tracking:
        - QQQ, AAPL, MSFT, NVDA
        - GOOGL, META, TSLA, AMZN, AMD
        
        Updates automatically every **10 seconds**.
        """)
    
    # Main content
    st.markdown('<h1 class="main-header">📊 NASDAQ Opportunity Indicator</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Real-time momentum signals & optimal entry points • Auto-updates every 10 seconds</p>', unsafe_allow_html=True)
    
    # Check for API key
    if 'api_key' not in st.session_state:
        st.warning("⚠️ Please enter your Perplexity API key in the sidebar to get started.")
        st.stop()
    
    # Initialize indicator
    indicator = NASDAQIndicator(st.session_state.api_key)
    
    # Get current time
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    st.caption(f"🕐 Last updated: {now}")
    
    # Scan market
    with st.spinner("🔍 Scanning market..."):
        signals = indicator.scan_market()
    
    if not signals:
        st.error("❌ No data received. Check your API key and try again.")
        st.stop()
    
    # Top opportunities
    st.subheader("🎯 Top Opportunities")
    
    # Display signals in cards
    cols = st.columns(3)
    
    for i, signal in enumerate(signals[:6]):  # Top 6
        with cols[i % 3]:
            with st.container():
                st.markdown(f"""
                <div class="metric-card">
                    <div style="font-size: 24px; font-weight: bold; margin-bottom: 5px;">
                        {signal['icon']} {signal['ticker']}
                    </div>
                    <div class="signal-badge {signal['signal_class']}">
                        {signal['signal']}
                    </div>
                    <div style="margin: 15px 0;">
                        <div style="color: #666; font-size: 14px;">Momentum Score</div>
                        <div style="font-size: 28px; font-weight: bold; color: #333;">
                            {signal['score']:.1f}/100
                        </div>
                    </div>
                    <div style="margin: 10px 0;">
                        <div style="color: #666; font-size: 14px;">Price</div>
                        <div style="font-size: 20px; font-weight: bold;">
                            ${signal['price']:.2f}
                            <span style="color: {'#28a745' if signal['change'] >= 0 else '#dc3545'}; font-size: 16px;">
                                ({signal['change']:+.2f}%)
                            </span>
                        </div>
                    </div>
                    <div style="margin: 10px 0;">
                        <div style="color: #666; font-size: 14px;">Opportunity</div>
                        <div class="{signal['rating_class']}" style="font-size: 18px;">
                            {signal['rating']}
                        </div>
                    </div>
                    <div style="margin-top: 15px; padding-top: 15px; border-top: 1px solid #ddd;">
                        <div style="color: #666; font-size: 13px; margin-bottom: 5px;">🎯 Entry: {signal['entry']['entry']}</div>
                        <div style="color: #666; font-size: 13px; margin-bottom: 5px;">🛑 Stop: {signal['entry']['stop']}</div>
                        <div style="color: #666; font-size: 13px;">📈 Target: {signal['entry']['tp2']}</div>
                        <div style="color: #666; font-size: 13px; margin-top: 8px;"><strong>R/R: {signal['entry']['rr']}:1</strong></div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
    
    # Full table
    st.divider()
    st.subheader("📊 All Signals")
    
    # Create DataFrame
    df = pd.DataFrame(signals)
    df['Price'] = df['price'].apply(lambda x: f"${x:.2f}")
    df['Change'] = df['change'].apply(lambda x: f"{x:+.2f}%")
    df['Score'] = df['score'].apply(lambda x: f"{x:.1f}")
    
    # Display table
    st.dataframe(
        df[['ticker', 'signal', 'score', 'price', 'change', 'rating']].rename(
            columns={'ticker': 'Ticker', 'signal': 'Signal', 'score': 'Score', 
                    'price': 'Price', 'change': 'Change', 'rating': 'Opportunity'}
        ),
        use_container_width=True,
        hide_index=True
    )
    
    # Export button
    csv = df.to_csv(index=False)
    st.download_button(
        label="📥 Download CSV",
        data=csv,
        file_name=f"nasdaq_signals_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
        mime="text/csv"
    )
    
    # Auto-refresh
    time.sleep(refresh_rate)
    st.rerun()


if __name__ == "__main__":
    main()

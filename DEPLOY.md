# 🚀 Deploy Your NASDAQ Indicator (FREE)

Get your **real-time web app** live in 5 minutes - completely FREE!

---

## Option 1: Streamlit Cloud (EASIEST - Recommended)

### Step 1: Go to Streamlit Cloud
**https://streamlit.io/cloud**

### Step 2: Sign Up
- Click "Start for free"
- Sign in with GitHub
- Authorize Streamlit

### Step 3: Deploy Your App
1. Click **"New app"**
2. Select your repository: `leoburton8-cmd/nasdaq-opportunity-indicator`
3. Branch: `main`
4. Main file path: `app.py`

### Step 4: Add Your API Key
1. Click on your deployed app
2. Click **"Settings"**
3. Under "Secrets", add:
```toml
[api_keys]
perplexity = "YOUR_PERPLEXITY_API_KEY_HERE"
```
4. Click **"Save"**

### Step 5: Go Live! 🎉
- Your app URL will be: `https://nasdaq-opportunity-indicator-app-xxxxxx.streamlit.app`
- **Auto-refreshes every 10 seconds**
- Access from anywhere (phone, tablet, computer)
- **100% FREE**

---

## Option 2: Run Locally

### Install
```bash
git clone https://github.com/leoburton8-cmd/nasdaq-opportunity-indicator.git
cd nasdaq-opportunity-indicator
pip install -r requirements.txt
```

### Run
```bash
streamlit run app.py
```

Opens at: `http://localhost:8501`

---

## Option 3: Render.com (Alternative Free Hosting)

### Step 1: Create Account
**https://render.com**

### Step 2: New Web Service
1. Click **"New +"** → **"Web Service"**
2. Connect GitHub
3. Select `nasdaq-opportunity-indicator`

### Step 3: Configure
- **Name:** nasdaq-indicator
- **Build Command:** `pip install -r requirements.txt`
- **Start Command:** `streamlit run app.py --server.port $PORT --server.address 0.0.0.0`

### Step 4: Environment Variables
Add:
```
PERPLEXITY_API_KEY=your_key_here
```

### Step 5: Deploy
- Click **"Create web service"**
- Wait 2-3 minutes
- Get your live URL!

---

## 🎯 Your Live App Will Have:

✅ **Real-time data** - Updates every 10 seconds  
✅ **Auto-refresh** - No manual reloading  
✅ **Mobile-friendly** - Works on phone/tablet  
✅ **Beautiful UI** - Professional dashboard  
✅ **Signal cards** - Top 6 opportunities  
✅ **Full table** - All 9 tickers  
✅ **Download CSV** - Export signals  
✅ **Free hosting** - No credit card needed  

---

## 📱 Access From Anywhere

Once deployed, you can:
- **Bookmark the URL** on your phone
- **Add to home screen** (looks like native app)
- **Access from any device**
- **Share with friends** (private link)

---

## 🔒 Security Notes

- Your API key is **encrypted** in Streamlit secrets
- App is **private by default** (only you can access)
- Can make **public** if you want to share
- **No one else** can see your API key

---

## 💡 Pro Tips

1. **Deploy on Streamlit Cloud** - easiest and most reliable
2. **Set auto-refresh to 10-15 seconds** - balance between fresh data and API calls
3. **Check during market hours** - 9:30 AM - 4:00 PM ET
4. **Best signals** appear at market open (9:30-10:30 AM ET)

---

## 🆘 Troubleshooting

**App won't load?**
- Check API key is correct
- Make sure repo is public
- Try redeploying

**No data showing?**
- Verify API key has finance access
- Check market is open (Mon-Fri 9:30-4 ET)

**Slow refresh?**
- Increase refresh interval in settings
- Free tier has rate limits

---

## 🎉 You're Done!

Your **real-time NASDAQ indicator** is now live and updating automatically!

**Access it anytime from:**
- Phone
- Tablet
- Computer
- Anywhere with internet

**Happy trading! 📈**

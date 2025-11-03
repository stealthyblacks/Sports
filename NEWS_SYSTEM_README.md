# Football News System Documentation

## 🏈 Overview
This system integrates football news into your prediction platform with AdSense-ready placements for monetization.

## 🚀 Features
- **NewsAPI Integration**: Primary source for latest football news
- **RSS Fallback**: Automatic fallback to BBC Sport, Sky Sports, and ESPN RSS feeds
- **AdSense Ready**: Strategic ad placements optimized for approval
- **Professional UI**: Clean news cards with football boots branding
- **Mobile Responsive**: Optimized for all device sizes

## 📁 File Structure
```
backend/
├── api/news.py              # News API with fallback
├── enhanced_backend.py      # Updated to include news routes

frontend/
├── pages/api/
│   ├── sports-news.ts       # Next.js API proxy
│   └── football-news.ts     # Football-specific news endpoint
├── components/
│   ├── AdSenseAd.js         # Reusable AdSense component
│   └── StickyFooterAd.js    # Sticky footer advertisement
└── pages/index.js           # Updated homepage with news section
```

## 🔧 Setup Instructions

### 1. Backend Setup
```bash
cd backend
pip install feedparser  # If not already installed
```

### 2. Environment Variables
Copy `.env.example` to `.env` and configure:
```bash
NEWS_API_KEY=your_newsapi_key_here  # Get from https://newsapi.org
BACKEND_URL=http://127.0.0.1:8001
```

### 3. Start Backend
```bash
cd backend
python enhanced_backend.py
```

### 4. Test News Endpoints
```bash
# Test news API
curl http://127.0.0.1:8001/api/v1/sports-news

# Test football-specific news
curl http://127.0.0.1:8001/api/v1/football-news

# Health check
curl http://127.0.0.1:8001/api/v1/news/health
```

### 5. Frontend Integration
The news section is automatically loaded on the homepage. Manual refresh available.

## 📱 AdSense Integration

### Current Placements
1. **Homepage News Section**: Rectangle ad above news cards
2. **Predictions Page**: Leaderboard between filters and predictions
3. **Matches Page**: Rectangle above fixtures list
4. **Sticky Footer**: Dismissible bottom ad across all pages

### AdSense Setup for Production
1. Replace `ca-pub-XXXXXX` with your AdSense publisher ID
2. Replace ad slot IDs with your actual slots
3. Set `isPlaceholder={false}` in `AdSenseAd` component
4. Add AdSense script to `_document.js`:

```javascript
<script
  async
  src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-XXXXXX"
  crossOrigin="anonymous"
></script>
```

## 🔄 Automation
Set up cron jobs for regular updates:

```bash
# Refresh news every 30 minutes
*/30 * * * * curl http://yourdomain.com/api/sports-news

# Refresh predictions daily at 6 AM
0 6 * * * curl http://yourdomain.com/api/enhanced/enhanced-predictions
```

## 🎨 Customization

### News Sources
Edit `RSS_FEEDS` in `backend/api/news.py` to add more sources:
```python
RSS_FEEDS = [
    "https://feeds.bbci.co.uk/sport/rss.xml",
    "https://www.skysports.com/rss/12040",
    "https://www.espn.com/espn/rss/news",
    "https://your-custom-feed.xml"  # Add your own
]
```

### Ad Placements
Modify ad slots and formats in components:
- `AdSenseAd.js` - Main ad component
- `StickyFooterAd.js` - Footer ad settings
- Individual pages for placement locations

## 🚨 Troubleshooting

### News Not Loading
1. Check backend is running on port 8001
2. Verify NewsAPI key is valid
3. Check RSS feeds are accessible
4. Review browser console for errors

### AdSense Issues
1. Ensure publisher ID is correct
2. Verify ad slots are created in AdSense dashboard
3. Check domain is added to AdSense account
4. Monitor AdSense policy compliance

## 📊 Performance
- News cached for 30 minutes
- Fallback to RSS if NewsAPI fails
- Lazy loading for news images
- Responsive design for all devices

## 🛡️ AdSense Compliance
- Strategic ad placement (3 per page max)
- Clear content-to-ads ratio
- Mobile-friendly responsive ads
- Proper ad labeling
- No gambling promotion
- Educational content focus
# Render Deployment Instructions

## ✅ Deployment Steps:

### 1. Connect GitHub Repository
- Go to https://render.com
- Click "New +" → "Web Service"
- Connect your GitHub account
- Select: `Skill-Exchange-Platform-for-students`
- Click "Connect"

### 2. Configure Service
- **Name**: `skill-exchange-platform` (or any name)
- **Environment**: `Python 3`
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `gunicorn app:app`
- **Free tier** is available

### 3. Add Environment Variables
- **No environment variables required!** (We switched from Zoom to Jitsi Meet)
- Optional variables:
  - `FLASK_ENV`: `production`
  - `FLASK_SECRET_KEY`: (your secret key)

### 4. Deploy
- Click "Create Web Service"
- Wait 2-5 minutes for deployment
- You'll get a live URL like: `https://skill-exchange-platform.onrender.com`

## 📝 Notes:
- Database will reset on free tier restarts (use PostgreSQL for persistence)
- First request may be slow (free tier sleeps after 15 min inactivity)
- Uses Jitsi Meet for video conferencing (no API keys required!)
- Recommend upgrading to paid tier for production use

## ⚠️ Important:
- Update `app.secret_key = "secret"` to use environment variable
- Never commit sensitive keys to GitHub
- Meetings now use Jitsi Meet (free, no API setup required!)

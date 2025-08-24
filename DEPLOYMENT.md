# Deployment Guide for Render

## 🚀 Quick Deploy on Render

### Option 1: Using render.yaml (Recommended)
1. Push your code to GitHub
2. Connect your repository to Render
3. Render will automatically detect the `render.yaml` and deploy

### Option 2: Manual Configuration
1. **Service Type**: Web Service
2. **Environment**: Python
3. **Build Command**: `pip install -r requirements.txt`
4. **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`

## 🔧 Key Configuration Changes Made

### 1. Host Binding
- **Before**: `host="127.0.0.1"` (localhost only)
- **After**: `host="0.0.0.0"` (all interfaces - required for Render)

### 2. Port Configuration
- **Before**: Fixed port `8000`
- **After**: Dynamic port using `$PORT` environment variable

### 3. Environment Variables
```bash
PORT=8000                    # Render provides this
DATABASE_URL=sqlite:///./orders.db
WEBHOOK_SECRET=render_production_secret
ENVIRONMENT=production
```

## 📁 Files Created/Modified

- ✅ `main.py` - Updated for Render compatibility
- ✅ `render.yaml` - Render deployment configuration
- ✅ `Dockerfile` - Alternative containerized deployment
- ✅ `start.sh` - Startup script
- ✅ `.dockerignore` - Docker optimization

## 🐳 Docker Deployment (Alternative)

If you prefer Docker:
1. **Build Command**: Leave empty (Render will use Dockerfile)
2. **Start Command**: Leave empty (Render will use Dockerfile CMD)

## ⚠️ Important Notes

1. **Database**: SQLite files are ephemeral on Render. For production, consider:
   - PostgreSQL (Render provides this)
   - External database service

2. **Environment Variables**: Update `WEBHOOK_SECRET` in Render dashboard for security

3. **Port Binding**: Always use `0.0.0.0` for external accessibility

## 🔍 Troubleshooting

### "No open ports detected" Error
- ✅ **Fixed**: Updated `main.py` to bind to `0.0.0.0`
- ✅ **Fixed**: Added `$PORT` environment variable support

### Build Failures
- Check `requirements.txt` has all dependencies
- Ensure Python version compatibility (3.11+ recommended)

### Runtime Errors
- Verify all import paths are correct
- Check environment variables are set in Render dashboard

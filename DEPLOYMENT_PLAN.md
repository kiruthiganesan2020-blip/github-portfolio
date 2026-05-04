# Deployment Plan: Render + Vercel

## Overview
Deploy Zomato AI with separate backend (Render) and frontend (Vercel) for optimal performance and scalability.

## Backend Deployment (Render)

### Prerequisites
- Render account (free tier available)
- GitHub repository connected to Render

### Steps
1. **Connect Repository**
   - Go to Render Dashboard
   - Click "New" → "Web Service"
   - Connect GitHub repository: `kiruthiganesan2020-blip/github-portfolio`

2. **Configure Service**
   - Name: `zomato-ai-backend`
   - Environment: `Python`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn backend.main:app --host 0.0.0.0 --port $PORT`
   - Instance Type: `Free` (or `Starter` for better performance)

3. **Environment Variables**
   ```
   GOOGLE_API_KEY=your_gemini_api_key
   PORT=10000
   FRONTEND_URL=https://your-vercel-app.vercel.app
   ```

4. **Deploy**
   - Click "Create Web Service"
   - Wait for deployment (2-3 minutes)
   - Note the deployed URL

## Frontend Deployment (Vercel)

### Prerequisites
- Vercel account (free tier available)
- Node.js installed locally

### Steps
1. **Install Dependencies**
   ```bash
   cd nextjs_frontend
   npm install
   ```

2. **Update API URL**
   - Edit `nextjs_frontend/app/page.tsx`
   - Replace `http://localhost:8000` with your Render backend URL

3. **Deploy to Vercel**
   ```bash
   cd nextjs_frontend
   npx vercel --prod
   ```
   - Follow prompts to connect to Vercel
   - Deploy to production

### Alternative: Vercel Dashboard
1. Go to Vercel Dashboard
2. Click "Add New" → "Project"
3. Import GitHub repository
4. Configure:
   - Framework: `Next.js`
   - Build Command: `npm run build`
   - Output Directory: `.next`
5. Add Environment Variable:
   ```
   NEXT_PUBLIC_API_URL=https://your-render-app.onrender.com
   ```

## Post-Deployment Checklist

### Backend (Render)
- [ ] Health check accessible at `/health`
- [ ] CORS configured for frontend domain
- [ ] API endpoints responding correctly
- [ ] Environment variables set
- [ ] Logs showing successful startup

### Frontend (Vercel)
- [ ] Application loads successfully
- [ ] API calls to backend working
- [ ] Forms submitting correctly
- [ ] Recommendations displaying
- [ ] Mobile responsive design

### Integration Testing
- [ ] Frontend can call backend API
- [ ] CORS headers properly configured
- [ ] Error handling working
- [ ] Loading states functioning
- [ ] Recommendations displaying correctly

## URLs After Deployment
- **Backend**: `https://your-app-name.onrender.com`
- **Frontend**: `https://your-app-name.vercel.app`
- **API Docs**: `https://your-app-name.onrender.com/docs`

## Monitoring
- Render: Dashboard shows logs, metrics, error rates
- Vercel: Analytics, performance metrics
- Both: Set up uptime monitoring if needed

## Troubleshooting

### Common Issues
1. **CORS Errors**: Check `FRONTEND_URL` environment variable
2. **API Timeouts**: Verify Render instance type (upgrade if needed)
3. **Build Failures**: Check `requirements.txt` and dependencies
4. **Frontend Errors**: Verify API URL configuration

### Performance Optimization
- Render: Upgrade to Starter instance for better performance
- Vercel: Enable Edge Functions if needed
- Both: Monitor and optimize API response times

## Security Considerations
- API keys stored in environment variables
- CORS restricted to specific domains in production
- Rate limiting implemented if needed
- HTTPS enforced on both platforms

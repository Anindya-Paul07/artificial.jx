# Deployment Guide

## Prerequisites

1. **Vercel Account**
   - Sign up at https://vercel.com/signup
   - Install Vercel CLI: `npm install -g vercel`

2. **Railway Account**
   - Sign up at https://railway.app/signup
   - Install Railway CLI: `curl -fsSL https://get.railway.app | sh`

3. **GroqCloud Account**
   - Sign up at https://cloud.groq.com/
   - Create API key in dashboard

## Environment Setup

1. Create `.env` file in root directory with:
```env
OPENAI_API_KEY=your_groq_api_key
NEXT_PUBLIC_GOOGLE_ADSENSE_ID=your_adsense_id (optional)
```

2. Add `.env` to `.gitignore` if not already there

## Deployment Process

1. **Install Dependencies**
```bash
npm install
```

2. **Build and Deploy**
```bash
./deploy.sh
```

The script will:
- Install dependencies
- Build frontend
- Deploy frontend to Vercel
- Deploy backend to Railway

## Post-Deployment

1. After deployment, set environment variables in both Vercel and Railway 
   - Get your GroqCloud API key and set it as OPENAI_API_KEY in your [.env](cci:7://file:///home/anindya-paul/projects/junior_project_structure/junior/.env:0:0-0:0) file
   - Install the required CLIs (Vercel and Railway) dashboards:
   - OPENAI_API_KEY (your GroqCloud API key)
   - NEXT_PUBLIC_GOOGLE_ADSENSE_ID (if using)

2. Update frontend configuration with backend URL in Railway

## Troubleshooting

If deployment fails:
1. Check logs in Vercel and Railway dashboards
2. Verify environment variables are set correctly
3. Ensure API keys have proper permissions
4. Check for any rate limits on GroqCloud API

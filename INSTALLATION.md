# Linux Installation Guide

## Prerequisites

### 1. Node.js and npm
```bash
# Install Node.js and npm
sudo apt update
sudo apt install nodejs npm

# Verify installation
node --version
npm --version
```

### 2. Vercel CLI
```bash
# Install Vercel CLI globally
npm install -g vercel

# Verify installation
vercel --version
```

### 3. Railway CLI
```bash
# Install Railway CLI
curl -fsSL https://get.railway.app | sh

# Verify installation
railway --version
```

### 4. Supabase Setup
1. Sign up at https://supabase.com/signup
2. Create a new project
3. Get your project URL and anon key from the dashboard
4. Add these to your .env file:
```env
NEXT_PUBLIC_SUPABASE_URL=your-project-url
NEXT_PUBLIC_SUPABASE_ANON_KEY=your-anon-key
```

## Environment Setup

1. Create a `.env` file in your project root:
```bash
touch .env
```

2. Add your environment variables:
```env
OPENAI_API_KEY=your_groq_api_key
NEXT_PUBLIC_GOOGLE_ADSENSE_ID=your_adsense_id (optional)
NEXT_PUBLIC_SUPABASE_URL=your-project-url
NEXT_PUBLIC_SUPABASE_ANON_KEY=your-anon-key
```

## Environment Setup

1. Create a `.env` file in your project root:
```bash
touch .env
```

2. Add your environment variables:
```env
OPENAI_API_KEY=your_groq_api_key
NEXT_PUBLIC_GOOGLE_ADSENSE_ID=your_adsense_id (optional)
```

## Project Setup

1. Install project dependencies:
```bash
cd /home/anindya-paul/projects/junior_project_structure/junior
npm install
```

2. Create a `.env` file with your API keys:
```bash
echo "OPENAI_API_KEY=your_groq_api_key" > .env
```

## Deployment Process

1. Run the deployment script:
```bash
./deploy.sh
```

The script will:
1. Check for required tools (Vercel, Railway)
2. Verify environment variables
3. Install dependencies
4. Build and deploy the project

## Troubleshooting

### Common Issues

1. **Missing Dependencies**
   - Solution: Run `npm install` in the project directory

2. **Missing Environment Variables**
   - Solution: Create `.env` file and add required variables

3. **Permission Errors**
   - Solution: Run commands with `sudo` if needed

4. **Network Issues**
   - Solution: Check your internet connection and try again

### Error Messages

If you encounter any of these errors, follow the suggested solutions:

1. "Error: vercel is not installed"
   ```bash
   npm install -g vercel
   ```

2. "Error: railway is not installed"
   ```bash
   curl -fsSL https://get.railway.app | sh
   ```

3. "Error: Missing required environment variables"
   - Create `.env` file
   - Add OPENAI_API_KEY
   - Add NEXT_PUBLIC_GOOGLE_ADSENSE_ID if using AdSense

## Post-Installation

1. After deployment, set environment variables in both Vercel and Railway dashboards
2. Verify deployment in both platforms
3. Test the application by accessing the provided URLs

#!/bin/bash

# Deploy script for Junior Project

echo "Starting deployment process..."

# Check if required tools are installed
check_tool_installed() {
    if ! command -v "$1" &> /dev/null; then
        echo "Error: $1 is not installed."
        echo "Please install $1 first."
        echo "Installation command: $2"
        exit 1
    fi
}

# Check for required environment variables
check_env_vars() {
    local required_vars=("OPENAI_API_KEY" "NEXT_PUBLIC_SUPABASE_URL" "NEXT_PUBLIC_SUPABASE_ANON_KEY")
    local missing_vars=()
    local env_file=".env"
    
    # Check if .env file exists
    if [ ! -f "$env_file" ]; then
        echo "Error: .env file not found"
        echo "Please create a .env file with your environment variables"
        exit 1
    fi
    
    # Source the .env file
    if [ -r "$env_file" ]; then
        export $(grep -v '^#' "$env_file" | xargs)
    else
        echo "Error: Cannot read .env file"
        exit 1
    fi
    
    # Check required variables
    for var in "${required_vars[@]}"; do
        if [ -z "${!var}" ]; then
            missing_vars+=("$var")
        fi
    done

    if [ ${#missing_vars[@]} -ne 0 ]; then
        echo "Error: Missing required environment variables:"
        printf "- %s\n" "${missing_vars[@]}"
        echo "Please set these variables in your .env file and try again."
        exit 1
    fi
}

# Install Vercel CLI if not installed
echo "\nChecking Vercel CLI..."
check_tool_installed "vercel" "npm install -g vercel"

# Install Railway CLI if not installed
echo "\nChecking Railway CLI..."
check_tool_installed "railway" "curl -fsSL https://get.railway.app | sh"

# Check environment variables
echo "\nChecking environment variables..."
check_env_vars

# Change to project directory
cd /home/anindya-paul/projects/junior_project_structure/junior || {
    echo "Error: Could not change to project directory"
    exit 1
}

echo "\n1. Installing dependencies..."
cd next-app
npm install

# Build frontend
echo "\n2. Building frontend..."
npm run build

# Deploy frontend to Vercel
echo "\n3. Deploying frontend to Vercel..."
vercel --prod

# Deploy backend to Railway
echo "\n4. Deploying backend to Railway..."
cd ../

# Login to Railway
railway login

# Deploy backend
railway deploy

echo "\nDeployment complete!"
echo "Frontend URL: https://your-vercel-url.vercel.app"
echo "Backend URL: https://your-railway-url.up.railway.app"

echo "\nImportant: Make sure to set these environment variables in both platforms:"
echo "- OPENAI_API_KEY (your GroqCloud API key)"
echo "- NEXT_PUBLIC_SUPABASE_URL (your Supabase project URL)"
echo "- NEXT_PUBLIC_SUPABASE_ANON_KEY (your Supabase anon key)"
echo "- NEXT_PUBLIC_GOOGLE_ADSENSE_ID (if using AdSense)"

echo "\nIf you encounter any errors, check the logs in both Vercel and Railway dashboards."
echo "\nNote: User data will be stored in Supabase. Make sure to set up your Supabase project first."

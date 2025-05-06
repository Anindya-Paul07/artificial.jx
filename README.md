# Junior AI Assistant

A modern AI-powered code analysis and assistant platform.

## Features

- Code analysis and suggestions
- AI-powered documentation
- Real-time error detection
- Context-aware search
- Premium features support

## Tech Stack

- Frontend: Next.js 14 with TypeScript
- Backend: FastAPI with Python
- Database: Supabase
- AI: OpenAI GPT-4, Claude
- UI: Tailwind CSS
- Authentication: Supabase Auth

## Project Structure

```
next-app/                 # Next.js frontend application
├── src/
│   ├── app/              # Next.js app router pages
│   ├── components/       # Reusable React components
│   ├── context/         # React context providers
│   ├── lib/            # Utility functions and shared code
│   ├── types/          # TypeScript type definitions
│   └── utils/          # Helper utilities
├── public/              # Static assets
├── tests/              # Test files
├── .env                # Environment variables
├── package.json        # Node.js dependencies
├── tsconfig.json       # TypeScript configuration
└── next.config.ts      # Next.js configuration

/
├── api/                 # API endpoints
├── core/               # Core application logic
├── agents/             # AI agents implementation
├── inference/          # ML/AI inference code
├── supabase/           # Supabase database configuration
└── requirements.txt    # Python dependencies
```

## Getting Started

1. Clone the repository
2. Install dependencies:
   ```bash
   # Install Python dependencies
   pip install -r requirements.txt
   
   # Install Next.js dependencies
   cd next-app
   npm install
   ```
3. Set up environment variables:
   - Copy `.env.example` to `.env`
   - Fill in your API keys and configuration
4. Run the development servers:
   ```bash
   # Start Python backend
   python main.py
   
   # Start Next.js frontend
   cd next-app
   npm run dev
   ```

## Environment Variables

- `NEXT_PUBLIC_SUPABASE_URL`: Supabase project URL
- `NEXT_PUBLIC_SUPABASE_ANON_KEY`: Supabase anonymous key
- `OPENAI_API_KEY`: OpenAI API key
- `CLAUDE_API_KEY`: Anthropic API key (optional)

## Deployment

### Local Development

1. Install dependencies:
   ```bash
   # Install Python dependencies
   pip install -r requirements.txt
   
   # Install Next.js dependencies
   cd next-app
   npm install
   ```

2. Run the development servers:
2. Run the development server:
   ```bash
   npm run dev
   ```

3. Build for production:
   ```bash
   npm run build
   ```

### Vercel Deployment

1. Install Vercel CLI:
   ```bash
   npm install -g vercel
   ```

2. Login to Vercel:
   ```bash
   vercel login
   ```

3. Deploy:
   ```bash
   vercel
   ```

### Railway Deployment

1. Install Railway CLI:
   ```bash
   curl -fsSL https://raw.githubusercontent.com/railwayapp/cli/main/install.sh | sh
   ```

2. Login to Railway:
   ```bash
   railway login
   ```

3. Deploy:
   ```bash
   railway deploy
   ```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

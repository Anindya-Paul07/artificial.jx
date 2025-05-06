declare global {
  interface Window {
    __env: {
      NEXT_PUBLIC_SUPABASE_URL: string;
      NEXT_PUBLIC_SUPABASE_ANON_KEY: string;
    };
  }
}

export {}; // Make this a module

export const getEnvironmentVariables = () => {
  const env = {
    NEXT_PUBLIC_SUPABASE_URL: process.env.NEXT_PUBLIC_SUPABASE_URL,
    NEXT_PUBLIC_SUPABASE_ANON_KEY: process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY,
  };

  if (typeof window !== 'undefined') {
    // Client-side
    if (!env.NEXT_PUBLIC_SUPABASE_URL || !env.NEXT_PUBLIC_SUPABASE_ANON_KEY) {
      console.error('Missing client-side environment variables:', env);
      throw new Error('Missing client-side environment variables');
    }
    return env;
  }

  // Server-side
  if (!env.NEXT_PUBLIC_SUPABASE_URL || !env.NEXT_PUBLIC_SUPABASE_ANON_KEY) {
    console.error('Missing server-side environment variables:', env);
    throw new Error('Missing server-side environment variables');
  }

  return env;
};

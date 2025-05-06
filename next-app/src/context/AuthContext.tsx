'use client';

import { createContext, useContext, useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { createClient } from '@supabase/supabase-js';
import { getEnvironmentVariables } from '../utils/env';

import { Session, User } from '@supabase/supabase-js';
import { AuthChangeEvent } from '@supabase/supabase-js';

// Initialize Supabase client
const env = getEnvironmentVariables();
const supabaseClient = createClient(
  env.NEXT_PUBLIC_SUPABASE_URL!,
  env.NEXT_PUBLIC_SUPABASE_ANON_KEY!
);

interface AuthContextType {
  user: User | null;
  isLoading: boolean;
  signIn: (email: string, password: string) => Promise<void>;
  signUp: (email: string, password: string, fullName: string) => Promise<void>;
  signOut: () => Promise<void>;
  updateProfile: (updates: { data: { fullName?: string; avatarUrl?: string } }) => Promise<void>;
  error: string | null;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<any | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const router = useRouter();

  useEffect(() => {
    // Get user from storage
    supabase.auth.getSession().then(({ data: { session } }) => {
      setUser(session?.user ?? null);
      setIsLoading(false);
    });

    // Listen for changes on auth state
    const { data: { subscription } } = supabaseClient.auth.onAuthStateChange((event: AuthChangeEvent, session: Session | null) => {
      setUser(session?.user ?? null);
      if (!event && !session?.user) {
        router.push('/auth/login');
      }
    });

    return () => {
      subscription.unsubscribe();
    };
  }, [router]);

  const signIn = async (email: string, password: string) => {
    try {
      setError(null);
      const { data: { session }, error } = await supabaseClient.auth.signInWithPassword({
        email,
        password,
      });

      if (error) throw error;
      router.push('/dashboard');
    } catch (err) {
      setError(err instanceof Error ? err.message : String(err) || 'Authentication failed');
      throw err;
    }
  };

  const signUp = async (email: string, password: string, fullName: string) => {
    try {
      setError(null);
      const { data: { user }, error } = await supabaseClient.auth.signUp({
        email,
        password,
        options: {
          data: {
            fullName,
          },
        },
      });

      if (error) throw error;
      router.push('/dashboard');
    } catch (err) {
      setError(err instanceof Error ? err.message : String(err) || 'Authentication failed');
      throw err;
    }
  };

  const signOut = async () => {
    try {
      setError(null);
      const { error } = await supabaseClient.auth.signOut();

      if (error) throw error;
      router.push('/auth/login');
    } catch (err) {
      setError(err instanceof Error ? err.message : String(err) || 'Authentication failed');
      throw err;
    }
  };

  const updateProfile = async (updates: { data: { fullName?: string; avatarUrl?: string } }) => {
    try {
      const { error } = await supabaseClient.auth.updateUser(updates.data);
      if (error) throw error;
    } catch (error) {
      setError(error instanceof Error ? error.message : 'Failed to update profile');
    }
  };

  return (
    <AuthContext.Provider value={{
      user,
      isLoading,
      signIn,
      signUp,
      signOut,
      updateProfile,
      error,
    }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
}

import { NextRequest, NextResponse } from 'next/server';
import { supabase } from '@/lib/supabase';
import { CodeAnalysisAgent } from '@/lib/agents';
import { ContextManager } from '@/lib/context';

const agent = new CodeAnalysisAgent();
const contextManager = ContextManager.getInstance();

// Helper function to get user ID from request
async function getUserId(request: NextRequest) {
  const { searchParams } = new URL(request.url);
  const session = await supabase.auth.getSession();
  return session.data.session?.user.id;
}

export async function POST(request: NextRequest) {
  try {
    const { action, data } = await request.json();

    switch (action) {
      case 'analyze': {
        const { code, context, fileId } = data;
        const analysis = await agent.analyze(code, context);
        
        // Save to Supabase
        const userId = await getUserId(request);
        if (!userId) {
          return NextResponse.json({ error: 'User not authenticated' }, { status: 401 });
        }

        await supabase.from('code_analysis').insert({
          user_id: userId,
          code: code,
          analysis: analysis,
          context: context,
          file_id: fileId
        });

        return NextResponse.json(analysis);
      }

      case 'search': {
        const { query, context } = data;
        const userId = await getUserId(request);
        if (!userId) {
          return NextResponse.json({ error: 'User not authenticated' }, { status: 401 });
        }

        const { data: searchResults } = await supabase
          .from('code_analysis')
          .select('*')
          .eq('user_id', userId)
          .ilike('code', `%${query}%`)
          .or(`analysis->>suggestions.ilike.%${query}%,analysis->>errors.ilike.%${query}%`)
          .limit(10);
        return NextResponse.json(searchResults);
      }

      case 'getContext': {
        const { fileId } = data;
        const userId = await getUserId(request);
        if (!userId) {
          return NextResponse.json({ error: 'User not authenticated' }, { status: 401 });
        }

        const { data: contextItems } = await supabase
          .from('code_analysis')
          .select('*')
          .eq('user_id', userId)
          .eq('file_id', fileId);
        return NextResponse.json(contextItems);
      }

      case 'searchContext': {
        const { query } = data;
        const userId = await getUserId(request);
        if (!userId) {
          return NextResponse.json({ error: 'User not authenticated' }, { status: 401 });
        }

        const { data: results } = await supabase
          .from('code_analysis')
          .select('*')
          .eq('user_id', userId)
          .ilike('code', `%${query}%`)
          .or(`analysis->>suggestions.ilike.%${query}%,analysis->>errors.ilike.%${query}%`)
          .limit(10);
        return NextResponse.json(results);
      }

      default:
        return NextResponse.json(
          { error: 'Invalid action' },
          { status: 400 }
        );
    }
  } catch (error) {
    console.error('API Error:', error);
    return NextResponse.json(
      { error: 'Internal server error' },
      { status: 500 }
    );
  }
}

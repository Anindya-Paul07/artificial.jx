import { supabase } from '../lib/supabase';
import { describe, it, expect, beforeAll, afterAll } from 'vitest';

describe('Database Operations', () => {
  let userId: string;
  let analysisId: string;

  beforeAll(async () => {
    // Create a test user
    const { data: { user }, error } = await supabase.auth.signUp({
      email: `test${Date.now()}@example.com`,
      password: 'password123',
    });

    if (error) throw error;
    userId = user.id;

    // Wait for user to be created
    await new Promise(resolve => setTimeout(resolve, 1000));
  });

  afterAll(async () => {
    // Clean up test data
    const { error: deleteError } = await supabase
      .from('code_analysis')
      .delete()
      .eq('user_id', userId);

    if (deleteError) console.error('Error cleaning up test data:', deleteError);

    // Delete test user
    const { error: authError } = await supabase.auth.admin.deleteUser(userId);
    if (authError) console.error('Error deleting test user:', authError);
  });

  it('should create and retrieve code analysis', async () => {
    // Create test analysis
    const testCode = 'function add(a, b) { return a + b; }';
    const testAnalysis = {
      suggestions: ['Add type annotations'],
      potentialIssues: [],
      bestPractices: ['Use descriptive variable names'],
    };

    const { data, error } = await supabase
      .from('code_analysis')
      .insert({
        user_id: userId,
        code: testCode,
        analysis: testAnalysis,
        context: 'Basic function example'
      })
      .select()
      .single();

    expect(error).toBeNull();
    expect(data).toBeDefined();
    expect(data.code).toBe(testCode);
    analysisId = data.id;

    // Retrieve analysis
    const { data: retrieved, error: retrieveError } = await supabase
      .from('code_analysis')
      .select('*')
      .eq('id', analysisId)
      .single();

    expect(retrieveError).toBeNull();
    expect(retrieved).toBeDefined();
    expect(retrieved.code).toBe(testCode);
    expect(retrieved.analysis).toEqual(testAnalysis);
  });

  it('should enforce Row Level Security', async () => {
    // Try to access another user's analysis
    const { data: otherUserAnalysis, error: accessError } = await supabase
      .from('code_analysis')
      .select('*')
      .eq('user_id', 'non-existent-id')
      .single();

    expect(accessError).toBeDefined();
    expect(otherUserAnalysis).toBeNull();
  });

  it('should update code analysis', async () => {
    const updatedAnalysis = {
      suggestions: ['Add type annotations', 'Add error handling'],
      potentialIssues: ['No error handling'],
      bestPractices: ['Use descriptive variable names']
    };

    const { error: updateError } = await supabase
      .from('code_analysis')
      .update({
        analysis: updatedAnalysis
      })
      .eq('id', analysisId);

    expect(updateError).toBeNull();

    const { data: updated, error: retrieveError } = await supabase
      .from('code_analysis')
      .select('*')
      .eq('id', analysisId)
      .single();

    expect(retrieveError).toBeNull();
    expect(updated.analysis).toEqual(updatedAnalysis);
  });

  it('should delete code analysis', async () => {
    const { error: deleteError } = await supabase
      .from('code_analysis')
      .delete()
      .eq('id', analysisId);

    expect(deleteError).toBeNull();

    const { data: deleted, error: retrieveError } = await supabase
      .from('code_analysis')
      .select('*')
      .eq('id', analysisId)
      .single();

    expect(retrieveError).toBeNull();
    expect(deleted).toBeNull();
  });
});

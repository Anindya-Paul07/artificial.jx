import { OpenAI } from 'openai';
import { CacheManager } from './cache_manager';
import { LanguageHub } from './language_hub';

export interface ProblemAnalysis {
  type: string;
  difficulty: string;
  requirements: string[];
  constraints: string[];
}

export interface CodeSolution {
  code: string;
  explanation: string;
  complexity: string;
}

export class ProblemSolver {
  private openai: OpenAI;
  private cache: CacheManager;
  private languageHub: LanguageHub;

  constructor() {
    this.openai = new OpenAI({
      apiKey: process.env.OPENAI_API_KEY
    });
    this.cache = new CacheManager();
    this.languageHub = new LanguageHub();
  }

  async analyzeProblem(problem: string): Promise<ProblemAnalysis> {
    const cacheKey = `analysis:${problem}`;
    const cached = await this.cache.get(cacheKey);
    
    if (cached) {
      return cached;
    }

    const completion = await this.openai.chat.completions.create({
      model: "gpt-4",
      messages: [
        {
          role: "system",
          content: "You are a problem analysis expert. Analyze the given problem and provide a structured analysis."
        },
        {
          role: "user",
          content: problem
        }
      ]
    });

    const analysis = JSON.parse(completion.choices[0].message.content) as ProblemAnalysis;
    await this.cache.set(cacheKey, analysis);
    return analysis;
  }

  async generateSolution(analysis: ProblemAnalysis, language: string): Promise<CodeSolution> {
    const cacheKey = `solution:${JSON.stringify(analysis)}:${language}`;
    const cached = await this.cache.get(cacheKey);
    
    if (cached) {
      return cached;
    }

    const completion = await this.openai.chat.completions.create({
      model: "gpt-4",
      messages: [
        {
          role: "system",
          content: `You are a ${language} code generation expert. Generate a solution based on the given analysis.`
        },
        {
          role: "user",
          content: JSON.stringify(analysis)
        }
      ]
    });

    const solution = JSON.parse(completion.choices[0].message.content) as CodeSolution;
    await this.cache.set(cacheKey, solution);
    return solution;
  }

  async translateMathToCode(expression: string, language: string): Promise<CodeSolution> {
    const completion = await this.openai.chat.completions.create({
      model: "gpt-4",
      messages: [
        {
          role: "system",
          content: `You are a math-to-code translator. Convert the given mathematical expression to ${language} code.`
        },
        {
          role: "user",
          content: expression
        }
      ]
    });

    return JSON.parse(completion.choices[0].message.content) as CodeSolution;
  }

  async optimizeSolution(code: string, language: string, goal: string): Promise<CodeSolution> {
    const completion = await this.openai.chat.completions.create({
      model: "gpt-4",
      messages: [
        {
          role: "system",
          content: `You are a code optimization expert. Optimize the given ${language} code for ${goal} efficiency.`
        },
        {
          role: "user",
          content: code
        }
      ]
    });

    return JSON.parse(completion.choices[0].message.content) as CodeSolution;
  }
}

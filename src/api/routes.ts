import { FastifyInstance, RouteGenericInterface, FastifyRequest, FastifyReply } from 'fastify';
import { ProblemSolver } from '../core/problem_solver';
import { analyzeFileForErrors } from '../core/error_detector';
import { loadJson } from '../utils/helpers';

const ERROR_ANALYSIS_PATH = '../core/error_analysis.json';
const problemSolver = new ProblemSolver();

export async function apiRouter(fastify: FastifyInstance) {
  const router = fastify;

  interface AnalyzeRequest {
    Body: {
      file_path: string;
    };
  }

  interface GetErrorsRequest {
    Querystring: {
      file_path?: string;
    };
  }

  interface SolveProblemRequest {
    Body: {
      problem: string;
      language: string;
    };
  }

  interface TranslateMathRequest {
    Body: {
      expression: string;
      language: string;
    };
  }

  interface OptimizeCodeRequest {
    Body: {
      code: string;
      language: string;
      goal: string;
    };
  }

  router.get('/', async (request: FastifyRequest, reply: FastifyReply) => {
    return { message: 'Junior FastAPI is running!' };
  });

  router.get('/status', async (request: FastifyRequest, reply: FastifyReply) => {
    return { status: 'running', message: 'Junior backend is active.' };
  });

  router.post<AnalyzeRequest>('/analyze', async (request: FastifyRequest<AnalyzeRequest>, reply: FastifyReply) => {
    const { file_path } = request.body;
    
    if (!file_path || !await router.fs.exists(file_path)) {
      reply.status(404).send({ error: 'File not found' });
      return;
    }
    
    const results = await analyzeFileForErrors(file_path);
    return results;
  });

  router.get<GetErrorsRequest>('/errors', async (request: FastifyRequest<GetErrorsRequest>, reply: FastifyReply) => {
    if (!await router.fs.exists(ERROR_ANALYSIS_PATH)) {
      return { errors: [] };
    }
    
    const errorData = await loadJson(ERROR_ANALYSIS_PATH);
    
    if (request.query.file_path) {
      return { errors: errorData[request.query.file_path] || {} };
    }
    
    return { errors: errorData };
  });

  router.post<SolveProblemRequest>('/solve-problem', async (request: FastifyRequest<SolveProblemRequest>, reply: FastifyReply) => {
    const { problem, language } = request.body;
    const analysis = await problemSolver.analyzeProblem(problem);
    const solution = await problemSolver.generateSolution(analysis, language);
    
    return {
      analysis,
      solution
    };
  });

  router.post<TranslateMathRequest>('/translate-math', async (request: FastifyRequest<TranslateMathRequest>, reply: FastifyReply) => {
    const { expression, language } = request.body;
    const result = await problemSolver.translateMathToCode(expression, language);
    return result;
  });

  router.post<OptimizeCodeRequest>('/optimize-code', async (request: FastifyRequest<OptimizeCodeRequest>, reply: FastifyReply) => {
    const { code, language, goal } = request.body;
    const result = await problemSolver.optimizeSolution(code, language, goal);
    return result;
  });
}

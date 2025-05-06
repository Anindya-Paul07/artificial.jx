export interface FileAnalysis {
  path: string;
  suggestions: string[];
  errors: string[];
  context: string;
  score?: number;
  content?: string;
  fileId?: string;
}

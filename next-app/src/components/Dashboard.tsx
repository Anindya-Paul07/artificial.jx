'use client';

import { useState, useEffect, useRef } from 'react';
import { MagnifyingGlassIcon as SearchIcon, XMarkIcon as XIcon } from '@heroicons/react/24/outline';
import { useInView } from 'react-intersection-observer';
import { FileAnalysis } from '../types/file-analysis';
import { toast } from 'react-hot-toast';

export default function Dashboard() {
  const [files, setFiles] = useState<File[]>([]);
  const [analysis, setAnalysis] = useState<FileAnalysis[]>([]);
  const [isPremium, setIsPremium] = useState(false);
  const [loading, setLoading] = useState(false);
  const [searchQuery, setSearchQuery] = useState('');
  const [context, setContext] = useState<string[]>([]);
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const { ref, inView } = useInView({ threshold: 0.1 });
  const searchRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    if (inView) {
      analyzeFiles();
    }
  }, [inView]);

  const analyzeFiles = async () => {
    try {
      setLoading(true);
      const response = await fetch('/api/analyze-files');
      if (!response.ok) {
        throw new Error('Failed to analyze files');
      }
      const data = await response.json();
      setAnalysis(data.analysis);
    } catch (error) {
      console.error('Error analyzing files:', error);
      toast.error('Failed to analyze files');
    } finally {
      setLoading(false);
    }
  };

  const handleSearch = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!searchQuery.trim()) return;

    try {
      setLoading(true);
      const response = await fetch('/api/search', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query: searchQuery, context }),
      });
      const data = await response.json();
      setAnalysis(data.results);
    } catch (error) {
      console.error('Error searching:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleClearSearch = () => {
    setSearchQuery('');
    setAnalysis([]);
  };

  const handleFileSelect = (file: File) => {
    setSelectedFile(file);
    setContext([]);
  };

  const handleContextSelect = (contextItem: string) => {
    setContext(prev => [...prev, contextItem]);
  };

  return (
    <div className="container mx-auto px-4 py-8">
      <div className="max-w-4xl mx-auto">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">
            Junior AI Assistant
          </h1>
          <p className="text-gray-600">
            Your intelligent code assistant
          </p>
        </div>

        {/* File Upload */}
        <div className="mb-8">
          <div className="border rounded-lg p-6 bg-white shadow-sm">
            <h2 className="text-xl font-semibold mb-4">Upload Files</h2>
            <div className="border-dashed border-2 border-gray-300 rounded-lg p-6 text-center">
              <label className="cursor-pointer">
                <div className="text-gray-600">
                  <svg className="w-12 h-12 mx-auto mb-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
                  </svg>
                  <p className="text-sm text-gray-500 mt-1">
                    Drag and drop files here or click to upload
                  </p>
                </div>
                <input
                  type="file"
                  multiple
                  className="hidden"
                  onChange={(e) => {
                    const selectedFiles = Array.from(e.target.files || []);
                    setFiles(prev => [...prev, ...selectedFiles]);
                  }}
                />
              </label>
            </div>
          </div>
        </div>

        {/* Search Section */}
        <div className="mb-8">
          <h2 className="text-xl font-semibold mb-4">Search & Context</h2>
          <form onSubmit={handleSearch} className="space-y-4">
            <div className="relative">
              <SearchIcon className="absolute left-3 top-3 h-5 w-5 text-gray-400" />
              <input
                type="text"
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                placeholder="Search code/documentation"
                className="w-full pl-10 pr-10 py-3 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-primary"
              />
              {searchQuery && (
                <button
                  type="button"
                  onClick={handleClearSearch}
                  className="absolute right-3 top-3 text-gray-400 hover:text-gray-600"
                  aria-label="Clear search"
                >
                  <XIcon className="h-5 w-5" />
                </button>
              )}
            </div>

            <div className="space-y-2">
              <label className="block text-sm font-medium text-gray-700">
                Context
              </label>
              <div className="flex flex-wrap gap-2">
                {context.map((item, index) => (
                  <span
                    key={index}
                    className="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium bg-primary/10 text-primary"
                  >
                    {item}
                    <button
                      type="button"
                      onClick={() => setContext(prev => prev.filter((_, i) => i !== index))}
                      className="ml-2 text-gray-400 hover:text-gray-600"
                      aria-label={`Remove context tag: ${item}`}
                    >
                      <XIcon className="h-4 w-4" />
                    </button>
                  </span>
                ))}
              </div>
            </div>

            <button
              type="submit"
              disabled={loading}
              className="w-full py-3 px-6 rounded-lg bg-primary text-white font-medium hover:bg-primary/90 transition-colors disabled:opacity-50"
            >
              {loading ? (
                <div className="flex items-center justify-center">
                  <svg className="animate-spin h-5 w-5 mr-2 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                    <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                  </svg>
                  Searching...
                </div>
              ) : (
                'Search'
              )}
            </button>
          </form>
        </div>

        {/* Results Section */}
        <div>
          <h2 className="text-xl font-semibold mb-4">Results</h2>
          <div className="space-y-4">
            {analysis.map((result, index) => (
              <div
                key={index}
                className="border rounded-lg p-6 bg-white shadow-sm"
              >
                <div className="flex items-center justify-between mb-4">
                  <h3 className="text-lg font-medium text-gray-900">
                    {result.path}
                  </h3>
                </div>
                <div className="space-y-4">
                  <div>
                    <h4 className="font-semibold mb-2">AI Suggestions:</h4>
                    <ul className="list-disc list-inside">
                      {result.suggestions.map((suggestion, i) => (
                        <li key={i} className="text-gray-700">
                          <span className="font-medium">Claude:</span> {suggestion}
                        </li>
                      ))}
                    </ul>
                  </div>

                  <div>
                    <h4 className="font-semibold mb-2">Potential Errors:</h4>
                    <ul className="list-disc list-inside">
                      {result.errors.map((error, i) => (
                        <li key={i} className="text-red-600">
                          <span className="font-medium">GPT-4:</span> {error}
                        </li>
                      ))}
                    </ul>
                  </div>

                  <div>
                    <h4 className="font-semibold mb-2">Context Analysis:</h4>
                    <p className="text-gray-600 whitespace-pre-wrap">{result.context}</p>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}

export interface AnalysisResult {
  id: string;
  timestamp: string;
  keyCombination: string;
  frequency: number;
  context: string;
  recommendation: string;
  significance: 'high' | 'medium' | 'low';
  category: string;
}

export interface FilterOptions {
  significance?: 'high' | 'medium' | 'low';
  category?: string;
  dateRange?: {
    start: string;
    end: string;
  };
  search?: string;
}

export interface SortOptions {
  field: keyof AnalysisResult;
  direction: 'asc' | 'desc';
}

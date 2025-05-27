export interface AnalysisResult {
  id: number;
  analysisType: string;
  campaign: {
    id: number;
    name: string;
  };
  dateDetected: string;
  severity: 'high' | 'medium' | 'low' | 'critical';
  metricAffected: string;
  description: string;
  recommendations: string[];
  createdAt: string;
}

export interface FilterOptions {
  severity?: string;
  analysisType?: string;
  metricAffected?: string;
  dateRange?: {
    start: string;
    end: string;
  };
}

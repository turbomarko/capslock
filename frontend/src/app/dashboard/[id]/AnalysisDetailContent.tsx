'use client';

import { useParams } from 'next/navigation';
import Link from 'next/link';
import { useGetAnalyticsByIdQuery } from '@/redux/analytics';
import { LoadingSpinner } from '@/components/ui';

export default function AnalysisDetailContent() {
  const { id } = useParams();
  const { data: analysis, isLoading, isError } = useGetAnalyticsByIdQuery(Number(id));

  if (isLoading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <LoadingSpinner />
      </div>
    );
  }

  if (isError || !analysis) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <h1 className="text-2xl font-semibold text-gray-900 mb-4">Error loading analysis</h1>
          <Link href="/dashboard" className="text-blue-600 hover:text-blue-800">
            Return to Dashboard
          </Link>
        </div>
      </div>
    );
  }

  // Parse recommendations if they're a string
  const recommendations = typeof analysis.recommendations === 'string' 
    ? JSON.parse(analysis.recommendations) 
    : analysis.recommendations;

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-lg font-medium text-gray-900">Campaign</h2>
        <p className="mt-1 text-sm text-gray-600">{analysis.campaign.name}</p>
      </div>

      <div>
        <h2 className="text-lg font-medium text-gray-900">Date Detected</h2>
        <p className="mt-1 text-sm text-gray-600">
          {new Date(analysis.dateDetected).toLocaleDateString('en-GB', {
            day: '2-digit',
            month: '2-digit',
            year: 'numeric'
          })}
        </p>
      </div>

      <div>
        <h2 className="text-lg font-medium text-gray-900">Analysis Type</h2>
        <p className="mt-1">
          <span className="font-mono bg-gray-100 px-2 py-1 rounded text-gray-900">
            {analysis.analysisType}
          </span>
        </p>
      </div>

      <div>
        <h2 className="text-lg font-medium text-gray-900">Severity</h2>
        <p className="mt-1">
          <span
            className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${
              analysis.severity === 'critical'
                ? 'bg-red-100 text-red-800'
                : analysis.severity === 'high'
                ? 'bg-orange-100 text-orange-800'
                : analysis.severity === 'medium'
                ? 'bg-yellow-100 text-yellow-800'
                : 'bg-green-100 text-green-800'
            }`}
          >
            {analysis.severity.charAt(0).toUpperCase() + analysis.severity.slice(1)}
          </span>
        </p>
      </div>

      <div>
        <h2 className="text-lg font-medium text-gray-900">Metric Affected</h2>
        <p className="mt-1 text-sm text-gray-600">{analysis.metricAffected}</p>
      </div>

      <div>
        <h2 className="text-lg font-medium text-gray-900">Description</h2>
        <p className="mt-1 text-sm text-gray-600">{analysis.description}</p>
      </div>

      <div>
        <h2 className="text-lg font-medium text-gray-900">Recommendations</h2>
        <ul className="mt-1 list-disc list-inside text-sm text-gray-600">
          {recommendations.map((rec: string, index: number) => (
            <li key={index}>{rec}</li>
          ))}
        </ul>
      </div>
    </div>
  );
} 
'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { createColumnHelper, ColumnDef } from '@tanstack/react-table';

import { AnalysisResult, FilterOptions, SortOptions } from '@/types/analysis';
import { DataTable, LoadingSpinner } from '@/components/ui';
import { FilterBar } from './FilterBar';

import { useGetAnalyticsQuery } from '@/redux/analytics';

const columnHelper = createColumnHelper<AnalysisResult>();

const columns: ColumnDef<AnalysisResult, any>[] = [
  columnHelper.accessor('dateDetected', {
    header: 'Date Detected',
    cell: (info) => {
      const date = new Date(info.getValue());
      return date.toLocaleDateString('en-GB', {
        day: '2-digit',
        month: '2-digit',
        year: 'numeric'
      });
    },
  }),
  columnHelper.accessor('campaign', {
    header: 'Campaign',
    cell: (info) => info.getValue(),
  }),
  columnHelper.accessor('analysisType', {
    header: 'Analysis Type',
    cell: (info) => (
      <span className="font-mono bg-gray-100 px-2 py-1 rounded">
        {info.getValue()}
      </span>
    ),
  }),
  columnHelper.accessor('metricAffected', {
    header: 'Metric Affected',
    cell: (info) => info.getValue(),
  }),
  columnHelper.accessor('description', {
    header: 'Description',
    cell: (info) => (
      <div className="max-w-md">
        <p className="text-sm text-gray-600">{info.getValue()}</p>
      </div>
    ),
  }),
  columnHelper.accessor('recommendations', {
    header: 'Recommendations',
    cell: (info) => {
      const recommendations = typeof info.getValue() === 'string' 
        ? JSON.parse(info.getValue()) 
        : info.getValue();
      
      return (
        <div className="max-w-md">
          <ul className="list-disc list-inside text-sm text-gray-600">
            {recommendations.map((rec: string, index: number) => (
              <li key={index}>{rec}</li>
            ))}
          </ul>
        </div>
      );
    },
  }),
  columnHelper.accessor('severity', {
    header: 'Severity',
    cell: (info) => (
      <span
        className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${
          info.getValue() === 'critical'
            ? 'bg-red-100 text-red-800'
            : info.getValue() === 'high'
            ? 'bg-orange-100 text-orange-800'
            : info.getValue() === 'medium'
            ? 'bg-yellow-100 text-yellow-800'
            : 'bg-green-100 text-green-800'
        }`}
      >
        {info.getValue().charAt(0).toUpperCase() + info.getValue().slice(1)}
      </span>
    ),
  }),
];

export default function DashboardContent() {
  const router = useRouter();
  const [filters, setFilters] = useState<FilterOptions>({});
  const [sort, setSort] = useState<SortOptions>({ field: 'dateDetected', direction: 'desc' });
  const { data: analytics, isLoading, isError } = useGetAnalyticsQuery(
    {
      severity: filters.severity,
      analysisType: filters.analysisType,
      metricAffected: filters.metricAffected,
      dateRange: filters.dateRange,
    }
  );

  const handleRowClick = (row: AnalysisResult) => {
    router.push(`/dashboard/${row.id}`);
  };

  if (isLoading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <LoadingSpinner />
      </div>
    );
  }

  if (isError) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <h1 className="text-2xl font-semibold text-gray-900 mb-4">Error loading analytics</h1>
          <p className="text-gray-600 mb-4">Please try refreshing the page</p>
        </div>
      </div>
    );
  }

  return (
    <>
      <FilterBar
        currentFilters={filters}
        onFilterChange={setFilters}
      />

      <div className="mt-6">
        <DataTable
          data={analytics || []}
          columns={columns}
          onRowClick={handleRowClick}
        />
      </div>
    </>
  );
} 
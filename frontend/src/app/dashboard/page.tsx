'use client';

import { useState } from 'react';
import { DataTable } from '@/components/DataTable';
import { FilterBar } from '@/components/FilterBar';
import { AnalysisResult, FilterOptions, SortOptions } from '@/types/analysis';
import { createColumnHelper, ColumnDef } from '@tanstack/react-table';

// Mock data - replace with actual API call
const mockData: AnalysisResult[] = [
  {
    id: '1',
    timestamp: '2024-03-20T10:00:00Z',
    keyCombination: 'Ctrl+C',
    frequency: 150,
    context: 'Text editing',
    recommendation: 'Consider using Ctrl+Shift+C for more precise copying',
    significance: 'high',
    category: 'Editing',
  },
  // Add more mock data as needed
];

const columnHelper = createColumnHelper<AnalysisResult>();

const columns: ColumnDef<AnalysisResult, any>[] = [
  columnHelper.accessor('timestamp', {
    header: 'Time',
    cell: (info) => new Date(info.getValue()).toLocaleString(),
  }),
  columnHelper.accessor('keyCombination', {
    header: 'Key Combination',
    cell: (info) => (
      <span className="font-mono bg-gray-100 px-2 py-1 rounded">
        {info.getValue()}
      </span>
    ),
  }),
  columnHelper.accessor('frequency', {
    header: 'Frequency',
    cell: (info) => info.getValue(),
  }),
  columnHelper.accessor('context', {
    header: 'Context',
    cell: (info) => info.getValue(),
  }),
  columnHelper.accessor('recommendation', {
    header: 'Recommendation',
    cell: (info) => (
      <div className="max-w-md">
        <p className="text-sm text-gray-600">{info.getValue()}</p>
      </div>
    ),
  }),
  columnHelper.accessor('significance', {
    header: 'Significance',
    cell: (info) => (
      <span
        className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${
          info.getValue() === 'high'
            ? 'bg-red-100 text-red-800'
            : info.getValue() === 'medium'
            ? 'bg-yellow-100 text-yellow-800'
            : 'bg-green-100 text-green-800'
        }`}
      >
        {info.getValue().charAt(0).toUpperCase() + info.getValue().slice(1)}
      </span>
    ),
  }),
  columnHelper.accessor('category', {
    header: 'Category',
    cell: (info) => info.getValue(),
  }),
];

export default function DashboardPage() {
  const [filters, setFilters] = useState<FilterOptions>({});
  const [sort, setSort] = useState<SortOptions>({ field: 'timestamp', direction: 'desc' });

  // Filter and sort the data
  const filteredData = mockData.filter((item) => {
    if (filters.significance && item.significance !== filters.significance) return false;
    if (filters.category && item.category !== filters.category) return false;
    if (filters.search) {
      const searchLower = filters.search.toLowerCase();
      return (
        item.keyCombination.toLowerCase().includes(searchLower) ||
        item.context.toLowerCase().includes(searchLower) ||
        item.recommendation.toLowerCase().includes(searchLower)
      );
    }
    return true;
  });

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
        <div className="px-4 py-6 sm:px-0">
          <div className="bg-white rounded-lg shadow">
            <div className="px-4 py-5 sm:p-6">
              <h1 className="text-2xl font-semibold text-gray-900 mb-6">
                Keyboard Analysis Dashboard
              </h1>
              
              <FilterBar
                currentFilters={filters}
                onFilterChange={setFilters}
              />

              <div className="mt-6">
                <DataTable
                  data={filteredData}
                  columns={columns}
                  onSort={(field, direction) =>
                    setSort({ field: field as keyof AnalysisResult, direction })
                  }
                />
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
} 
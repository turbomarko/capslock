import { FilterOptions } from '@/types/analysis';

interface FilterBarProps {
  currentFilters: FilterOptions;
  onFilterChange: (filters: FilterOptions) => void;
}

export function FilterBar({ currentFilters, onFilterChange }: FilterBarProps) {
  const handleFilterChange = (key: keyof FilterOptions, value: any) => {
    onFilterChange({
      ...currentFilters,
      [key]: value,
    });
  };

  return (
    <div className="flex flex-wrap gap-4 items-center">
      <select
        className="rounded-md border-gray-300 bg-white text-gray-900 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 py-2 px-3 font-medium"
        value={currentFilters.severity || ''}
        onChange={(e) => handleFilterChange('severity', e.target.value || undefined)}
      >
        <option value="">All Severities</option>
        <option value="critical">Critical</option>
        <option value="high">High</option>
        <option value="medium">Medium</option>
        <option value="low">Low</option>
      </select>

      <select
        className="rounded-md border-gray-300 bg-white text-gray-900 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 py-2 px-3 font-medium"
        value={currentFilters.analysisType || ''}
        onChange={(e) => handleFilterChange('analysisType', e.target.value || undefined)}
      >
        <option value="">All Analysis Types</option>
        <option value="anomaly_detection">Anomaly Detection</option>
        <option value="threshold_alert">Threshold Alert</option>
        <option value="performance_alert">Performance Alert</option>
      </select>

      <select
        className="rounded-md border-gray-300 bg-white text-gray-900 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 py-2 px-3 font-medium"
        value={currentFilters.metricAffected || ''}
        onChange={(e) => handleFilterChange('metricAffected', e.target.value || undefined)}
      >
        <option value="">All Metrics</option>
        <option value="ctr">CTR</option>
        <option value="cpc">CPC</option>
        <option value="conversion_rate">Conversion Rate</option>
        <option value="spend">Spend</option>
      </select>

      <div className="flex gap-2 items-center">
        <input
          type="date"
          className="rounded-md border-gray-300 bg-white text-gray-900 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 py-2 px-3 font-medium"
          value={currentFilters.dateRange?.start || ''}
          onChange={(e) =>
            handleFilterChange('dateRange', {
              ...currentFilters.dateRange,
              start: e.target.value || undefined,
            })
          }
        />
        <span>to</span>
        <input
          type="date"
          className="rounded-md border-gray-300 bg-white text-gray-900 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 py-2 px-3 font-medium"
          value={currentFilters.dateRange?.end || ''}
          onChange={(e) =>
            handleFilterChange('dateRange', {
              ...currentFilters.dateRange,
              end: e.target.value || undefined,
            })
          }
        />
      </div>
    </div>
  );
}

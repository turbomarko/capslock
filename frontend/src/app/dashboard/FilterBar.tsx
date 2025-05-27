import { FilterOptions } from '@/types/analysis';
import { Dropdown, DatePicker } from '@/components/form';

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

  const severityOptions = [
    { value: 'critical', label: 'Critical' },
    { value: 'high', label: 'High' },
    { value: 'medium', label: 'Medium' },
    { value: 'low', label: 'Low' },
  ];

  const analysisTypeOptions = [
    { value: 'anomaly_detection', label: 'Anomaly Detection' },
    { value: 'threshold_alert', label: 'Threshold Alert' },
    { value: 'performance_alert', label: 'Performance Alert' },
  ];

  const metricOptions = [
    { value: 'ctr', label: 'CTR' },
    { value: 'cpc', label: 'CPC' },
    { value: 'conversion_rate', label: 'Conversion Rate' },
    { value: 'spend', label: 'Spend' },
  ];

  return (
    <div className="flex flex-wrap gap-4 items-center">
      <Dropdown
        value={currentFilters.severity || ''}
        onChange={(value) => handleFilterChange('severity', value)}
        options={severityOptions}
        placeholder="All Severities"
      />

      <Dropdown
        value={currentFilters.analysisType || ''}
        onChange={(value) => handleFilterChange('analysisType', value)}
        options={analysisTypeOptions}
        placeholder="All Analysis Types"
      />

      <Dropdown
        value={currentFilters.metricAffected || ''}
        onChange={(value) => handleFilterChange('metricAffected', value)}
        options={metricOptions}
        placeholder="All Metrics"
      />

      <div className="flex gap-2 items-center">
        <DatePicker
          value={currentFilters.dateRange?.start || ''}
          onChange={(value) =>
            handleFilterChange('dateRange', {
              ...currentFilters.dateRange,
              start: value,
            })
          }
        />
        <span>to</span>
        <DatePicker
          value={currentFilters.dateRange?.end || ''}
          onChange={(value) =>
            handleFilterChange('dateRange', {
              ...currentFilters.dateRange,
              end: value,
            })
          }
        />
      </div>
    </div>
  );
}

import { Fragment } from 'react';
import { Menu, Transition, MenuButton, MenuItems } from '@headlessui/react';
import { FunnelIcon } from '@heroicons/react/24/outline';
import { FilterOptions } from '@/types/analysis';

interface FilterBarProps {
  onFilterChange: (filters: FilterOptions) => void;
  currentFilters: FilterOptions;
}

export function FilterBar({ onFilterChange, currentFilters }: FilterBarProps) {
  const significanceOptions = ['high', 'medium', 'low'] as const;
  const categoryOptions = ['Navigation', 'Editing', 'System', 'Custom'] as const;

  const handleDateChange = (field: 'start' | 'end', value: string) => {
    const newDateRange = {
      ...currentFilters.dateRange,
      [field]: value,
    };
    
    // Only update if both dates are present
    if (newDateRange.start && newDateRange.end) {
      onFilterChange({
        ...currentFilters,
        dateRange: newDateRange as { start: string; end: string },
      });
    } else {
      onFilterChange({
        ...currentFilters,
        dateRange: undefined,
      });
    }
  };

  return (
    <div className="flex items-center space-x-4 p-4 bg-white border-b">
      <div className="flex-1">
        <input
          type="text"
          placeholder="Search..."
          className="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
          value={currentFilters.search || ''}
          onChange={(e) => onFilterChange({ ...currentFilters, search: e.target.value })}
        />
      </div>

      <Menu as="div" className="relative">
        <MenuButton className="flex items-center px-4 py-2 text-sm font-medium text-gray-700 bg-white border rounded-lg hover:bg-gray-50">
          <FunnelIcon className="w-5 h-5 mr-2" />
          Filters
        </MenuButton>

        <Transition
          as={Fragment}
          enter="transition ease-out duration-100"
          enterFrom="transform opacity-0 scale-95"
          enterTo="transform opacity-100 scale-100"
          leave="transition ease-in duration-75"
          leaveFrom="transform opacity-100 scale-100"
          leaveTo="transform opacity-0 scale-95"
        >
          <MenuItems className="absolute right-0 z-10 mt-2 w-56 origin-top-right rounded-md bg-white shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none">
            <div className="p-4">
              <div className="mb-4">
                <label className="block text-sm font-medium text-gray-700">Significance</label>
                <select
                  className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
                  value={currentFilters.significance || ''}
                  onChange={(e) => onFilterChange({ ...currentFilters, significance: e.target.value as any })}
                >
                  <option value="">All</option>
                  {significanceOptions.map((option) => (
                    <option key={option} value={option}>
                      {option.charAt(0).toUpperCase() + option.slice(1)}
                    </option>
                  ))}
                </select>
              </div>

              <div className="mb-4">
                <label className="block text-sm font-medium text-gray-700">Category</label>
                <select
                  className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
                  value={currentFilters.category || ''}
                  onChange={(e) => onFilterChange({ ...currentFilters, category: e.target.value })}
                >
                  <option value="">All</option>
                  {categoryOptions.map((option) => (
                    <option key={option} value={option}>
                      {option}
                    </option>
                  ))}
                </select>
              </div>

              <div className="mb-4">
                <label className="block text-sm font-medium text-gray-700">Date Range</label>
                <div className="mt-1 grid grid-cols-2 gap-2">
                  <input
                    type="date"
                    className="block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
                    value={currentFilters.dateRange?.start || ''}
                    onChange={(e) => handleDateChange('start', e.target.value)}
                  />
                  <input
                    type="date"
                    className="block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
                    value={currentFilters.dateRange?.end || ''}
                    onChange={(e) => handleDateChange('end', e.target.value)}
                  />
                </div>
              </div>
            </div>
          </MenuItems>
        </Transition>
      </Menu>
    </div>
  );
} 
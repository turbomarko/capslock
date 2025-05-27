import { ChangeEvent } from 'react';

interface DropdownOption {
  value: string;
  label: string;
}

interface DropdownProps {
  value: string;
  onChange: (value: string | undefined) => void;
  options: DropdownOption[];
  placeholder: string;
}

export function Dropdown({ value, onChange, options, placeholder }: DropdownProps) {
  const handleChange = (e: ChangeEvent<HTMLSelectElement>) => {
    onChange(e.target.value || undefined);
  };

  return (
    <select
      className="w-full rounded-md border-gray-300 bg-white text-gray-900 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 py-1.5 px-2 sm:py-2 sm:px-3 text-sm sm:text-base font-medium"
      value={value || ''}
      onChange={handleChange}
    >
      <option value="">{placeholder}</option>
      {options.map((option) => (
        <option key={option.value} value={option.value}>
          {option.label}
        </option>
      ))}
    </select>
  );
} 
import { ChangeEvent } from 'react';

interface DatePickerProps {
  value: string;
  onChange: (value: string | undefined) => void;
}

export function DatePicker({ value, onChange }: DatePickerProps) {
  const handleChange = (e: ChangeEvent<HTMLInputElement>) => {
    onChange(e.target.value || undefined);
  };

  return (
    <input
      type="date"
      className="w-full rounded-md border-gray-300 bg-white text-gray-900 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 py-1.5 px-2 sm:py-2 sm:px-3 text-sm sm:text-base font-medium"
      value={value || ''}
      onChange={handleChange}
    />
  );
}

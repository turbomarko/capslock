import { AnalysisResult, FilterOptions } from "@/types/analysis";

import baseApi from "../api";

const api = baseApi.injectEndpoints({
  endpoints: (builder) => ({
    getAnalytics: builder.query<AnalysisResult[], FilterOptions>({
      query: (filters) => {
        const params: Record<string, string> = {};
        
        // Handle regular filters
        Object.entries(filters).forEach(([key, value]) => {
          if (value && key !== 'dateRange') {
            params[key] = value;
          }
        });

        // Handle date range separately due to nested structure
        if (filters.dateRange?.start) {
          params['dateRange.start'] = filters.dateRange.start;
        }
        if (filters.dateRange?.end) {
          params['dateRange.end'] = filters.dateRange.end;
        }
        
        return {
          url: "/analytics/",
          params,
        };
      },
    }),
  }),
  overrideExisting: false,
});

export const {
  useGetAnalyticsQuery,
} = api;

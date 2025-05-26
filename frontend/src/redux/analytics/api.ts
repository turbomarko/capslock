import { AnalysisResult } from "@/types/analysis";

import baseApi from "../api";

const api = baseApi.injectEndpoints({
  endpoints: (builder) => ({
    getAnalytics: builder.query<AnalysisResult[], void>({
      query: () => "/analytics/",
    }),
  }),
  overrideExisting: false,
});

export const {
  useGetAnalyticsQuery,
} = api;

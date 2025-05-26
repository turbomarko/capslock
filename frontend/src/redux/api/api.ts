import { createApi, fetchBaseQuery } from "@reduxjs/toolkit/query/react";

// initialize an empty api service that we'll inject endpoints into later as needed
const api = createApi({
  baseQuery: fetchBaseQuery({ 
    baseUrl: "http://localhost:8000",
    paramsSerializer: (params) => {
      const searchParams = new URLSearchParams();
      Object.entries(params).forEach(([key, value]) => {
        if (value !== undefined && value !== null) {
          searchParams.append(key, value.toString());
        }
      });
      return searchParams.toString();
    },
  }),
  endpoints: () => ({}),
});

export default api;

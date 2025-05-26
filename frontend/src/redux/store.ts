import { configureStore } from "@reduxjs/toolkit";
import {
  persistStore,
  Persistor,
  FLUSH,
  REHYDRATE,
  PAUSE,
  PERSIST,
  PURGE,
  REGISTER,
} from 'redux-persist';
import { createLogger } from 'redux-logger';

import rootReducer from './rootReducer';
import api from './api';

// Setting up the middlewares
const setMiddlewares = () => {
  const middlewares = [];

  // Adding the api middleware enables caching, invalidation, polling,
  middlewares.push(api.middleware);

  // Setting up redux logger only for development
  if (process.env.NODE_ENV === 'development') {
    const loggerOptions = {
      collapsed: true,
      // eslint-disable-next-line
      titleFormatter: (action: any, time: string, took: number) => {
        return `${action.type} -> ${time} --> ${took.toFixed(2)} ms`;
      }
    };
    const logger = createLogger(loggerOptions);
    middlewares.push(logger);
  }

  return middlewares;
};

export const store = configureStore({
  reducer: rootReducer,
  middleware: (getDefaultMiddleware) =>
    getDefaultMiddleware({
      serializableCheck: {
        ignoredActions: [FLUSH, REHYDRATE, PAUSE, PERSIST, PURGE, REGISTER],
      }
    }).concat(setMiddlewares()),
});

export const persistor: Persistor = persistStore(store);

export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;

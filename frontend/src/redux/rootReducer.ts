import { persistCombineReducers } from 'redux-persist';
import storage from 'redux-persist/lib/storage';

import api from './api';

export const config = {
  key: 'root',
  storage,
  timeout: 10000
};

const rootReducer = persistCombineReducers(config, {
  [api.reducerPath]: api.reducer,
});

export default rootReducer;

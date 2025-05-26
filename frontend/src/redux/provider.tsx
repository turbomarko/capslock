"use client";

import { PersistGate } from 'redux-persist/integration/react';

import { store, persistor } from './store';
import { Provider as ReduxProvider } from "react-redux";

const Provider = ({ children }: { children: React.ReactNode }) => {
  return (
    <ReduxProvider store={store}>
      <PersistGate loading={null} persistor={persistor}>
        {children}
      </PersistGate>
    </ReduxProvider>
  );
}

export default Provider;

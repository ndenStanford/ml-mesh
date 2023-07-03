import { configureStore } from "@reduxjs/toolkit";
import { persistStore, persistReducer } from "redux-persist";
import storage from "redux-persist/lib/storage";
import { combineReducers } from "redux";
import appReducer from "./slices/app";
import modalsReducer from "./slices/modals";
import promptsReducer from "./slices/prompts";
import modelsReducer from "./slices/models";
import chatReducer from "./slices/chat";

const persistConfig = {
  key: "root",
  storage,
};

const globalReducer = combineReducers({
  app: appReducer,
  prompts: promptsReducer,
  modals: modalsReducer,
  chat: chatReducer,
  models: modelsReducer,
});

const persistedReducer = persistReducer(persistConfig, globalReducer);

export const store = configureStore({
  reducer: persistedReducer,
  devTools: process.env.NODE_ENV !== "production",
  middleware: (getDefaultMiddleware) =>
    getDefaultMiddleware({ serializableCheck: false }),
});

export const persistor = persistStore(store);

export type GlobalDispatch = typeof store.dispatch;
export type GlobalState = ReturnType<typeof store.getState>;

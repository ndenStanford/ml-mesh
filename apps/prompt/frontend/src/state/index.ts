import { configureStore } from "@reduxjs/toolkit";
import { persistStore, persistReducer } from "redux-persist";
import storage from "redux-persist/lib/storage";
import { combineReducers } from "redux";
import {
  useDispatch,
  TypedUseSelectorHook,
  useSelector as rawUseSelector,
} from "react-redux";
import appReducer from "./slices/app";
import promptsReducer from "./slices/prompts";
import thunk from "redux-thunk";

const persistConfig = {
  key: "root",
  storage,
};

const rootReducer = combineReducers({
  app: appReducer,
  prompts: promptsReducer,
});

const persistedReducer = persistReducer(persistConfig, rootReducer);

export const store = configureStore({
  reducer: persistedReducer,
  devTools: process.env.NODE_ENV !== "production",
  middleware: [thunk],
});

export const persistor = persistStore(store);

export type GlobalDispatch = typeof store.dispatch;
export type GlobalState = ReturnType<typeof store.getState>;

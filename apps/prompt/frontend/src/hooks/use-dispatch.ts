import { TypedUseSelectorHook, useDispatch, useSelector } from "react-redux";
import type { GlobalState, GlobalDispatch } from "../state";

// Use throughout your app instead of plain `useDispatch` and `useSelector`
export const useGlobalDispatch = () => useDispatch<GlobalDispatch>();
export const useGlobalSelector: TypedUseSelectorHook<GlobalState> = useSelector;

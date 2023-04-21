import { createSlice } from "@reduxjs/toolkit";
import { DEFAULT_THEME } from "../../constants";
import { AppState } from "@/src/types";
import { updateTheme } from "../../utils";

const appSlice = createSlice({
  name: "app",
  initialState: {
    theme: DEFAULT_THEME,
    showToast: false,
  } as AppState,
  reducers: {
    switchTheme: (state) => {
      return {
        ...state,
        theme: updateTheme(state.theme),
      };
    },
    showToast: (state) => {
      return {
        ...state,
        showToast: true,
      };
    },
    hideToast: (state) => {
      return {
        ...state,
        showToast: false,
      };
    },
  },
});

export const { switchTheme, showToast, hideToast } = appSlice.actions;
const appReducer = appSlice.reducer;
export default appReducer;

import { createSlice } from "@reduxjs/toolkit";
import { DEFAULT_THEME } from "../../constants";
import { AppState } from "@/src/types";
import { updateTheme } from "../../utils";

const appSlice = createSlice({
  name: "app",
  initialState: {
    theme: DEFAULT_THEME,
  } as AppState,
  reducers: {
    switchTheme: (state) => {
      return {
        ...state,
        theme: updateTheme(state.theme),
      };
    },
  },
});

export const { switchTheme } = appSlice.actions;
const appReducer = appSlice.reducer;
export default appReducer;

import { createSlice, PayloadAction } from "@reduxjs/toolkit";
import { ModalsState } from "@/src/types";

const modalsSlice = createSlice({
  name: "modals",
  initialState: {
    list: {},
  } as ModalsState,
  reducers: {
    showModal: (state, action: PayloadAction<string>) => {
      state.list[action.payload] = true;
    },
    hideModal: (state, action: PayloadAction<string>) => {
      state.list[action.payload] = false;
    },
    addModal: (state, action: PayloadAction<string>) => {
      state.list[action.payload] = false;
    },
  },
});

export const { showModal, hideModal, addModal } = modalsSlice.actions;
const modalsReducer = modalsSlice.reducer;
export default modalsReducer;

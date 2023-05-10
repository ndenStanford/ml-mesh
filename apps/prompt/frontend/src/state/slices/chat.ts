import { createSlice, PayloadAction } from "@reduxjs/toolkit";
import { ChatState, Message } from "@/src/types";

const chatSlice = createSlice({
  name: "chat",
  initialState: {
    messages: {},
  } as ChatState,
  reducers: {
    addMessage: (state, action: PayloadAction<Message>) => {
      state.messages[action.payload.id] = action.payload;
    },
    clearMessages: (state) => {
      return {
        ...state,
        messages: {},
      };
    },
    setIsLoading(state, action: PayloadAction<Message>) {
      state.messages[action.payload.id].isLoading = true;
    },
    setHasFinishedLoading(state, action: PayloadAction<Message>) {
      state.messages[action.payload.id].isLoading = false;
    },
  },
});

export const {
  addMessage,
  clearMessages,
  setIsLoading,
  setHasFinishedLoading,
} = chatSlice.actions;
const chatReducer = chatSlice.reducer;
export default chatReducer;

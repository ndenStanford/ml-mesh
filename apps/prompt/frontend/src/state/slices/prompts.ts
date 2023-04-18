import { createAsyncThunk, createSlice } from "@reduxjs/toolkit";
import { PromptListItemProps, PromptsState } from "@/src/types";
import { API_URI, API_KEY } from "../../constants";
import { GlobalState } from "..";

export const getPrompts = createAsyncThunk("prompts/list", async () => {
  const response = await fetch(`${API_URI}/prompts`, {
    method: "GET",
    headers: {
      accept: "application/json",
      "x-api-key": API_KEY,
    },
  });
  const jsonResponse = await response.json();
  const promptItems = jsonResponse.prompts.map(
    (prompt: PromptListItemProps) => {
      const promptItem = {
        id: prompt.id,
        alias: prompt.alias,
        template: prompt.template,
        time: prompt.created_at,
        selected: prompt.selected,
      };
      return promptItem;
    }
  );
  return promptItems;
});

const promptsSlice = createSlice({
  name: "prompts",
  initialState: {
    list: [],
  } as PromptsState,
  reducers: {},
  extraReducers: (builder) => {
    builder.addCase(getPrompts.fulfilled, (state, action) => {
      if (action.payload) {
        state.list = action.payload;
      }
    });
  },
});

export const listPrompts = (state: GlobalState) => state.prompts.list;
const promptsReducer = promptsSlice.reducer;
export default promptsReducer;

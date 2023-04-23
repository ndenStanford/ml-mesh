import { createAsyncThunk, createSlice } from "@reduxjs/toolkit";
import { PromptListItemProps, PromptsState } from "@/src/types";
import { API_URI, API_KEY } from "../../constants";

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
        variables: prompt.variables,
        created_at: prompt.created_at,
        selected: prompt.selected,
      };
      return promptItem;
    }
  );
  return promptItems;
});

export const createPrompt = createAsyncThunk(
  "prompts/create",
  async (template: string) => {
    const response = await fetch(`${API_URI}/prompts?template=${template}`, {
      method: "POST",
      headers: {
        accept: "application/json",
        "x-api-key": API_KEY,
      },
    });
    if (response.status !== 201) {
      console.log("Error fetching");
    }
    console.log("Successfully created new prompt.");
  }
);

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

const promptsReducer = promptsSlice.reducer;
export default promptsReducer;

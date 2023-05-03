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
  async ({ template, alias }: { template: string; alias: string }) => {
    const response = await fetch(
      `${API_URI}/prompts?template=${template}&alias=${alias}`,
      {
        method: "POST",
        headers: {
          accept: "application/json",
          "x-api-key": API_KEY,
        },
      }
    );
    if (response.status !== 201) {
      // if (response.status == 409) {

      // }
      console.log("Error fetching");
    }
    console.log("Successfully created new prompt.");
  }
);

export const generateTextFromPrompt = createAsyncThunk(
  "prompts/generate/prompt",
  async (
    { prompt_id, body }: { prompt_id: string; body: any },
    thunkAPI: any
  ) => {
    const response = await fetch(`${API_URI}/prompts/${prompt_id}/generate`, {
      method: "POST",
      headers: {
        accept: "application/json",
        "x-api-key": API_KEY,
        "Content-Type": "application/json",
      },
      body: JSON.stringify(body),
    });
    if (response.status !== 200) {
      console.log("Error generating text");
    }
    console.log("Successfully generated text.");
    const jsonResponse = await response.json();
    return jsonResponse;
  }
);

export const generateText = createAsyncThunk(
  "prompts/generate/string",
  async (prompt: string) => {
    const response = await fetch(`${API_URI}/prompts/generate/${prompt}`, {
      method: "GET",
      headers: {
        accept: "application/json",
        "x-api-key": API_KEY,
      },
    });
    if (response.status !== 200) {
      console.log("Error generating text");
      return;
    }
    console.log("Successfully generated text.");
    const jsonResponse = await response.json();
    return jsonResponse["generated"];
  }
);

const promptsSlice = createSlice({
  name: "prompts",
  initialState: {
    list: [],
  } as PromptsState,
  reducers: {
    updateState: (state, action) => {
      return {
        ...state,
        list: state.list,
      };
    },
  },
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

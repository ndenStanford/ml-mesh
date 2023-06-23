import { createAsyncThunk, createSlice } from "@reduxjs/toolkit";
import {
  ModelListItemProps,
  PromptListItemProps,
  PromptsState,
} from "@/src/types";
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
  async (
    { template, alias }: { template: string; alias: string },
    thunkAPI: any
  ) => {
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
      console.log("Error fetching");
    }
    if (response.status == 409) {
      console.log("409 Conflict, alias exists in database");
      return thunkAPI.rejectWithValue({
        message: "409",
      });
    }
    console.log("Successfully created new prompt.");
  }
);

export const deletePrompt = createAsyncThunk(
  "prompts/delete",
  async ({ alias }: { alias: string }, thunkAPI: any) => {
    const response = await fetch(`${API_URI}/prompts/${alias}`, {
      method: "DELETE",
      headers: {
        accept: "application/json",
        "x-api-key": API_KEY,
      },
    });
    if (response.status !== 200) {
      console.log("Error Deleting");
    } else {
      console.log("Successfully deleted prompt.");
    }
  }
);

export const generateTextFromPrompt = createAsyncThunk(
  "prompts/generate/prompt",
  async (
    { alias, body, modelName }: { alias: string; body: any; modelName: string },
    thunkAPI: any
  ) => {
    var suffix = "";
    if (modelName != "gpt-3.5-turbo") {
      suffix = `prompts/${alias}/generate/model/${modelName}`;
    } else {
      suffix = `prompts/${alias}/generate`;
    }
    const response = await fetch(`${API_URI}/${suffix}`, {
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
  async (
    { prompt, modelName }: { prompt: string; modelName: string },
    thunkAPI: any
  ) => {
    var suffix = "";
    if (modelName != "gpt-3.5-turbo") {
      suffix = `prompts/generate/${prompt}/model/${modelName}`;
    } else {
      suffix = `prompts/generate/${prompt}`;
    }
    const response = await fetch(`${API_URI}/${suffix}`, {
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

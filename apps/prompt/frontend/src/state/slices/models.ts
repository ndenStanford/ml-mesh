import { createAsyncThunk, createSlice } from "@reduxjs/toolkit";
import { ModelListItemProps, ModelsState } from "@/src/types";
import { API_URI, API_KEY } from "../../constants";

export const getModels = createAsyncThunk("models/list", async () => {
  const response = await fetch(`${API_URI}/models`, {
    method: "GET",
    headers: {
      accept: "application/json",
      "x-api-key": API_KEY,
    },
  });
  const jsonResponse = await response.json();
  const modelItems = jsonResponse.models.map((model: ModelListItemProps) => {
    const modelItem = {
      id: model.id,
      model_name: model.model_name,
      parameters: model.parameters,
      created_at: model.created_at,
      selected: model.selected,
    };
    return modelItem;
  });
  return modelItems;
});

const modelsSlice = createSlice({
  name: "models",
  initialState: {
    list: [],
  } as ModelsState,
  reducers: {
    updateState: (state, action) => {
      return {
        ...state,
        list: state.list,
      };
    },
  },
  extraReducers: (builder) => {
    builder.addCase(getModels.fulfilled, (state, action) => {
      if (action.payload) {
        state.list = action.payload;
      }
    });
  },
});

const modelsReducer = modelsSlice.reducer;
export default modelsReducer;

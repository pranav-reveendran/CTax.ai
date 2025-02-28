import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import chatService from '../../services/chatService';

const initialState = {
  conversations: [],
  currentConversation: null,
  messages: [],
  isLoading: false,
  isError: false,
  message: '',
};

// Create new conversation
export const createConversation = createAsyncThunk(
  'chat/createConversation',
  async (conversationData, thunkAPI) => {
    try {
      const token = thunkAPI.getState().auth.token;
      return await chatService.createConversation(conversationData, token);
    } catch (error) {
      const message =
        (error.response && error.response.data && error.response.data.message) ||
        error.message ||
        error.toString();
      return thunkAPI.rejectWithValue(message);
    }
  }
);

// Get all conversations
export const getConversations = createAsyncThunk(
  'chat/getConversations',
  async (_, thunkAPI) => {
    try {
      const token = thunkAPI.getState().auth.token;
      return await chatService.getConversations(token);
    } catch (error) {
      const message =
        (error.response && error.response.data && error.response.data.message) ||
        error.message ||
        error.toString();
      return thunkAPI.rejectWithValue(message);
    }
  }
);

// Get single conversation
export const getConversation = createAsyncThunk(
  'chat/getConversation',
  async (conversationId, thunkAPI) => {
    try {
      const token = thunkAPI.getState().auth.token;
      return await chatService.getConversation(conversationId, token);
    } catch (error) {
      const message =
        (error.response && error.response.data && error.response.data.message) ||
        error.message ||
        error.toString();
      return thunkAPI.rejectWithValue(message);
    }
  }
);

// Send message
export const sendMessage = createAsyncThunk(
  'chat/sendMessage',
  async ({ conversationId, message }, thunkAPI) => {
    try {
      const token = thunkAPI.getState().auth.token;
      return await chatService.sendMessage(conversationId, message, token);
    } catch (error) {
      const message =
        (error.response && error.response.data && error.response.data.message) ||
        error.message ||
        error.toString();
      return thunkAPI.rejectWithValue(message);
    }
  }
);

const chatSlice = createSlice({
  name: 'chat',
  initialState,
  reducers: {
    reset: (state) => {
      state.isLoading = false;
      state.isError = false;
      state.message = '';
    },
    setCurrentConversation: (state, action) => {
      state.currentConversation = action.payload;
    },
  },
  extraReducers: (builder) => {
    builder
      // Create conversation
      .addCase(createConversation.pending, (state) => {
        state.isLoading = true;
      })
      .addCase(createConversation.fulfilled, (state, action) => {
        state.isLoading = false;
        state.conversations.push(action.payload);
        state.currentConversation = action.payload;
      })
      .addCase(createConversation.rejected, (state, action) => {
        state.isLoading = false;
        state.isError = true;
        state.message = action.payload;
      })
      // Get conversations
      .addCase(getConversations.pending, (state) => {
        state.isLoading = true;
      })
      .addCase(getConversations.fulfilled, (state, action) => {
        state.isLoading = false;
        state.conversations = action.payload;
      })
      .addCase(getConversations.rejected, (state, action) => {
        state.isLoading = false;
        state.isError = true;
        state.message = action.payload;
      })
      // Get conversation
      .addCase(getConversation.pending, (state) => {
        state.isLoading = true;
      })
      .addCase(getConversation.fulfilled, (state, action) => {
        state.isLoading = false;
        state.currentConversation = action.payload;
        state.messages = action.payload.messages || [];
      })
      .addCase(getConversation.rejected, (state, action) => {
        state.isLoading = false;
        state.isError = true;
        state.message = action.payload;
      })
      // Send message
      .addCase(sendMessage.pending, (state) => {
        state.isLoading = true;
      })
      .addCase(sendMessage.fulfilled, (state, action) => {
        state.isLoading = false;
        // Add new messages to the current conversation
        if (state.currentConversation) {
          state.messages.push({
            role: 'user',
            content: action.payload.query,
          });
          state.messages.push({
            role: 'assistant',
            content: action.payload.message,
            sources: action.payload.sources,
          });
        }
      })
      .addCase(sendMessage.rejected, (state, action) => {
        state.isLoading = false;
        state.isError = true;
        state.message = action.payload;
      });
  },
});

export const { reset, setCurrentConversation } = chatSlice.actions;
export default chatSlice.reducer;

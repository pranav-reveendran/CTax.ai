import React, { useState, useEffect, useRef } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { useParams } from 'react-router-dom';
import {
  Container,
  Box,
  Paper,
  TextField,
  Button,
  Typography,
  CircularProgress,
  Card,
  CardContent,
  Chip,
  Stack,
} from '@mui/material';
import { Send } from '@mui/icons-material';
import { getConversation, sendMessage } from '../redux/slices/chatSlice';

const Chat = () => {
  const { id } = useParams();
  const dispatch = useDispatch();
  const [input, setInput] = useState('');
  const messagesEndRef = useRef(null);

  const { currentConversation, messages, isLoading } = useSelector(
    (state) => state.chat
  );

  useEffect(() => {
    if (id) {
      dispatch(getConversation(id));
    }
  }, [id, dispatch]);

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!input.trim()) return;

    const userMessage = input;
    setInput('');

    await dispatch(
      sendMessage({
        conversationId: id,
        message: userMessage,
      })
    );
  };

  return (
    <Container maxWidth="md" sx={{ height: 'calc(100vh - 100px)', display: 'flex', flexDirection: 'column', py: 2 }}>
      <Paper elevation={3} sx={{ flexGrow: 1, display: 'flex', flexDirection: 'column', overflow: 'hidden' }}>
        {/* Chat Header */}
        <Box sx={{ p: 2, borderBottom: 1, borderColor: 'divider' }}>
          <Typography variant="h6">
            {currentConversation?.title || 'Loading...'}
          </Typography>
          {currentConversation?.context && (
            <Typography variant="body2" color="text.secondary">
              {currentConversation.context.visaType} | Tax Year: {currentConversation.context.taxYear}
            </Typography>
          )}
        </Box>

        {/* Messages Area */}
        <Box
          sx={{
            flexGrow: 1,
            overflow: 'auto',
            p: 2,
            display: 'flex',
            flexDirection: 'column',
            gap: 2,
          }}
        >
          {messages && messages.length > 0 ? (
            messages.map((message, index) => (
              <Box
                key={index}
                sx={{
                  display: 'flex',
                  justifyContent: message.role === 'user' ? 'flex-end' : 'flex-start',
                }}
              >
                <Card
                  sx={{
                    maxWidth: '70%',
                    bgcolor: message.role === 'user' ? 'primary.main' : 'background.paper',
                    color: message.role === 'user' ? 'white' : 'text.primary',
                  }}
                >
                  <CardContent>
                    <Typography variant="body1" sx={{ whiteSpace: 'pre-wrap' }}>
                      {message.content}
                    </Typography>
                    {message.sources && message.sources.length > 0 && (
                      <Box sx={{ mt: 2 }}>
                        <Typography variant="caption" color="text.secondary" display="block" gutterBottom>
                          Sources:
                        </Typography>
                        <Stack direction="row" spacing={1} flexWrap="wrap">
                          {message.sources.map((source, idx) => (
                            <Chip
                              key={idx}
                              label={`${source.documentName} (p.${source.pageNumber})`}
                              size="small"
                              variant="outlined"
                              sx={{ mt: 0.5 }}
                            />
                          ))}
                        </Stack>
                      </Box>
                    )}
                  </CardContent>
                </Card>
              </Box>
            ))
          ) : (
            <Box sx={{ textAlign: 'center', mt: 4 }}>
              <Typography variant="body1" color="text.secondary">
                No messages yet. Start by asking a question about California taxes!
              </Typography>
            </Box>
          )}
          {isLoading && (
            <Box sx={{ display: 'flex', justifyContent: 'center' }}>
              <CircularProgress size={24} />
            </Box>
          )}
          <div ref={messagesEndRef} />
        </Box>

        {/* Input Area */}
        <Box
          component="form"
          onSubmit={handleSubmit}
          sx={{
            p: 2,
            borderTop: 1,
            borderColor: 'divider',
            display: 'flex',
            gap: 1,
          }}
        >
          <TextField
            fullWidth
            placeholder="Ask a question about California taxes..."
            value={input}
            onChange={(e) => setInput(e.target.value)}
            disabled={isLoading}
            multiline
            maxRows={4}
          />
          <Button
            type="submit"
            variant="contained"
            endIcon={<Send />}
            disabled={isLoading || !input.trim()}
          >
            Send
          </Button>
        </Box>
      </Paper>
    </Container>
  );
};

export default Chat;

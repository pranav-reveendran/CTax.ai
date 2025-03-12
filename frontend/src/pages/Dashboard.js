import React, { useEffect } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { useNavigate } from 'react-router-dom';
import {
  Container,
  Box,
  Typography,
  Button,
  Grid,
  Card,
  CardContent,
  CardActions,
  IconButton,
  CircularProgress,
} from '@mui/material';
import { Add, Chat as ChatIcon, Delete } from '@mui/icons-material';
import {
  getConversations,
  createConversation,
} from '../redux/slices/chatSlice';

const Dashboard = () => {
  const dispatch = useDispatch();
  const navigate = useNavigate();
  const { user } = useSelector((state) => state.auth);
  const { conversations, isLoading } = useSelector((state) => state.chat);

  useEffect(() => {
    dispatch(getConversations());
  }, [dispatch]);

  const handleNewConversation = async () => {
    const result = await dispatch(
      createConversation({
        title: 'New Conversation',
        visaType: user?.visaType,
      })
    );

    if (result.payload && result.payload._id) {
      navigate(`/chat/${result.payload._id}`);
    }
  };

  const handleOpenConversation = (id) => {
    navigate(`/chat/${id}`);
  };

  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 4 }}>
        <Box>
          <Typography variant="h4" gutterBottom>
            Welcome, {user?.name}!
          </Typography>
          <Typography variant="body1" color="text.secondary">
            Visa Type: {user?.visaType} | Tax Year: {new Date().getFullYear()}
          </Typography>
        </Box>
        <Button
          variant="contained"
          startIcon={<Add />}
          onClick={handleNewConversation}
          size="large"
        >
          New Conversation
        </Button>
      </Box>

      <Typography variant="h5" gutterBottom sx={{ mt: 4 }}>
        Your Conversations
      </Typography>

      {isLoading ? (
        <Box sx={{ display: 'flex', justifyContent: 'center', mt: 4 }}>
          <CircularProgress />
        </Box>
      ) : conversations && conversations.length > 0 ? (
        <Grid container spacing={3} sx={{ mt: 2 }}>
          {conversations.map((conversation) => (
            <Grid item xs={12} sm={6} md={4} key={conversation._id}>
              <Card>
                <CardContent>
                  <Typography variant="h6" gutterBottom>
                    {conversation.title}
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    Messages: {conversation.metadata?.totalMessages || 0}
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    Last active: {new Date(conversation.updatedAt).toLocaleDateString()}
                  </Typography>
                </CardContent>
                <CardActions>
                  <Button
                    size="small"
                    startIcon={<ChatIcon />}
                    onClick={() => handleOpenConversation(conversation._id)}
                  >
                    Open
                  </Button>
                </CardActions>
              </Card>
            </Grid>
          ))}
        </Grid>
      ) : (
        <Box sx={{ textAlign: 'center', mt: 4 }}>
          <Typography variant="body1" color="text.secondary" gutterBottom>
            No conversations yet. Start a new conversation to get help with California tax questions!
          </Typography>
          <Button
            variant="outlined"
            startIcon={<Add />}
            onClick={handleNewConversation}
            sx={{ mt: 2 }}
          >
            Start Your First Conversation
          </Button>
        </Box>
      )}
    </Container>
  );
};

export default Dashboard;

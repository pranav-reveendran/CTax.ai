const Conversation = require('../models/Conversation');
const logger = require('../utils/logger');
const axios = require('axios');

// @desc    Create new conversation
// @route   POST /api/chat/conversations
// @access  Private
exports.createConversation = async (req, res) => {
  try {
    const { title, visaType, taxYear } = req.body;

    const conversation = await Conversation.create({
      user: req.user.id,
      title: title || 'New Conversation',
      context: {
        visaType: visaType || req.user.visaType,
        taxYear: taxYear || new Date().getFullYear(),
        state: 'California',
      },
    });

    res.status(201).json({
      success: true,
      data: conversation,
    });
  } catch (error) {
    logger.error(`Create conversation error: ${error.message}`);
    res.status(500).json({
      success: false,
      message: 'Error creating conversation',
    });
  }
};

// @desc    Get all user conversations
// @route   GET /api/chat/conversations
// @access  Private
exports.getConversations = async (req, res) => {
  try {
    const conversations = await Conversation.find({
      user: req.user.id,
      isActive: true,
    })
      .sort({ updatedAt: -1 })
      .select('-messages');

    res.status(200).json({
      success: true,
      count: conversations.length,
      data: conversations,
    });
  } catch (error) {
    logger.error(`Get conversations error: ${error.message}`);
    res.status(500).json({
      success: false,
      message: 'Error fetching conversations',
    });
  }
};

// @desc    Get single conversation
// @route   GET /api/chat/conversations/:id
// @access  Private
exports.getConversation = async (req, res) => {
  try {
    const conversation = await Conversation.findOne({
      _id: req.params.id,
      user: req.user.id,
    });

    if (!conversation) {
      return res.status(404).json({
        success: false,
        message: 'Conversation not found',
      });
    }

    res.status(200).json({
      success: true,
      data: conversation,
    });
  } catch (error) {
    logger.error(`Get conversation error: ${error.message}`);
    res.status(500).json({
      success: false,
      message: 'Error fetching conversation',
    });
  }
};

// @desc    Send message and get RAG response
// @route   POST /api/chat/conversations/:id/messages
// @access  Private
exports.sendMessage = async (req, res) => {
  try {
    const { message } = req.body;

    if (!message) {
      return res.status(400).json({
        success: false,
        message: 'Message is required',
      });
    }

    const conversation = await Conversation.findOne({
      _id: req.params.id,
      user: req.user.id,
    });

    if (!conversation) {
      return res.status(404).json({
        success: false,
        message: 'Conversation not found',
      });
    }

    // Add user message to conversation
    conversation.messages.push({
      role: 'user',
      content: message,
      timestamp: new Date(),
    });

    // Call RAG service to get response
    try {
      const ragResponse = await axios.post(
        `${process.env.DOCUMENT_PROCESSOR_URL}/api/query`,
        {
          query: message,
          context: conversation.context,
          conversationHistory: conversation.messages.slice(-5), // Last 5 messages for context
        },
        {
          timeout: 30000, // 30 second timeout
        }
      );

      // Add assistant response to conversation
      conversation.messages.push({
        role: 'assistant',
        content: ragResponse.data.answer,
        sources: ragResponse.data.sources || [],
        timestamp: new Date(),
      });

      await conversation.save();

      res.status(200).json({
        success: true,
        data: {
          conversationId: conversation._id,
          message: ragResponse.data.answer,
          sources: ragResponse.data.sources || [],
        },
      });
    } catch (ragError) {
      logger.error(`RAG service error: ${ragError.message}`);

      // Fallback response if RAG service is unavailable
      const fallbackMessage = 'I apologize, but I\'m currently unable to process your request. Please try again later or contact support if the issue persists.';

      conversation.messages.push({
        role: 'assistant',
        content: fallbackMessage,
        timestamp: new Date(),
      });

      await conversation.save();

      res.status(200).json({
        success: true,
        data: {
          conversationId: conversation._id,
          message: fallbackMessage,
          sources: [],
          isError: true,
        },
      });
    }
  } catch (error) {
    logger.error(`Send message error: ${error.message}`);
    res.status(500).json({
      success: false,
      message: 'Error processing message',
    });
  }
};

// @desc    Delete conversation
// @route   DELETE /api/chat/conversations/:id
// @access  Private
exports.deleteConversation = async (req, res) => {
  try {
    const conversation = await Conversation.findOne({
      _id: req.params.id,
      user: req.user.id,
    });

    if (!conversation) {
      return res.status(404).json({
        success: false,
        message: 'Conversation not found',
      });
    }

    conversation.isActive = false;
    await conversation.save();

    res.status(200).json({
      success: true,
      data: {},
    });
  } catch (error) {
    logger.error(`Delete conversation error: ${error.message}`);
    res.status(500).json({
      success: false,
      message: 'Error deleting conversation',
    });
  }
};

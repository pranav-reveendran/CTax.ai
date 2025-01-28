const mongoose = require('mongoose');

const MessageSchema = new mongoose.Schema({
  role: {
    type: String,
    enum: ['user', 'assistant', 'system'],
    required: true,
  },
  content: {
    type: String,
    required: true,
  },
  sources: [{
    documentName: String,
    pageNumber: Number,
    excerpt: String,
    relevanceScore: Number,
  }],
  timestamp: {
    type: Date,
    default: Date.now,
  },
});

const ConversationSchema = new mongoose.Schema(
  {
    user: {
      type: mongoose.Schema.Types.ObjectId,
      ref: 'User',
      required: true,
    },
    title: {
      type: String,
      default: 'New Conversation',
      trim: true,
    },
    messages: [MessageSchema],
    context: {
      visaType: String,
      taxYear: Number,
      state: {
        type: String,
        default: 'California',
      },
    },
    isActive: {
      type: Boolean,
      default: true,
    },
    metadata: {
      totalMessages: {
        type: Number,
        default: 0,
      },
      lastMessageAt: Date,
    },
  },
  {
    timestamps: true,
  }
);

// Update metadata before saving
ConversationSchema.pre('save', function (next) {
  this.metadata.totalMessages = this.messages.length;
  if (this.messages.length > 0) {
    this.metadata.lastMessageAt = this.messages[this.messages.length - 1].timestamp;
  }
  next();
});

module.exports = mongoose.model('Conversation', ConversationSchema);

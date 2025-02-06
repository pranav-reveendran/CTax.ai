const express = require('express');
const {
  createConversation,
  getConversations,
  getConversation,
  sendMessage,
  deleteConversation,
} = require('../controllers/chatController');
const { protect } = require('../middleware/auth');

const router = express.Router();

// Protect all routes
router.use(protect);

router.route('/conversations')
  .get(getConversations)
  .post(createConversation);

router.route('/conversations/:id')
  .get(getConversation)
  .delete(deleteConversation);

router.post('/conversations/:id/messages', sendMessage);

module.exports = router;

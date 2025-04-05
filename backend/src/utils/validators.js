const { body, validationResult } = require('express-validator');

/**
 * Validation rules for user registration
 */
exports.registerValidation = [
  body('name').trim().notEmpty().withMessage('Name is required'),
  body('email').isEmail().withMessage('Valid email is required'),
  body('password')
    .isLength({ min: 6 })
    .withMessage('Password must be at least 6 characters'),
  body('visaType')
    .optional()
    .isIn(['F-1', 'J-1', 'H-1B', 'OPT', 'CPT', 'Other'])
    .withMessage('Invalid visa type'),
];

/**
 * Validation rules for user login
 */
exports.loginValidation = [
  body('email').isEmail().withMessage('Valid email is required'),
  body('password').notEmpty().withMessage('Password is required'),
];

/**
 * Validation rules for creating conversation
 */
exports.conversationValidation = [
  body('title').optional().trim(),
  body('visaType')
    .optional()
    .isIn(['F-1', 'J-1', 'H-1B', 'OPT', 'CPT', 'Other']),
  body('taxYear').optional().isInt({ min: 2020, max: 2030 }),
];

/**
 * Validation rules for sending message
 */
exports.messageValidation = [
  body('message')
    .trim()
    .notEmpty()
    .withMessage('Message is required')
    .isLength({ max: 5000 })
    .withMessage('Message too long'),
];

/**
 * Middleware to check validation results
 */
exports.validate = (req, res, next) => {
  const errors = validationResult(req);
  if (!errors.isEmpty()) {
    return res.status(400).json({
      success: false,
      errors: errors.array(),
    });
  }
  next();
};

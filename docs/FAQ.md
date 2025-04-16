# Frequently Asked Questions (FAQ)

## General Questions

### What is Taxzy.ai?

Taxzy.ai is an AI-powered tax assistant specifically designed to help international students and employees on various visa types navigate California tax regulations. It uses Retrieval-Augmented Generation (RAG) technology to provide accurate, source-backed answers from official California Franchise Tax Board documents.

### Who can use Taxzy.ai?

Taxzy.ai is designed for:
- F-1 student visa holders
- J-1 exchange visitors
- H-1B workers
- OPT/CPT participants
- Other international visa holders in California

### Is Taxzy.ai a replacement for a tax professional?

No. Taxzy.ai is an educational tool to help you understand California tax regulations. For complex tax situations or personalized advice, you should consult with a qualified tax professional.

## Technical Questions

### What technology does Taxzy.ai use?

Taxzy.ai is built with:
- **Frontend**: React.js with Material UI
- **Backend**: Node.js with Express.js
- **Database**: MongoDB for user data, Chroma for vector embeddings
- **AI/ML**: LlamaIndex for RAG, BAAI embeddings, Llama 3.1 8B Instruct model

### How accurate are the answers?

All answers are grounded in official California FTB documents. The system provides source citations so you can verify the information. However, tax laws change frequently, so always verify with current official sources.

### Is my data secure?

Yes. We use:
- JWT-based authentication
- Encrypted connections (HTTPS)
- Secure password hashing
- Industry-standard security practices

### Can I delete my data?

Yes. You can delete your account and all associated conversations at any time through your account settings.

## Usage Questions

### How do I ask a question?

1. Create an account or log in
2. Start a new conversation
3. Type your tax question in the chat interface
4. Review the AI-generated answer and source citations

### What kind of questions can I ask?

You can ask about:
- Tax residency determination
- Filing requirements and deadlines
- Income taxation (wages, scholarships, fellowships)
- Deductions and credits
- State vs. federal tax differences
- Visa-specific tax implications

### Why does the AI include source citations?

Source citations allow you to:
- Verify the information
- Read the full context in official documents
- Build confidence in the answers
- Understand where the information comes from

### Can I save my conversations?

Yes. All conversations are automatically saved to your account. You can access past conversations from your dashboard.

## Visa-Specific Questions

### I'm on an F-1 visa. Am I a resident or nonresident for tax purposes?

Generally, F-1 students are considered nonresident aliens for their first 5 calendar years in the US. However, your specific situation may vary. Ask Taxzy.ai for personalized guidance based on your circumstances.

### Do I need to file taxes if I only have scholarship income?

Even if you don't owe taxes, you may still need to file Form 8843 if you're on F-1 or J-1 status. Taxzy.ai can help you understand your filing requirements.

### What's the difference between OPT and CPT for tax purposes?

Both are extensions of F-1 status, but they have different implications for employment and taxation. Taxzy.ai can explain the specific differences relevant to your situation.

## Troubleshooting

### The AI doesn't understand my question

Try:
- Rephrasing your question
- Breaking complex questions into smaller parts
- Being more specific about your visa type and situation
- Providing more context

### I got an error message

Common solutions:
- Check your internet connection
- Try refreshing the page
- Log out and log back in
- Clear your browser cache

### The response seems incorrect

- Check the source citations
- Rephrase your question
- Verify with official FTB publications
- Consult a tax professional for confirmation

### I can't find a specific document

The knowledge base includes major FTB publications. For specialized forms or recent updates:
- Visit the California FTB website directly
- Ask about the topic rather than the specific form
- Contact the FTB for the most current information

## Account Questions

### How do I reset my password?

Password reset functionality is available on the login page. Click "Forgot Password" and follow the instructions.

### Can I change my visa type after registration?

Yes, you can update your profile information including visa type in your account settings.

### Is there a limit to how many questions I can ask?

There are no hard limits, but rate limiting prevents abuse. Typical users won't hit these limits during normal usage.

## Privacy & Data

### What information do you collect?

We collect:
- Account information (name, email, visa type)
- Conversation history
- Usage analytics

### Do you share my data?

No. Your data is not shared with third parties. See our Privacy Policy for details.

### How long do you keep my data?

Account data is kept until you delete your account. Conversation history is preserved for your reference.

## Support

### How do I report a bug?

Open an issue on our GitHub repository or contact support through the app.

### Can I request new features?

Yes! We welcome feature requests through GitHub issues.

### How do I contribute to the project?

See our CONTRIBUTING.md file for guidelines on contributing to the project.

### Who maintains Taxzy.ai?

Taxzy.ai is maintained by a team at San Jose State University. See the README for contact information.

## Legal Disclaimer

Taxzy.ai provides educational information only and should not be construed as professional tax, legal, or immigration advice. For personalized advice regarding your specific situation, consult with qualified professionals.

Tax laws and regulations are subject to change. While we strive to keep information current, always verify with official sources and current publications.

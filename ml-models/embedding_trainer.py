"""
Fine-tune embedding model for California tax document retrieval
"""
import os
import torch
from sentence_transformers import SentenceTransformer, InputExample, losses
from sentence_transformers import evaluation
from torch.utils.data import DataLoader
import json
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TaxEmbeddingTrainer:
    """
    Fine-tune embeddings specifically for California tax documents
    """

    def __init__(self, base_model='BAAI/bge-base-en-v1.5'):
        self.base_model = base_model
        self.model = None
        self.train_examples = []
        self.eval_examples = []

    def load_training_data(self, data_path):
        """
        Load training pairs for fine-tuning
        Format: [{"query": "...", "positive": "...", "negative": "..."}]
        """
        logger.info(f"Loading training data from {data_path}")

        with open(data_path, 'r') as f:
            data = json.load(f)

        for item in data:
            self.train_examples.append(
                InputExample(
                    texts=[item['query'], item['positive'], item['negative']]
                )
            )

        logger.info(f"Loaded {len(self.train_examples)} training examples")

    def prepare_model(self):
        """Initialize the base model"""
        logger.info(f"Loading base model: {self.base_model}")
        self.model = SentenceTransformer(self.base_model)

    def train(self, output_path, epochs=4, batch_size=16, warmup_steps=500):
        """
        Fine-tune the model
        """
        if not self.model:
            self.prepare_model()

        # Create dataloader
        train_dataloader = DataLoader(
            self.train_examples,
            shuffle=True,
            batch_size=batch_size
        )

        # Define loss function
        train_loss = losses.MultipleNegativesRankingLoss(self.model)

        # Configure training
        logger.info(f"Starting training for {epochs} epochs")

        self.model.fit(
            train_objectives=[(train_dataloader, train_loss)],
            epochs=epochs,
            warmup_steps=warmup_steps,
            output_path=output_path,
            show_progress_bar=True,
            use_amp=True  # Use automatic mixed precision
        )

        logger.info(f"Model saved to {output_path}")

    def evaluate(self, test_queries, test_docs, test_relevance):
        """
        Evaluate model performance
        """
        from sentence_transformers.evaluation import InformationRetrievalEvaluator

        evaluator = InformationRetrievalEvaluator(
            test_queries,
            test_docs,
            test_relevance
        )

        results = evaluator(self.model)
        logger.info(f"Evaluation results: {results}")
        return results


def create_training_dataset():
    """
    Create synthetic training data for tax domain
    """
    training_data = [
        {
            "query": "What are the tax filing requirements for F-1 students?",
            "positive": "F-1 students must file Form 1040-NR and Form 8843 if they were present in the US during the tax year.",
            "negative": "H-1B workers file Form 1040 as resident aliens after passing the substantial presence test."
        },
        {
            "query": "California state tax rate for international students",
            "positive": "California state tax rates range from 1% to 12.3% based on income brackets for all residents and part-year residents.",
            "negative": "Federal tax rates for nonresident aliens on scholarship income are generally 14% on the taxable portion."
        },
        {
            "query": "Do OPT students pay Social Security tax?",
            "positive": "Students on F-1 OPT are exempt from Social Security and Medicare taxes for the first 5 years under the student exemption.",
            "negative": "H-1B workers are required to pay Social Security and Medicare taxes from their first day of employment."
        },
        {
            "query": "Tax treaty benefits for Indian students in California",
            "positive": "The US-India tax treaty provides exemptions for scholarship and fellowship income for Indian students studying in the US.",
            "negative": "The California Franchise Tax Board does not conform to all federal tax treaty provisions."
        },
        {
            "query": "When is the deadline to file California state taxes?",
            "positive": "California state tax returns are due on April 15th, or October 15th with an extension.",
            "negative": "FAFSA applications are due by March 2nd for California students applying for state aid."
        },
        {
            "query": "What is Form 8843 and who needs to file it?",
            "positive": "Form 8843 is required for F-1 and J-1 visa holders to claim the exempt individual status, even if they have no income.",
            "negative": "Form W-4 is used by all employees to determine federal tax withholding from paychecks."
        },
        {
            "query": "Scholarship taxation for graduate students on F-1 visa",
            "positive": "Scholarship amounts used for tuition and fees are tax-free, but amounts for room, board, and living expenses are taxable for F-1 students.",
            "negative": "Teaching assistantships for graduate students are generally fully taxable as employment income."
        },
        {
            "query": "Resident vs nonresident alien determination",
            "positive": "F-1 students are nonresident aliens for their first 5 calendar years. After 5 years, they may become residents under the substantial presence test.",
            "negative": "California residency is determined by domicile and intent to remain, which differs from federal tax residency."
        }
    ]

    output_path = '/home/user/CTax.ai/ml-models/data/training_pairs.json'
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with open(output_path, 'w') as f:
        json.dump(training_data, f, indent=2)

    logger.info(f"Training data saved to {output_path}")
    return output_path


if __name__ == '__main__':
    # Create training dataset
    data_path = create_training_dataset()

    # Initialize trainer
    trainer = TaxEmbeddingTrainer()

    # Load and train
    trainer.load_training_data(data_path)
    trainer.train(
        output_path='/home/user/CTax.ai/ml-models/models/tax-embeddings',
        epochs=4,
        batch_size=16
    )

"""
Evaluate RAG model performance and accuracy
"""
import numpy as np
from typing import List, Dict, Tuple
import json
import logging
from sklearn.metrics import precision_recall_fscore_support
import matplotlib.pyplot as plt
import seaborn as sns

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class RAGModelEvaluator:
    """
    Comprehensive evaluation of RAG model performance
    """

    def __init__(self):
        self.metrics = {}
        self.test_cases = []

    def load_test_cases(self, test_file: str):
        """Load evaluation test cases"""
        with open(test_file, 'r') as f:
            self.test_cases = json.load(f)
        logger.info(f"Loaded {len(self.test_cases)} test cases")

    def calculate_retrieval_metrics(
        self,
        retrieved_docs: List[str],
        relevant_docs: List[str]
    ) -> Dict[str, float]:
        """
        Calculate precision, recall, and F1 for document retrieval
        """
        retrieved_set = set(retrieved_docs)
        relevant_set = set(relevant_docs)

        if len(retrieved_set) == 0:
            return {'precision': 0.0, 'recall': 0.0, 'f1': 0.0}

        # True positives: documents both retrieved and relevant
        tp = len(retrieved_set.intersection(relevant_set))

        # Precision: proportion of retrieved docs that are relevant
        precision = tp / len(retrieved_set) if len(retrieved_set) > 0 else 0

        # Recall: proportion of relevant docs that were retrieved
        recall = tp / len(relevant_set) if len(relevant_set) > 0 else 0

        # F1 score
        f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0

        return {
            'precision': precision,
            'recall': recall,
            'f1': f1,
            'true_positives': tp
        }

    def calculate_mrr(self, retrieved_docs: List[str], relevant_docs: List[str]) -> float:
        """
        Calculate Mean Reciprocal Rank
        """
        for idx, doc in enumerate(retrieved_docs, 1):
            if doc in relevant_docs:
                return 1.0 / idx
        return 0.0

    def calculate_ndcg(
        self,
        retrieved_docs: List[str],
        relevance_scores: Dict[str, float],
        k: int = 10
    ) -> float:
        """
        Calculate Normalized Discounted Cumulative Gain (NDCG@k)
        """
        # DCG
        dcg = 0.0
        for idx, doc in enumerate(retrieved_docs[:k], 1):
            relevance = relevance_scores.get(doc, 0)
            dcg += relevance / np.log2(idx + 1)

        # IDCG (ideal DCG)
        ideal_docs = sorted(relevance_scores.items(), key=lambda x: x[1], reverse=True)
        idcg = 0.0
        for idx, (doc, relevance) in enumerate(ideal_docs[:k], 1):
            idcg += relevance / np.log2(idx + 1)

        return dcg / idcg if idcg > 0 else 0.0

    def evaluate_answer_quality(
        self,
        generated_answer: str,
        reference_answer: str
    ) -> Dict[str, float]:
        """
        Evaluate generated answer quality using various metrics
        """
        # Simple token overlap (can be replaced with BLEU, ROUGE, etc.)
        gen_tokens = set(generated_answer.lower().split())
        ref_tokens = set(reference_answer.lower().split())

        overlap = len(gen_tokens.intersection(ref_tokens))
        precision = overlap / len(gen_tokens) if len(gen_tokens) > 0 else 0
        recall = overlap / len(ref_tokens) if len(ref_tokens) > 0 else 0
        f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0

        return {
            'token_precision': precision,
            'token_recall': recall,
            'token_f1': f1
        }

    def evaluate_faithfulness(
        self,
        answer: str,
        source_documents: List[str]
    ) -> float:
        """
        Evaluate if answer is grounded in source documents
        Simple implementation - can be enhanced with NLI models
        """
        answer_tokens = set(answer.lower().split())

        source_tokens = set()
        for doc in source_documents:
            source_tokens.update(doc.lower().split())

        # Calculate what portion of answer tokens appear in sources
        grounded_tokens = answer_tokens.intersection(source_tokens)
        faithfulness = len(grounded_tokens) / len(answer_tokens) if len(answer_tokens) > 0 else 0

        return faithfulness

    def run_comprehensive_evaluation(self, rag_system) -> Dict[str, any]:
        """
        Run full evaluation suite
        """
        all_retrieval_metrics = []
        all_answer_metrics = []
        all_mrr_scores = []
        all_faithfulness_scores = []

        for test_case in self.test_cases:
            query = test_case['query']

            # Get RAG response
            response = rag_system.query(query)

            # Evaluate retrieval
            retrieval_metrics = self.calculate_retrieval_metrics(
                [s['documentName'] for s in response['sources']],
                test_case['relevant_docs']
            )
            all_retrieval_metrics.append(retrieval_metrics)

            # Evaluate MRR
            mrr = self.calculate_mrr(
                [s['documentName'] for s in response['sources']],
                test_case['relevant_docs']
            )
            all_mrr_scores.append(mrr)

            # Evaluate answer quality
            if 'reference_answer' in test_case:
                answer_metrics = self.evaluate_answer_quality(
                    response['answer'],
                    test_case['reference_answer']
                )
                all_answer_metrics.append(answer_metrics)

            # Evaluate faithfulness
            faithfulness = self.evaluate_faithfulness(
                response['answer'],
                [s['excerpt'] for s in response['sources']]
            )
            all_faithfulness_scores.append(faithfulness)

        # Aggregate results
        results = {
            'retrieval': {
                'avg_precision': np.mean([m['precision'] for m in all_retrieval_metrics]),
                'avg_recall': np.mean([m['recall'] for m in all_retrieval_metrics]),
                'avg_f1': np.mean([m['f1'] for m in all_retrieval_metrics]),
            },
            'mrr': np.mean(all_mrr_scores),
            'answer_quality': {
                'avg_token_f1': np.mean([m['token_f1'] for m in all_answer_metrics]) if all_answer_metrics else 0,
            },
            'faithfulness': np.mean(all_faithfulness_scores),
            'num_test_cases': len(self.test_cases)
        }

        logger.info("Evaluation Results:")
        logger.info(json.dumps(results, indent=2))

        return results

    def generate_evaluation_report(self, results: Dict, output_path: str):
        """
        Generate visual evaluation report
        """
        fig, axes = plt.subplots(2, 2, figsize=(12, 10))
        fig.suptitle('RAG Model Evaluation Report', fontsize=16)

        # Retrieval metrics
        retrieval_data = results['retrieval']
        axes[0, 0].bar(retrieval_data.keys(), retrieval_data.values())
        axes[0, 0].set_title('Retrieval Metrics')
        axes[0, 0].set_ylim([0, 1])

        # MRR
        axes[0, 1].bar(['MRR'], [results['mrr']])
        axes[0, 1].set_title('Mean Reciprocal Rank')
        axes[0, 1].set_ylim([0, 1])

        # Answer Quality
        axes[1, 0].bar(['Token F1'], [results['answer_quality']['avg_token_f1']])
        axes[1, 0].set_title('Answer Quality')
        axes[1, 0].set_ylim([0, 1])

        # Faithfulness
        axes[1, 1].bar(['Faithfulness'], [results['faithfulness']])
        axes[1, 1].set_title('Answer Faithfulness')
        axes[1, 1].set_ylim([0, 1])

        plt.tight_layout()
        plt.savefig(output_path)
        logger.info(f"Report saved to {output_path}")


# Sample test cases
def create_test_cases():
    """Create evaluation test cases"""
    test_cases = [
        {
            "query": "What forms do F-1 students need to file?",
            "relevant_docs": ["Form 1040-NR Instructions.pdf", "Form 8843 Instructions.pdf"],
            "reference_answer": "F-1 students must file Form 1040-NR for income tax reporting and Form 8843 to claim exempt individual status."
        },
        {
            "query": "California state tax rates for 2024",
            "relevant_docs": ["California Tax Rates 2024.pdf", "FTB Publication 1032.pdf"],
            "reference_answer": "California state tax rates for 2024 range from 1% to 12.3% depending on income level."
        }
    ]

    import os
    output_path = '/home/user/CTax.ai/ml-models/data/test_cases.json'
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with open(output_path, 'w') as f:
        json.dump(test_cases, f, indent=2)

    return output_path


if __name__ == '__main__':
    # Create test cases
    test_file = create_test_cases()

    # Initialize evaluator
    evaluator = RAGModelEvaluator()
    evaluator.load_test_cases(test_file)

    # Note: In practice, you would pass your actual RAG system here
    # results = evaluator.run_comprehensive_evaluation(rag_system)
    # evaluator.generate_evaluation_report(results, 'evaluation_report.png')

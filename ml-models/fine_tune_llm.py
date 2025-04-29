"""
Fine-tune LLM for California tax-specific responses
"""
import torch
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    TrainingArguments,
    Trainer,
    DataCollatorForLanguageModeling
)
from datasets import Dataset
import json
import logging
from typing import List, Dict

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TaxLLMFineTuner:
    """
    Fine-tune language model on California tax domain
    """

    def __init__(self, base_model='microsoft/phi-2'):
        self.base_model = base_model
        self.model = None
        self.tokenizer = None

    def load_model(self):
        """Load base model and tokenizer"""
        logger.info(f"Loading model: {self.base_model}")

        self.tokenizer = AutoTokenizer.from_pretrained(self.base_model)
        self.model = AutoModelForCausalLM.from_pretrained(
            self.base_model,
            torch_dtype=torch.float16,
            device_map="auto",
            trust_remote_code=True
        )

        # Add padding token if not present
        if self.tokenizer.pad_token is None:
            self.tokenizer.pad_token = self.tokenizer.eos_token

    def prepare_training_data(self, data_path: str) -> Dataset:
        """
        Prepare training data in instruction-following format
        """
        with open(data_path, 'r') as f:
            examples = json.load(f)

        # Format as instruction-following
        formatted_examples = []
        for example in examples:
            text = f"""### Instruction:
{example['instruction']}

### Context:
{example.get('context', '')}

### Response:
{example['response']}"""
            formatted_examples.append({'text': text})

        dataset = Dataset.from_list(formatted_examples)

        # Tokenize
        def tokenize_function(examples):
            return self.tokenizer(
                examples['text'],
                truncation=True,
                max_length=512,
                padding='max_length'
            )

        tokenized_dataset = dataset.map(
            tokenize_function,
            batched=True,
            remove_columns=dataset.column_names
        )

        return tokenized_dataset

    def train(
        self,
        train_dataset: Dataset,
        output_dir: str,
        num_epochs: int = 3,
        batch_size: int = 4
    ):
        """
        Fine-tune the model
        """
        training_args = TrainingArguments(
            output_dir=output_dir,
            num_train_epochs=num_epochs,
            per_device_train_batch_size=batch_size,
            gradient_accumulation_steps=4,
            learning_rate=2e-5,
            fp16=True,
            logging_steps=10,
            save_steps=100,
            save_total_limit=2,
            warmup_steps=50,
            logging_dir=f'{output_dir}/logs',
            report_to='tensorboard'
        )

        data_collator = DataCollatorForLanguageModeling(
            tokenizer=self.tokenizer,
            mlm=False
        )

        trainer = Trainer(
            model=self.model,
            args=training_args,
            train_dataset=train_dataset,
            data_collator=data_collator
        )

        logger.info("Starting training...")
        trainer.train()

        logger.info(f"Saving model to {output_dir}")
        trainer.save_model(output_dir)
        self.tokenizer.save_pretrained(output_dir)


def create_training_examples():
    """
    Create domain-specific training examples
    """
    examples = [
        {
            "instruction": "Explain the tax filing requirements for F-1 students in California.",
            "context": "F-1 visa, nonresident alien status, California state",
            "response": "F-1 students in California must file both federal and state tax returns if they have income. For federal taxes, they file Form 1040-NR as nonresident aliens (for first 5 years) and Form 8843 to claim exempt individual status. For California state taxes, they file Form 540-NR if they have California-source income. Even with no income, Form 8843 is required."
        },
        {
            "instruction": "What is the California state tax rate for international students?",
            "context": "California, tax rates, 2024",
            "response": "California state tax rates for 2024 range from 1% to 12.3% based on income brackets. The rates apply to all residents and part-year residents, including international students. For students with minimal income (under $10,000), the effective rate is typically 1-2%. Higher income students may pay progressively higher rates up to 9.3% for most income levels."
        },
        {
            "instruction": "Are F-1 OPT students exempt from Social Security and Medicare taxes?",
            "context": "F-1 OPT, FICA taxes, student exemption",
            "response": "Yes, F-1 students on OPT are exempt from Social Security (OASDI) and Medicare taxes for the first 5 calendar years they are in F-1 status, under the student FICA exemption. This exemption applies as long as they maintain their F-1 status and haven't changed to another visa category. After 5 years, or if they become resident aliens, they must pay FICA taxes."
        },
        {
            "instruction": "How do I determine if I'm a resident or nonresident alien for tax purposes?",
            "context": "Tax residency, substantial presence test, F-1 status",
            "response": "Tax residency is determined by the substantial presence test, but F-1 students are exempt individuals. For the first 5 calendar years in F-1 status, you're a nonresident alien regardless of days present. After 5 years, you apply the substantial presence test: if present 183 days in current year, or 183 weighted days over 3 years, you become a resident alien. Note: California state residency rules differ from federal."
        },
        {
            "instruction": "What happens if I file my taxes late as an international student?",
            "context": "Late filing, penalties, international students",
            "response": "Late filing penalties can be significant. The IRS charges a failure-to-file penalty of 5% per month (up to 25%) of unpaid taxes. California FTB has similar penalties. However, if you have no tax liability (common for students with minimal income), penalties may be minimal. Still, failing to file Form 8843 could affect your visa status. Always file on time, even if requesting an extension."
        },
        {
            "instruction": "Can I claim tax treaty benefits as an Indian student?",
            "context": "US-India tax treaty, scholarship exemption",
            "response": "Yes, the US-India tax treaty (Article 21) provides that payments received by Indian students for maintenance, education, or training are exempt from US tax. This covers scholarships and fellowship grants. To claim this benefit, file Form 1040-NR with Form 8833 (treaty-based return position). Note that California doesn't always conform to federal treaty provisions, so state taxes may still apply."
        }
    ]

    import os
    output_path = '/home/user/CTax.ai/ml-models/data/llm_training_examples.json'
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with open(output_path, 'w') as f:
        json.dump(examples, f, indent=2)

    logger.info(f"Training examples saved to {output_path}")
    return output_path


if __name__ == '__main__':
    # Create training data
    data_path = create_training_examples()

    # Initialize fine-tuner
    fine_tuner = TaxLLMFineTuner()
    fine_tuner.load_model()

    # Prepare and train
    train_dataset = fine_tuner.prepare_training_data(data_path)
    fine_tuner.train(
        train_dataset,
        output_dir='/home/user/CTax.ai/ml-models/models/tax-llm-finetuned',
        num_epochs=3,
        batch_size=4
    )

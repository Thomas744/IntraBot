from transformers import pipeline

class LLMClient:
    def __init__(self):
        self.llm = pipeline(
            "text2text-generation",
            model="google/flan-t5-base",
            max_length=512,
        )

    def generate(self, prompt: str) -> str:
        return self.llm(prompt)[0]["generated_text"]

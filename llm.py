import os
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()

# Create reusable OpenAI client
client = OpenAI()


def generate_response(prompt: str) -> str:
    """
    Generate text using OpenAI Responses API.
    Compatible with agent architecture.
    """

    model = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")

    try:
        response = client.responses.create(
            model=model,
            input=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            temperature=0.2,
            max_output_tokens=600,
        )

        return response.output_text.strip()

    except Exception as e:
        raise RuntimeError(f"OpenAI API request failed: {e}")

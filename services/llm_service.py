# services/llm_service.py

import openai
import os
from config.settings import DEFAULT_LLM_MODEL

OPENAI_API_KEY = os.getenv("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")
openai.api_key = OPENAI_API_KEY

def get_llm_response(prompt: str, model: str = DEFAULT_LLM_MODEL, system_prompt: str = "You are a witty cricket assistant.") -> str:
    try:
        response = openai.ChatCompletion.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=300
        )
        return response['choices'][0]['message']['content'].strip()
    except Exception as e:
        return f"⚠️ LLM error: {str(e)}"

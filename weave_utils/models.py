import os
import asyncio
import random
import weave
from typing import Optional

import time
from litellm import acompletion

from dotenv import load_dotenv
load_dotenv()

from openai import RateLimitError


MODEL_MAP = {
    "llama3": "llama3",
    "llama2": "llama2",
    "codellama": "codellama",
    "mistral": "mistral",
    "mixtral": "mixtral",
    "llava": "llava",
    "gemma": "gemma",
    "phi3": "phi3",
    "qwen2": "qwen2",
    "qwen3:14b-q4_K_M": "qwen3:14b-q4_K_M",
    "command-r": "command-r",
    "command-r-plus": "command-r-plus",
}

EXPONENTIAL_BASE = 2    


class MajorityVoteModel(weave.Model):
    model: weave.Model
    num_responses: int = 3
    
    @weave.op()
    async def predict(self, prompt: str):
        tasks = [self.model.predict(prompt) for _ in range(self.num_responses)]
        return await asyncio.gather(*tasks)


class LiteLLMModel(weave.Model):
    model_name: str
    system_prompt: Optional[str] = None
    temp: float = 0.7
    max_tokens: int = 2048
    top_p: float = 0.95
    max_retries: int = 3
    
    def __init__(self, **data):
        super().__init__(**data)
        # Add any additional initialization logic here
        if self.model_name not in MODEL_MAP:
            raise ValueError(f"Invalid model name: {self.model_name}")

        self.model_name = f"ollama/{self.model_name}"

    
    @weave.op()
    async def predict(self, prompt: str):
        delay = 2

        for i in range(self.max_retries):
            try:
                messages = []
                if self.system_prompt is not None:
                    messages.append({
                        "role": "system",
                        "content": self.system_prompt
                    })
                messages.append({
                    "role": "user",
                    "content": prompt
                })
                response = await acompletion(
                    model=self.model_name,
                    messages=messages,
                    temperature=self.temp,
                    max_tokens=self.max_tokens,
                    top_p=self.top_p
                )

                if response.choices[0].message.content is not None:
                    return response.choices[0].message.content
                else:
                    print(response)
                    raise Exception("No content in response")
            except RateLimitError as e:
                delay *= EXPONENTIAL_BASE * (1 + random.random())
                print(
                    f"RateLimitError, retrying after {round(delay, 2)} seconds, {i+1}-th retry...", e
                )
                await asyncio.sleep(delay)
                continue
            except Exception as e:
                print(f"Error in retry {i+1}, retrying...", e)
                continue

        raise Exception("Failed to get response after max retries")

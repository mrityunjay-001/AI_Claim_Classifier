# llm.py

import os

# Disable LiteLLM telemetry/logging workers
os.environ["LITELLM_LOG"] = "ERROR"
os.environ["LITELLM_MODE"] = "PRODUCTION"

from dotenv import load_dotenv
from litellm import completion
import litellm

load_dotenv()

# Disable verbose/debug
litellm.set_verbose = False

PRIMARY = "groq/llama-3.3-70b-versatile"
FALLBACK = "gemini/gemini-2.5-flash"


def ask(messages, **kwargs):

    response = completion(
        model=PRIMARY,
        messages=messages,
        fallbacks=[FALLBACK],
        num_retries=1,
        timeout=30,
        stream=False,  # important
        **kwargs
    )

    return response
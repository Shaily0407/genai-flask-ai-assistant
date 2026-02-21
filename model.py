import ssl
ssl._create_default_https_context = ssl._create_unverified_context

import time
import logging
from ibm_watsonx_ai import Credentials
from ibm_watsonx_ai.foundation_models import ModelInference
from ibm_watsonx_ai.metanames import GenTextParamsMetaNames
from config import *

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


# 🔹 Simple sentiment detection
def detect_sentiment(text):
    text = text.lower()

    negative_words = ["sad", "bad", "angry", "upset", "depressed", "cry", "hurt"]
    positive_words = ["happy", "good", "great", "excited", "awesome", "love"]

    for word in negative_words:
        if word in text:
            return "Negative"

    for word in positive_words:
        if word in text:
            return "Positive"

    return "Neutral"


# 🔹 MAIN FUNCTION (WITH CHAT HISTORY)
def generate_response(user_prompt, model_name, chat_history):

    start_time = time.time()

    logging.info(f"User message: {user_prompt}")
    logging.info(f"Selected model: {model_name}")

    credentials = Credentials(
        url=URL,
        verify=False
    )

    model_id = MODELS.get(model_name, MODELS[MODEL_DEFAULT])

    params = {
        GenTextParamsMetaNames.DECODING_METHOD: DECODING_METHOD,
        GenTextParamsMetaNames.MAX_NEW_TOKENS: MAX_NEW_TOKENS,
        GenTextParamsMetaNames.TEMPERATURE: TEMPERATURE
    }

    model = ModelInference(
        model_id=model_id,
        params=params,
        credentials=credentials,
        project_id=PROJECT_ID
    )

    chat_history.append({
        "role": "user",
        "content": user_prompt
    })

    chat_history = chat_history[-10:]

    context = ""
    for msg in chat_history:
        context += f"{msg['role'].capitalize()}: {msg['content']}\n"

    formatted_prompt = f"""
You are a helpful AI assistant.

Use the conversation history below to maintain context.
Try to remember important details shared earlier.
Respond naturally.

Conversation History:
{context}

Assistant:
"""

    response = model.generate(formatted_prompt)
    raw_output = response['results'][0]['generated_text'].strip()

    chat_history.append({
        "role": "assistant",
        "content": raw_output
    })

    end_time = time.time()
    response_time = round(end_time - start_time, 2)

    logging.info(f"Response time: {response_time} seconds")
    logging.info(f"Assistant response: {raw_output}")

    return {
        "data": {
            "summary": user_prompt[:50] + "...",
            "sentiment": detect_sentiment(user_prompt),
            "response": raw_output,
            "model_used": model_name,
            "response_time": response_time,
            "total_messages": len(chat_history)
        },
        "updated_history": chat_history
    }
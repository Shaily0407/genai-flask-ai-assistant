import time
import logging
import requests
from config import *

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


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


def generate_response(user_prompt, model_name, chat_history):

    start_time = time.time()

    logging.info(f"User message: {user_prompt}")
    logging.info(f"Selected model: {model_name}")

    chat_history.append({"role": "user", "content": user_prompt})
    chat_history = chat_history[-10:]

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }

    # Map your dropdown to real OpenRouter models
    model_map = {
        "granite": "mistralai/mistral-7b-instruct",
        "llama": "meta-llama/llama-3-8b-instruct",
        "mistral": "mistralai/mistral-7b-instruct"
    }

    payload = {
        "model": model_map.get(model_name, "mistralai/mistral-7b-instruct"),
        "messages": chat_history,
        "temperature": 0.3,
        "max_tokens": 200
    }

    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers=headers,
        json=payload
    )

    result = response.json()

    if "error" in result:
        return {
            "data": {
                "summary": "Error",
                "sentiment": "Unknown",
                "response": result["error"]["message"],
                "model_used": model_name,
                "response_time": 0,
                "total_messages": len(chat_history)
            },
            "updated_history": chat_history
        }

    raw_output = result["choices"][0]["message"]["content"]

    chat_history.append({"role": "assistant", "content": raw_output})

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
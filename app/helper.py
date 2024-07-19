from pydantic import BaseModel
from loguru import logger
from .assistent import FastAPIAssistant
from .mluvii import ChatbotActivitySender
from .database.redis import redis_client

class WebhookRequest(BaseModel):
    activity: str
    timestamp: str
    text: str
    sessionId: int
    language: str
    source: str

async def process_webhook(webhook: WebhookRequest, assistant: FastAPIAssistant, chatbot_sender: ChatbotActivitySender):
    await handle_webhook(webhook, assistant, chatbot_sender)

async def handle_webhook(webhook: WebhookRequest, assistant: FastAPIAssistant, chatbot_sender: ChatbotActivitySender):
    session_id = webhook.sessionId

    try:
        thread_id = await redis_client.get(session_id)
    except Exception as e:
        logger.error(f"Error retrieving thread ID from Redis: {e}")
        return

    if not thread_id:
        thread = await assistant.post_thread()
        if thread:
            thread_id = thread['data']['id']
            # Uložte thread_id do Redis
            await redis_client.set(session_id, thread_id)
        else:
            logger.error("Failed to create thread")
            return

    try:
        response = await assistant.chat(webhook.text, thread_id)
        await chatbot_sender.send_activity(session_id, response)
        logger.debug(f"Response from assistant: {response}")
    except Exception as e:
        logger.error(f"Error during chat process: {e}")

    await assistant.close()

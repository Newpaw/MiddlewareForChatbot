import markdown
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

def convert_markdown_to_html(markdown_text):
    return markdown.markdown(markdown_text)


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

        await chatbot_sender.send_typing(session_id, show=True)
        response = await assistant.chat(webhook.text, thread_id)
        response_html = convert_markdown_to_html(response)
        await chatbot_sender.send_activity(session_id, response_html)
        await chatbot_sender.send_typing(session_id, show=False)

        logger.debug(f"Response from assistant: {response}")
    except Exception as e:
        logger.error(f"Error during chat process: {e}")

    await assistant.close()

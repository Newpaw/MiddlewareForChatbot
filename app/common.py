from loguru import logger
from .assistent import FastAPIAssistant
from .mluvii import ChatbotActivitySender
from .config import settings

def get_assistant_service() -> FastAPIAssistant:
    base_url_assistent = settings.BASE_URL_ASSISTENT
    logger.debug(f"FastAPIAssistant base URL: {base_url_assistent}")
    return FastAPIAssistant(base_url_assistent)


def get_chatbot_sender() -> ChatbotActivitySender:
    chatbot_id = settings.CHATBOT_ID
    base_url_mluvii = settings.BASE_URL_MLUVII
    client_id = settings.CLIENT_ID
    client_secret = settings.CLIENT_SECRET


    logger.debug(f"Chatbot ID: {chatbot_id}")
    logger.debug(f"Chatbot Base URL: {base_url_mluvii}")

    if not client_id or not client_secret:
        logger.error("Client ID and Client Secret must be provided")
        raise ValueError("Client ID and Client Secret must be provided")

    return ChatbotActivitySender(chatbot_id, base_url_mluvii, client_id, client_secret)

from fastapi import APIRouter, Request, Depends
from loguru import logger
from .assistent import FastAPIAssistant
from .mluvii import ChatbotActivitySender
from .common import get_assistant_service, get_chatbot_sender
from .helper import WebhookRequest, process_webhook



router = APIRouter()

@router.post("/", tags=["webhooks"])
async def receive_webhook(request: Request, assistant: FastAPIAssistant = Depends(get_assistant_service), chatbot_sender: ChatbotActivitySender = Depends(get_chatbot_sender)):
    webhook_data:dict = await request.json()
    logger.debug(f"Received webhook data: {webhook_data}")
    
    if webhook_data.get("activity") != "Text":
        return {"status": "success"}

    webhook = WebhookRequest(**webhook_data)

    # Přímo zavoláme asynchronní funkci
    await process_webhook(webhook, assistant, chatbot_sender)

    return {"status": "success"}

# To run the application use: uvicorn app.main:app --reload --port 8080

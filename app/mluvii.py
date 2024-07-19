import httpx
import datetime
from typing import Optional
from loguru import logger
import pytz


prague_tz = pytz.timezone('Europe/Prague')

class ChatbotActivitySender:
    def __init__(self, chatbot_id:str, base_url:str, client_id:str, client_secret:str):
        self.chatbot_id = chatbot_id
        self.base_url = base_url
        self.client_id = client_id
        self.client_secret = client_secret
        self.endpoint = f"{self.base_url}/api/v1/Chatbot/{self.chatbot_id}/activity"
        self.token_url = f"{self.base_url}/login/connect/token"
        self.access_token: Optional[str] = None
        self.token_expiry: Optional[datetime.datetime] = None

    async def get_access_token(self):
        async with httpx.AsyncClient() as client:
            response = await client.post(
                self.token_url,
                data={
                    'grant_type': 'client_credentials',
                    'client_id': self.client_id,
                    'client_secret': self.client_secret
                },
                headers={'Content-Type': 'application/x-www-form-urlencoded'}
            )
            response_data = response.json()
            self.access_token = response_data['access_token']
            expires_in = response_data['expires_in']
            self.token_expiry = datetime.datetime.now() + datetime.timedelta(seconds=expires_in)

    async def ensure_token_valid(self):
        if self.access_token is None or datetime.datetime.now() >= self.token_expiry:
            await self.get_access_token()

    async def send_activity(self, session_id: str, text: str, activity_type: str = "message"):
        await self.ensure_token_valid()

        timestamp = datetime.datetime.now(prague_tz).isoformat()
        payload = {
            "sessionId": session_id,
            "type": activity_type,
            "text": text,
            "timestamp": timestamp
        }

        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }

        async with httpx.AsyncClient(follow_redirects=True) as client:
            response = await client.post(self.endpoint, json=payload, headers=headers)

        if response.status_code == 200:
            logger.debug("Activity sent successfully")
            return None
        else:
            logger.error(
                f"Failed to send activity: {response.status_code} - {response.text}")
            return None

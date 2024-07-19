import httpx
from loguru import logger

class FastAPIAssistant:
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.client = httpx.AsyncClient(timeout=httpx.Timeout(60.0, connect=10.0))
        logger.debug("FastAPIAssistant initialized")

    async def get_assistant(self):
        url = f"{self.base_url}/api/v1/assistant"
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
        response.raise_for_status()
        return response.json()

    async def post_thread(self):
        url = f"{self.base_url}/api/v1/assistant/threads"
        async with httpx.AsyncClient() as client:
            response = await client.post(url)
        response.raise_for_status()
        return response.json()

    async def chat(self, text: str, thread_id: str) -> str:
        url = f"{self.base_url}/api/v1/assistant/chat"
        payload = {
            "text": text,
            "thread_id": thread_id
        }

        # Debug log pro kontrolu payloadu
        logger.debug(f"Payload for chat: {payload}")

        # Ujistěte se, že žádný prvek payload není typu bytes
        for key, value in payload.items():
            if isinstance(value, bytes):
                payload[key] = value.decode('utf-8')

        
        for attempt in range(3):
            try:
                response = await self.client.post(url, json=payload)
                response.raise_for_status()
                return response.text
            except httpx.RequestError as exc:
                logger.error(f"Request error {exc} on attempt {attempt + 1}")
            except httpx.HTTPStatusError as exc:
                logger.error(f"HTTP status error {exc} on attempt {attempt + 1}")
            except httpx.TimeoutException as exc:
                logger.error(f"Timeout error {exc} on attempt {attempt + 1}")

        raise httpx.HTTPStatusError("Failed to connect after several attempts", request=None, response=None)
    
    async def close(self):
        await self.client.aclose()
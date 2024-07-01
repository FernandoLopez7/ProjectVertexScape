import asyncio
import json
from channels.generic.websocket import AsyncWebsocketConsumer
import logging

logger = logging.getLogger(__name__)

class CameraStreamConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        logger.info("WebSocket connected")

    async def disconnect(self, close_code):
        logger.info(f"WebSocket disconnected: {close_code}")

    async def receive(self, text_data=None, bytes_data=None):
        if text_data:
            logger.info(f"Received text data: {text_data}")
            try:
                data = json.loads(text_data)

                # Check if the message is a command to subscribe to a group
                if data.get('command') == 'subscribe' and data.get('group'):
                    await self.channel_layer.group_add(
                        data['group'],  # Group name to subscribe
                        self.channel_name  # Channel name of this consumer
                    )
                    logger.info(f"Subscribed to group: {data['group']}")
                else:
                    await self.channel_layer.group_send(
                        "web_clients_group",
                        {
                            "type": "web_data",
                            "data": text_data
                        }
                    )
            except json.JSONDecodeError:
                logger.error("Invalid JSON format")
                await self.send(text_data=json.dumps({
                    'error': 'Invalid JSON format'
                }))

        if bytes_data:
            await self.channel_layer.group_send(
                "web_clients_group",
                {
                    "type": "web_data",
                    "data": bytes_data
                }
            )

    async def web_data(self, event):
        data = event['data']
        if isinstance(data, bytes):
            await self.send(bytes_data=data)
        else:
            await self.send(text_data=data)
        #logger.info(f"Data sent to web clients group: {data}") #comprobado, si funciona

import asyncio
import websockets
import json

connected_clients = set()

async def handler(websocket, path):
    # Add the new client to the set of connected clients
    connected_clients.add(websocket)
    try:
        async for message in websocket:
            data = json.loads(message)
            # Broadcast the message to all connected clients
            for client in connected_clients:
                if client != websocket:
                    await client.send(json.dumps(data))
    finally:
        # Remove the client from the set of connected clients
        connected_clients.remove(websocket)

start_server = websockets.serve(handler, "0.0.0.0", 6789)
# start_server = websockets.serve(handler, "example.com", 80)
# para conección segura 443
# para conección NO segura 80


asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()

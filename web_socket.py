import os
import asyncio
import json
import websockets

from app import judge, just_output


async def hello():
    while True:
        try:
            async with websockets.connect("ws://localhost:8765") as websocket:
                async for strin_message in websocket:
                    message = json.loads(strin_message)
                    if message['type'] == 'judge':
                        check_id, data = message['id'], message['data']
                        response = judge(check_id, data)
                        response |= {
                            'auth_token': os.environ['AUTH_TOKEN'], 'id': check_id, 'request_id': message['request_id']}
                        await websocket.send(json.dumps(response))
                    elif message['type'] == 'output':
                        check_id, data = message['id'], message['data']
                        response = just_output(check_id, data)
                        response |= {
                            'auth_token': os.environ['AUTH_TOKEN'], 'id': check_id, 'request_id': message['request_id']}
                        await websocket.send(json.dumps(response))

        except Exception as e:
            print('Connection closed')
            print(e)
            await asyncio.sleep(10)
            print('Reconnecting')

asyncio.run(hello())

import asyncio
import websockets
import json
import random  # Simulating IMU data

async def send_imu_data(websocket):
    print("Client connected")
    try:
        while True:
            # Simulating IMU angles (roll, pitch, yaw)
            imu_data = {
                "roll": 0,
                "pitch": 0,
                "yaw": 0
            }

            print(imu_data)
            
            # Send JSON data
            await websocket.send(json.dumps(imu_data))
            await asyncio.sleep(0.1)  # Simulate real-time streaming
    except websockets.exceptions.ConnectionClosed:
        print("Client disconnected")

async def main():
    server = await websockets.serve(send_imu_data, "localhost", 8080)
    await server.wait_closed()

asyncio.run(main())

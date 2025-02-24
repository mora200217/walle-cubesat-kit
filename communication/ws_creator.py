import asyncio
import websockets
import json
import random  # Simulating IMU data
from walle_sensors.bmi import BMI


async def send_imu_data(websocket, path = None):
    print("Client connected")
    try:
        while True:
            # Simulating IMU angles (roll, pitch, yaw)
            results = imu.read()
            print(results)
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
    global imu

    imu = BMI(0x69)
    imu.setup()

    print("Sensores configuration done")
    
    server = await websockets.serve(send_imu_data, "192.168.30.236", 8080)
    await server.wait_closed()

asyncio.run(main())

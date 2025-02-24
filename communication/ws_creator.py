import asyncio
import websockets
import numpy as np 
import json
import random  # Simulating IMU data
from walle_sensors.bmi import BMI
from utils.filter import LowPassFilter

N = 10 # For filter 

async def send_imu_data(websocket, path = None):
    print("Client connected")
    try:
        while True:
            # Simulating IMU angles (roll, pitch, yaw)
            angles = imu.read()
            # angles = results[1] # get pitch and roll
            filter = LowPassFilter(0.4)
            obs = obs[1:len(obs-1), angles[1]]
            filtered_value = filter.update(obs)
            
            imu_data = {
                "roll": filtered_value,
                "pitch":0,
                "yaw": 0
            }

            

            print(imu_data)
            
            # Send JSON data
            await websocket.send(json.dumps(imu_data))
            await asyncio.sleep(0.1)  # Simulate real-time streaming
    except websockets.exceptions.ConnectionClosed:
        print("Client disconnected")

async def main():
    global imu, obs 
    obs = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    imu = BMI(0x69)
    imu.setup()

    print("Sensores configuration done")

    server = await websockets.serve(send_imu_data, "192.168.30.236", 8080)
    await server.wait_closed()



def start(): 
    asyncio.run(main())

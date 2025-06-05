import asyncio
import os
import requests
from random import randint
from PIL import Image
from dotenv import get_key
from time import sleep

# Function to open and display generated images
def open_images(prompt):
    folder_path = r"Data"
    prompt = prompt.replace(" ", "_")
    Files = [f"{prompt}{i}.png" for i in range(1, 5)]
    
    for png_file in Files:
        image_path = os.path.join(folder_path, png_file)
        try:
            img = Image.open(image_path)
            print(f"Opening image: {image_path}")
            img.show()
            sleep(1)
        except IOError:
            print(f"Unable to open image {image_path}")
            
API_URL = "https://api-inference.huggingface.co/models/sd-legacy/stable-diffusion-v1-5"

headers = {"Authorization": f"Bearer {get_key('.env', 'HuggingFaceAPI')}"}

# Function to send a request to the API
async def query(payload):
    response = await asyncio.to_thread(requests.post, API_URL, headers=headers, json=payload)
    return response.content

# Function to generate images based on the prompt
async def generate_image(prompt: str):
    tasks = []
    for _ in range(4):
        payload = {
            "inputs": f"{prompt}, quality=4K, sharpness=maximum, Ultra High details, high resolution, seed = {randint(0, 1000000)}",
        }
        task = asyncio.create_task(query(payload))
        tasks.append(task)

    image_bytes_list = await asyncio.gather(*tasks)
    
    # Ensure the 'Data' directory exists
    if not os.path.exists('Data'):
        os.makedirs('Data')
    
    for i, image_bytes in enumerate(image_bytes_list):
        with open(fr"Data\{prompt.replace(' ', '_')}{i+1}.png", "wb") as f:
            f.write(image_bytes)

# Main function to coordinate image generation
def GenerateImages(prompt: str):
    asyncio.run(generate_image(prompt))
    open_images(prompt)

# Main loop to monitor the status and trigger image generation
while True:
    try:
        with open(r"Frontend\Files\ImageGeneration.data", "r") as f:
            Data: str = f.read()
        
        Prompt, Status = Data.split(",")
        Status = Status.strip()

        if Status == "True":
            print("Generating Image...")
            GenerateImages(prompt=Prompt)

            # Update the status after generation
            with open(r"Frontend\Files\ImageGeneration.data", "w") as f:
                f.write("False,False")
                print("Image generation complete, status updated.")

            # Exit the loop after completing the task
            break
        else:
            sleep(1)
    except Exception as e:
        print(f"Error encountered: {e}")
        sleep(1)

import openai
import os
import requests
from pathlib import Path

def generate_image(full_prompt, api_key):
    openai.api_key = api_key
    model_version = 'dall-e-3'
    try:
        response = openai.Image.create(
            prompt=full_prompt,
            n=1,
            size="1024x1024",
            model=model_version
        )
        return response
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def save_image(image_url, folder, file_name):
    Path(folder).mkdir(parents=True, exist_ok=True)
    try:
        img_data = requests.get(image_url).content
        with open(f"{folder}/{file_name}.png", 'wb') as handler:
            handler.write(img_data)
        print(f"Image saved as {folder}/{file_name}.png")
    except Exception as e:
        print(f"Error saving the image: {e}")

def get_detailed_prompt():
    print("Let's create a detailed prompt for DALL-E.")
    subject = input("Describe the main subject of the image: ")
    setting = input("Describe the setting/background: ")
    style_mood = input("Specify the artistic style and mood: ")
    colors_lighting = input("Mention specific colors and lighting effects: ")
    additional_elements = input("Include additional elements or details: ")
    perspective = input("Indicate the perspective and composition: ")
    return f"{subject} in a {setting}, {style_mood} style. Colors: {colors_lighting}. Details: {additional_elements}. Perspective: {perspective}"

api_key = os.getenv('YOUR_OPENAI_API_KEY')

# Collect the prompt and number of images only once
full_prompt = get_detailed_prompt()
num_images = int(input("How many images do you need to tell the story? "))

for i in range(num_images):
    generated_image = generate_image(full_prompt, api_key)
    if generated_image:
        print(f"Image {i+1} generated successfully!")
        image_url = generated_image['data'][0]['url']
        save_image(image_url, 'generated_images', f'image_{i+1}')

import requests
import os
import io
from PIL import Image

API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-3.5-large"
api_token = os.getenv('HUGGINGFACE_API_TOKEN')
if not api_token:
	raise ValueError("HUGGINGFACE_API_TOKEN environment variable is not set")

headers = {"Authorization": f"Bearer {api_token}"}
payload = {"inputs": "Astronaut riding a horse"}

def query(payload):
	response = requests.post(API_URL, headers=headers, json=payload)
	response.raise_for_status() 
	return response.content

try:
	image_bytes = query(payload)
except requests.exceptions.RequestException as e:
	print(f"An error occurred: {e}")
	image_bytes = None

if image_bytes:
	image = Image.open(io.BytesIO(image_bytes))
	image.show()
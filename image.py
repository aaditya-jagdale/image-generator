import requests
import os
import io
from PIL import Image
import time
import threading

API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-3.5-large"
api_token = os.getenv('HUGGINGFACE_API_TOKEN')
if not api_token:
	raise ValueError("HUGGINGFACE_API_TOKEN environment variable is not set")

headers = {"Authorization": f"Bearer {api_token}"}
payload = {"inputs": "A cat looking dog with a dog looking cat"}

def query(payload):
	response = requests.post(API_URL, headers=headers, json=payload)
	response.raise_for_status()
	return response.content

def loading_animation(stop_event):
	while not stop_event.is_set():
		for frame in "|/-\\":
			if stop_event.is_set():
				break
			print(f"\Generating image {frame}", end="")
			time.sleep(0.1)

try:
	stop_event = threading.Event()
	loading_thread = threading.Thread(target=loading_animation, args=(stop_event,))
	loading_thread.start()

	image_bytes = query(payload)
finally:
	stop_event.set()
	loading_thread.join()
	print("\rLoading complete!   ")

if image_bytes:
	image = Image.open(io.BytesIO(image_bytes))
	image.show()

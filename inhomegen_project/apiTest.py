import os
import requests
import base64
from PIL import Image
from io import BytesIO

# api_url = "http://127.0.0.1:5000/generate_image"  # Update with your ngrok URL if needed

# server_url = "https://0f2f-34-80-203-200.ngrok-free.app/"
server_url = "https://b391-104-196-248-71.ngrok-free.app/"
api_url = f"{server_url}generate_image"  # Update with your ngrok URL if needed

# Example payload for retro style
payload_retro = {
    # "input_prompt": "minimalistic living room",
    "input_prompt": "Generate an image of an victorian-style bedroom with a luxurious bed, adorned with classic furniture, bathed in cool lighting, ",
    "style_templateslist_id": 1,
    "look_id": 4,    #max =  7
    "styles_id": 4,  #max =  5
    "artists_id": 3, #max =  4
    "num_inference_steps": 70, #default = 30,
}

'''
        input_prompt = request.json['input_prompt']
        style_templateslist_id = request.json['style_templateslist_id']
        look_id = request.json['look_id']
        styles_id = request.json['styles_id']
        artists_id = request.json['artists_id']
'''

try:
    # Make a POST request to the API
    response_retro = requests.post(api_url, json=payload_retro)
    # print(response_retro.json())

    # Check if the request was successful (status code 200)
    if response_retro.status_code == 200:
        print(f"Image generated successfully for prompt : {payload_retro['input_prompt']}.")
        print("message : ", response_retro.json()["message"])
        print("full_prompt : ", response_retro.json()["full_prompt"])


        # Create the output directory if it doesn't exist
        output_dir = "generated_img"
        os.makedirs(output_dir, exist_ok=True)
        saved_img_path = "generated_img/current_new.jpeg"
        # image_path = response_retro.json()["image_path"]

        # Save the base64-encoded image to a file in JPEG format
        encoded_image = response_retro.json()["image_base64"]
        image_data = base64.b64decode(encoded_image)
        image = Image.open(BytesIO(image_data))
        image.save(saved_img_path)
        print(f"Image saved at: {saved_img_path}")

        # image.show()        # Open and display the saved image

    else:
        print("Error:", response_retro.json())

except Exception as e:
    print("Error:", str(e))

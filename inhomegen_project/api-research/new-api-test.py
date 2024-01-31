import os
import requests
import base64
from PIL import Image
from io import BytesIO

# api_url = "http://127.0.0.1:5000/generate_image"  # Update with your ngrok URL if needed

# server_url = "https://0f2f-34-80-203-200.ngrok-free.app/"
server_url = "https://6cb4-34-105-23-167.ngrok-free.app/"
api_url = f"{server_url}generate_image"  # Update with your ngrok URL if needed



# Map style to the corresponding prompt template for home interiors
def generate_home_interior_config(input_prompt, style_templateslist_id=0, look_id=0, styles_id=0, artists_id=0, color_palette_id=0, content_id=0, artistic_params_id=0):
    looks = ["", "modern and luxurious", "vintage and cozy", "minimalistic and sleek", "rustic and charming", "bohemian and eclectic"]
    styles = ["", "contemporary", "traditional", "industrial", "scandinavian", "mid-century modern"]
    artists = ["", "Kelly Wearstler", "Nate Berkus", "Candice Olson", "Joanna Gaines", "Philippe Starck"]


    style_templateslist = ["", "elegant", "cozy", "minimalistic", "eclectic", "industrial", "vibrant", "natural"]
    style_templates = {
        'elegant':      f'theme is an elegant home interior with sophisticated touches,',
        'cozy':         f'theme is a cozy and inviting home space with warm colors and textures,',
        'minimalistic': f'theme is a minimalistic home design focusing on simplicity and functionality,',
        'eclectic':     f'theme is an eclectic mix of styles, creating a vibrant and unique atmosphere,',
        'industrial':   f'theme is an industrial-inspired interior with raw materials and exposed elements,',
        'vibrant':      f'theme is a vibrant and lively home decor with bold colors and patterns,',
        'natural':      f'theme is a natural and organic home environment, bringing the outdoors inside,',
    }

    # resolutions = ["High Resolution (e.g., 3000x2000 pixels)", "Medium Resolution (e.g., 1500x1000 pixels)", "Low Resolution (e.g., 800x600 pixels)"]
    color_palettes = ["", "Neutral Tones (e.g., whites, grays, beiges)", "Earthy and Natural (e.g., greens, browns, muted tones)", "Vibrant and Bold (e.g., reds, blues, yellows)", "Monochromatic (e.g., shades of a single color)", "Pastel Colors (e.g., soft pinks, blues, greens)"]
    artistic_params = ["", "Texture Emphasis (e.g., emphasis on wood, stone, or fabric textures)", "Lighting Style (e.g., natural light, ambient, dramatic)", "Furniture Styles (e.g., modern, vintage, eclectic)", "Pattern Usage (e.g., geometric patterns, floral prints)", "Wall Art and Decor (e.g., paintings, sculptures, wall hangings)"]

    # Use the input_prompt and other parameters to construct the final configuration
    configuration = f'Input: {input_prompt}, '
    configuration += f'Style: {styles[styles_id]} with {style_templates[style_templateslist[style_templateslist_id]]}'
    configuration += f'Look: {looks[look_id]}, '
    configuration += f'Artist: {artists[artists_id]}, '
    configuration += f'Color Palette: {color_palettes[color_palette_id]}, '
    configuration += f'Artistic Parameters: {artistic_params[artistic_params_id]}'

    return configuration


# Example usage:
input_prompt = "Generate an image of an old-style bedroom with a luxurious king-size bed, adorned with classic furniture, bathed in warm lighting, and featuring a charming French window overlooking serene scenery, gray pallet minimalistic: tv, sofa, table"

neg_prompt = "blurry"

style_templateslist_id = 1  # Selecting "cozy" from style_templateslist
look_id = 2  # Selecting "minimalistic and sleek" from looks
styles_id = 3  # Selecting "industrial" from styles
artists_id = 1  # Selecting "interior_designer2" from artists
resolution_id = 0  # Selecting "High Resolution"
color_palette_id = 1  # Selecting "Earthy and Natural"
content_id = 4  # Selecting "Home Office"
artistic_params_id = 2  # Selecting "Furniture Styles (e.g., modern, vintage, eclectic)"

prompt = generate_home_interior_config(input_prompt, style_templateslist_id, 
                                       look_id, styles_id, artists_id, color_palette_id, artistic_params_id)


# ----------------------------------------------------------------------

# Example payload for retro style
payload_retro = {
    "input_prompt": prompt,
    "input_neg_prompt": neg_prompt,
    "num_inference_steps": 70, #default = 30,
}

'''
        input_prompt = request.json['input_prompt']
        input_neg_prompt = request.json['input_neg_prompt']
        num_inference_steps = request.json['num_inference_steps']
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





















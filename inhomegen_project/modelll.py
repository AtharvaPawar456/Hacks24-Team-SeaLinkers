from huggingface_hub import notebook_login
# Set the details for your model here:
my_prompt_trigger = "green frog "
hf_username = "TimothyAlexisVass"
hf_modelname = "my-model-name"
checkpoint = "sdxl-dreambooth-lora-000016.safetensors"

import torch

from diffusers import DiffusionPipeline, AutoencoderKL

vae = AutoencoderKL.from_pretrained("madebyollin/sdxl-vae-fp16-fix", torch_dtype=torch.float16)
base = DiffusionPipeline.from_pretrained("stabilityai/stable-diffusion-xl-base-1.0",
    vae=vae,
    torch_dtype=torch.float16,
    variant="fp16",
    use_safetensors=True,
)
# base.load_lora_weights(f"{hf_username}/{hf_modelname}", weight_name=checkpoint)

_ = base.to("cuda")

from flask import Flask, request, jsonify
from flask_ngrok import run_with_ngrok
import base64
from PIL import Image


import os
import zipfile
import random


def imgGen_llm(prompt, num_inference_steps=20):
    # my_prompt_trigger = "green frog "

    # prompt = f"Blazing colorportrait of {my_prompt_trigger} as cyberpunk cyborg in black polished metal armor looking determined, futuristic duotone background"
    quality = "intricate details even to the smallest particle, extreme detail of the enviroment, sharp portrait, well lit, interesting outfit, beautiful shadows, bright, photoquality, ultra realistic, masterpiece, 8k"
    negative_prompt = "ugly, old, boring, photoshopped, tired, wrinkles, scar, gray hair, big forehead, crosseyed, dumb, stupid, cockeyed, disfigured, blurry, assymetrical, unrealistic, grayscale, black and white, bald, high hairline, balding, receeding hairline, grayscale, bad anatomy, unnatural irises, no pupils, blurry eyes, dark eyes, extra limbs, deformed, disfigured eyes, out of frame, no irises, assymetrical face, broken fingers, extra fingers, disfigured hands"
    num_samples = 1
    guidance_scale = 8
    # num_inference_steps = 30
    height = 1024
    width = 1024
    seed = random.randint(1, 99999)


    # Set this to the folder you want to save the image to in Google Drive
    output_dir = "C:/Users/Shaun/Downloads/content"
    os.makedirs(output_dir, exist_ok=True)

    images = base(
        prompt + ". " + quality,
        height=height,
        width=width,
        negative_prompt=negative_prompt,
        num_images_per_prompt=num_samples,
        num_inference_steps=num_inference_steps,
        guidance_scale=guidance_scale,
        generator=torch.manual_seed(seed)
    ).images

    for image in images:
        # display(image)
        # img_path = os.path.join(output_dir, f"content/generated_img/gen_image.jpeg")
        image.save("C:/Users/Shaun/Downloads/content/generated_img/gen_image.jpeg")
        
app = Flask(__name__)
run_with_ngrok(app)

@app.route("/")
def hello():
    return "Hello, I am Generating Dreambooth SDXL LLM Model used to generate 4K images based on prompt given, \n Enjoy !!!, \n\n Api Working : Home Route ..."


@app.route('/generate_image', methods=['POST'])
def generate_image():
    try:
        # Get parameters from the request
        input_prompt = request.json['input_prompt']
#         style_templateslist_id = request.json['style_templateslist_id']
#         look_id = request.json['look_id']
#         styles_id = request.json['styles_id']
#         artists_id = request.json['artists_id']
#         num_inference_steps = request.json['num_inference_steps']

        # Map style to the corresponding prompt template
        def templateEdit( input_prompt, style_templateslist_id=0, look_id=0, styles_id=0, artists_id=0):
          looks = ["", "confident and wealthy", "heroic in high-tech armor", "fantastically luxurious", "peaceful and smiling", "sharp with jewellery", "gritty and realistic", "colorful and vibrant"]
          styles = ["", "colorful sci-fi", "vibrant fantasy", "detailed steampunk", "glorious cyberpunk", "retro futuristic"]
          artists = ["", "alejandro burdisio", "alena aenami", "alex alemany", "alex andreev"]

          style_templateslist = ["", "retro", "artistic", "painting", "realistic", "animated", "anime", "filters", "dreaming"]
          style_templates = {
                'retro':    f'theme is a retro style artwork with a nostalgic touch,',
                'artistic': f'theme is an artistic creation with unique and vibrant elements,',
                'painting': f'theme is a beautiful painting capturing the natural essence of ,',
                'realistic':f'theme is a realistic scene ,',
                'animated': f'theme is an with imagination, ',
                'anime':    f'theme is an anime-inspired illustration with futuristic elements,',
                'filters':  f'theme is a photograph enhanced with artistic filters,',
                'dreaming': f'theme is a dreamy and surreal composition,'

          }
          # return style_templates['style']
          # ret_text = f"{style_templates.get(style, input_prompt)}"

          complete_prompt = f"{style_templates[style_templateslist[style_templateslist_id]]} and Portrait of {input_prompt} looking {looks[look_id]} by {artists[artists_id]} in {styles[styles_id]} style"

          # complete_prompt = f"Portrait of {my_prompt_trigger} looking {looks[look_id]} by {artists[artists_id]} in {styles[styles_id]} style"
          return complete_prompt



        # Use the specified style or fallback to a default prompt
#         prompt = templateEdit(input_prompt, style_templateslist_id, look_id, styles_id, artists_id)
        print("input_prompt : ", input_prompt)
              
        # Generate the image using the DiffusionPipeline
        imgGen_llm(input_prompt, num_inference_steps)

        # # Save the generated image
        image_path = f"C:/Users/Shaun/Downloads/content/generated_img/gen_image.jpeg"
#         image_path = f"/content/content/generated_img/gen_image.jpeg"

        # Encode the image into base64
        with open(image_path, "rb") as image_file:
            encoded_image = base64.b64encode(image_file.read()).decode('utf-8')

        # Return the path and base64-encoded image as the API response
        return jsonify({"message": "Image generated successfully using Generating Dreambooth SDXL", "image_path": image_path, "image_base64": encoded_image, "full_prompt": prompt})

    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == "__main__":
    app.run()

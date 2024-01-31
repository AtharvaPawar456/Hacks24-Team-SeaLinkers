from flask import Flask, request, jsonify
from flask_ngrok import run_with_ngrok
import base64
from PIL import Image


import os
import zipfile
import random


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
        input_neg_prompt = request.json['input_neg_prompt']
        num_inference_steps = request.json['num_inference_steps']


        # print(prompt)

        # Use the specified style or fallback to a default prompt
        # prompt = templateEdit(input_prompt, style_templateslist_id, look_id, styles_id, artists_id)

        # Generate the image using the DiffusionPipeline
        imgGen_llm(input_prompt, input_neg_prompt, num_inference_steps)

        # # Save the generated image
        image_path = f"/content/generated_img/gen_image.png"
        image_path = f"/content/content/generated_img/gen_image.jpeg"

        # Encode the image into base64
        with open(image_path, "rb") as image_file:
            encoded_image = base64.b64encode(image_file.read()).decode('utf-8')

        # Return the path and base64-encoded image as the API response
        return jsonify({"message": "Image generated successfully using Generating Dreambooth SDXL", "image_path": image_path, "image_base64": encoded_image, "full_prompt": input_prompt})

    except Exception as e:
        return jsonify({"error": str(e)})
    







def imgGen_llm(prompt, input_negative_prompt, num_inference_steps=30):
    # my_prompt_trigger = "green frog "

    # prompt = f"Blazing colorportrait of {my_prompt_trigger} as cyberpunk cyborg in black polished metal armor looking determined, futuristic duotone background"
    censored = "Utilize the model to generate high-resolution home interior images with intricate details, emphasizing realistic textures, lighting, and diverse furniture styles. Create well-lit, visually appealing scenes, focusing on specific rooms such as living rooms, bedrooms, kitchens, bathrooms, home offices, dining rooms, and outdoor spaces. Exclude human figures and ensure the absence of explicit or suggestive content. Avoid generating blurry images. Provide options for different resolutions, color palettes, and artistic parameters, allowing users to tailor the generated images to their preferences. Ensure the exclusion of undesirable features outlined in the negative prompt, such as ugliness, old age, boredom, photoshopped appearances, tiredness, wrinkles, scars, gray hair, and other imperfections. Strive for photo-quality, ultra-realistic results, resembling masterpieces in 8k resolution, maintaining sharpness and well-lit compositions throughout the diverse range of generated home interiors."

    quality = "intricate details even to the smallest particle, extreme detail of the enviroment, sharp portrait, well lit, interesting outfit, beautiful shadows, bright, photoquality, ultra realistic, masterpiece, 8k"
    
    negative_prompt = f"ugly, old, boring, photoshopped, tired, wrinkles, scar, gray hair, big forehead, crosseyed, dumb, stupid, cockeyed, disfigured, blurry, assymetrical, unrealistic, grayscale, black and white, bald, high hairline, balding, receeding hairline, grayscale, bad anatomy, unnatural irises, no pupils, blurry eyes, dark eyes, extra limbs, deformed, disfigured eyes, out of frame, no irises, assymetrical face, broken fingers, extra fingers, disfigured hands {input_negative_prompt}"
    
    num_samples = 1
    guidance_scale = 8
    # num_inference_steps = 30
    height = 1024
    width = 1024
    seed = random.randint(1, 99999)


    # Set this to the folder you want to save the image to in Google Drive
    output_dir = "content/generated_img"
    os.makedirs(output_dir, exist_ok=True)

    images = base(
        prompt + ". " + censored + quality,
        height=height,
        width=width,
        negative_prompt=negative_prompt ,
        num_images_per_prompt=num_samples,
        num_inference_steps=num_inference_steps,
        guidance_scale=guidance_scale,
        generator=torch.manual_seed(seed)
    ).images

    for image in images:
        # display(image)
        # img_path = os.path.join(output_dir, f"content/generated_img/gen_image.jpeg")
        image.save("content/generated_img/gen_image.jpeg")

if __name__ == "__main__":
    app.run()

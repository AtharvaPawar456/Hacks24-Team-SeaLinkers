#  i have created this file - GTA
from datetime import datetime
# import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import UserData, ImgDetails
import random
import os
import requests
import json
import ast, subprocess, re
from ultralytics import YOLO

from IPython.display import display, Image

from django.utils import timezone
from fuzzywuzzy import fuzz, process



from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout, logout

from django.contrib.auth.decorators import login_required

from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt


from django.conf import settings
from django.core.files.storage import FileSystemStorage
import urllib.request
import base64
import json
import time
import os

import vtracer


webui_server_url = 'http://127.0.0.1:7860'
out_dir = r"C:\Users\Shaun\Desktop\Hackathons\TSEC 2024\inHomeGen\inhomegen_project\inhome_app\static\inhome_app\generatedimg"
# media_full_path = settings.MEDIA_ROOT + "\playapp_data"
# upload_file_full_path = settings.STATIC_MEDIA_ROOT + "\\static\\bandapp\\uploaded_files"
# results_full_path = settings.STATIC_MEDIA_ROOT + "\\static\\bandapp\\ResultsFiles"

# bandapp\static\bandapp\uploaded_files
# C:\\Users\\Atharva Pawar\\Documents\\GitHub\\SECUIRX-v2\\securix_v2_project\\bandapp\\static\\playapp\\ResultsFiles\\codeGoat.py


# media_full_path = settings.MEDIA_ROOT + "\playapp_data"
media_full_path = settings.STATIC_MEDIA_ROOT + "\\static\\inhome_app\\generatedimg"

product_file = settings.STATIC_MEDIA_ROOT + "\\static\\inhome_app\\setup\\demo.json"
svg_file = settings.STATIC_MEDIA_ROOT + "\\static\\inhome_app\\setup\\test.svg"


# Create your views here.
def index(request):
    # return HttpResponse('Securix V2    |      index Page')
    return render(request,'inhome_app/welcome.html')

# def showresult(request):
    # return HttpResponse('Securix V2    |      index Page')
    # return render(request,'inhome_app/showresult.html')

# def addproject(request):
#     # return HttpResponse('Securix V2    |      index Page')
#     return render(request,'inhome_app/addproject.html')

def img2svg(inp, out):
    # Minimal example: use all default values, generate a multicolor SVG
    vtracer.convert_image_to_svg_py(inp, out)

    # Single-color example. Good for line art, and much faster than full color:
    vtracer.convert_image_to_svg_py(inp, out, colormode='binary')

    # All the bells & whistles
    vtracer.convert_image_to_svg_py(inp, out, colormode = 'color',         hierarchical = 'stacked',    mode = 'spline',             filter_speckle = 4,          color_precision = 6,         layer_difference = 16,       corner_threshold = 60,       length_threshold = 4.0,       max_iterations = 10,         splice_threshold = 45,       path_precision = 3)

def convert_image_to_svg(request, myid):
    # Assuming the image is associated with the provided ID in your model
    image_object = ImgDetails.objects.get(id=myid)
    input_image_path = image_object.path  # Adjust this based on your model structure
    # output_svg_path = "path/to/your/output.svg"
    output_svg_path = svg_file

# <a href="{% url 'convert_image_to_svg' myid=myid %}" download="output.svg">Download SVG</a>

    img2svg(input_image_path, output_svg_path)

    # Read the generated SVG content
    with open(output_svg_path, 'r') as svg_file:
        svg_content = svg_file.read()

    # Provide the SVG as a downloadable file
    dataresponse = HttpResponse(svg_content, content_type="image/svg+xml")
    dataresponse['Content-Disposition'] = f'attachment; filename="{image_object.image.name}.svg"'

    return dataresponse


@login_required
def gallery(request):

    logedIn_user = request.user.username
    
    imgData = ImgDetails.objects.all()


    # Pass the data to the template
    context = {'imgData': imgData}
    
    return render(request, 'inhome_app/gallery.html', context)


@login_required
def addproject(request):
    if request.method == 'POST':
        proj_name   = request.POST.get('proj_name')

        user_name   = request.user.username

        dataandtime = timezone.now()
        pub_date     = dataandtime.date()
        pub_time     = dataandtime.strftime('%H:%M:%S')

        jsonData = ''
        
        # Create a new node
        # ProjectDetails.objects.create(name=proj_name, user_name=user_name,  pub_date=pub_date, pub_time=pub_time, jsonData=jsonData)

        # Redirect to a success page or another view
        return redirect('dashboard')  # Change 'node_list' to the actual URL name for the node list view

    return render(request,'inhome_app/addproject.html')






@login_required
def dashboard(request):

    logedIn_user = request.user.username
    
    # Query the database to get all records for the logged-in user
    # userData = ProjectDetails.objects.filter(user_name=logedIn_user)
    # userData = ImgDetails.objects.filter(user_name=logedIn_user, projName=proj_name)


    # Pass the data to the template
    context = {'userData': ""}
    
    return render(request, 'inhome_app/index.html', context)



@login_required
def viewprojects(request):

    # Get the logged-in user's username
    logedIn_user = request.user.username
    
    # Query the database to get all records for the logged-in user
    # userData = ProjectDetails.objects.filter(user_name=logedIn_user)
    unique_proj_names = ImgDetails.objects.filter(user_name=logedIn_user).values_list('projName', flat=True).distinct()


    # Pass the data to the template
    context = {'imgData': unique_proj_names,}
    
    return render(request, 'inhome_app/viewproj.html', context)



@login_required
def dashboard_v2(request, proj_name):

    # Get the logged-in user's username
    logedIn_user = request.user.username
    
    # Query the database to get all records for the logged-in user
    # userData = ProjectDetails.objects.filter(user_name=logedIn_user)
    imgData = ImgDetails.objects.filter(user_name=logedIn_user, projName=proj_name)



    # Pass the data to the template
    context = {'imgData': imgData, 'proj_name' : proj_name}
    
    return render(request, 'inhome_app/index.html', context)


def imagedetection(path):
    with open('output.txt', 'w') as file:
    # Run the yolo command and redirect both stdout and stderr to the file
        command = f"yolo task=detect mode=predict model=yolov8n.pt conf=0.25 source={path} save=True"
        process = subprocess.Popen(command, shell=True, stdout=file, stderr=subprocess.STDOUT, text=True)

        # Wait for the command to complete
        process.wait()
    with open('output.txt', 'r') as file:
        text=file.read()


    # Define a regular expression pattern to extract detected objects
    pattern = re.compile(r'image \d+/\d+ .*: \d+x\d+ (.+)')
    matches = pattern.findall(text)

    # Extracted objects are in the first capturing group of the pattern
    objects={}
    if matches:
        detected_objects = matches[0].split(', ')
        print("Detected Objects:")
        for obj in detected_objects:
            print(obj)
            if any(map(str.isdigit, obj[1:])):
                pass
            else: 
                objects[f"{obj[1:]}"]=obj[0]
    else:
        print("No objects detected.")
        objects["Objects"]="None"
    return str(objects).replace('\'','"')

@login_required
def Budget(request, genimgid):

    # Get the logged-in user's username
    logedIn_user = request.user.username
    
    # Query the database to get all records for the logged-in user
    # userData = ProjectDetails.objects.filter(user_name=logedIn_user)
    imgData = ImgDetails.objects.filter(user_name=logedIn_user, id=genimgid).first()

    # Convert the string to a list using ast.literal_eval
    # objects_init_list = ast.literal_eval(imgData.objectsinit)


    # Read the JSON data from the file
    with open(product_file, 'r') as file:
        product_data = json.load(file)

    # print("product_data : ", product_data)

    # List of products to match
    product_list = json.loads(imgData.objectsinit)
    product_list_keys=list(product_list.keys())
    product_data_keys=[]
    for i in range(10):
        product_data_keys.append(list(product_data[i].keys())[0])
    print(product_data_keys,product_list_keys)
    # Function to perform fuzzy string matching
    def match_products(product_list, product_data):
        matches = {}

        for product in product_list:
            best_match = None
            best_score = 0

            # Iterate through each dictionary in product_data
            for category_dict in product_data:
                for affordability_levels in category_dict.items():
                    # Iterate through the affordability levels in each category
                    for affordability, products in affordability_levels.items():
                        # Iterate through the products in each affordability level
                        for product_info in products:
                            # Perform fuzzy matching with the product name
                            score = fuzz.token_set_ratio(product, product_info['name'])

                            # Update the best match if the current score is higher
                            if score > best_score:
                                best_score = score
                                best_match = product_info

            # Check if the best match score is above a certain threshold (adjust as needed)
            if best_score >= 80:
                matches[product] = best_match

        return matches

    # Perform fuzzy string matching
    # matched_products = match_products(product_list_keys, product_data)
    matched_products={"Table":"1","Chair":"2"}
    # Print the matched products    
    # for key, value in matched_products.items():
    #     print(f'Matched: {key} -> {value["name"]}')

    # Pass the data to the template
    fin=json.loads( imgData.objectsinit)
    context = {'imgData': imgData, 'proj_name' : genimgid, 'objects_init_list' :fin}
    
    return render(request, 'inhome_app/budget.html', context)



def timestamp():
    return datetime.fromtimestamp(time.time()).strftime("%Y%m%d-%H%M%S")


@login_required
def revision(request):

    if request.method == 'POST':
        genimgid   = request.POST.get('genimgid')
        print("Important\n",genimgid)
        proj_name = request.POST.get('proj_name')
        # selected_room = request.POST.get('selectedroom')
        # selected_model = request.POST.get('selectedmodel')  # Assuming this is intentional

        style = 'minimal design'

        prompt = request.POST.get('prompt')
        negative_prompt = request.POST.get('negativePrompt')


        dataandtime = timezone.now()
        pub_date     = dataandtime.date()
        pub_time     = dataandtime.strftime('%H:%M:%S')

        
        # Create a new node
        # ProjectDetails.objects.create(name=proj_name, user_name=user_name,  pub_date=pub_date, pub_time=pub_time, jsonData=jsonData)


        # return render(request,'inhome_app/addproject.html')

        logedIn_user = request.user.username
        
        # userData = ProjectDetails.objects.filter(user_name=logedIn_user)
        imgData = ImgDetails.objects.filter(user_name=logedIn_user, id=genimgid).first()

        # prompt = "Add candles in the room and make"
        filename = f"{imgData.projName}_v{str(imgData.id)}_{timestamp()}"
        print("Hello",imgData.path)
        newpath = img2img(prompt,imgData.path, filename)

        detections=imagedetection(newpath)


        ImgDetails.objects.create(user_name=logedIn_user, projName=proj_name, roomName="", prompt=prompt, negprompt="", modelName="", style=style, path=newpath, objectsinit=detections, pub_date=pub_date, pub_time=pub_time)

        imgData = ImgDetails.objects.filter(user_name=logedIn_user)

        # Pass the data to the template
        context = {'imgData': imgData, 'proj_name' : genimgid}
        
        # return redirect('dashboard')
        # return redirect('dashboard_v2', proj_name=proj_name)
        return render(request, 'inhome_app/index.html', context)  # Change 'node_list' to the actual URL name for the node list view


    else:
        # if request.method == 'GET':
        # Get parameters from the GET request
        genimgid = request.GET.get('genimgid', '')

        logedIn_user = request.user.username
        
        # userData = ProjectDetails.objects.filter(user_name=logedIn_user)
        imgData = ImgDetails.objects.filter(user_name=logedIn_user, id=genimgid).first()

        context = {'imgData': imgData, 'genimgid' : genimgid}

        # Redirect to a success page or another view
        return render(request, 'inhome_app/revision.html', context)  # Change 'node_list' to the actual URL name for the node list view

# http://example.com/revision/?genimgid=your_project_name





@login_required
def generate(request):
    if request.method == 'POST':
        # Get the values from the form
        proj_name = request.POST.get('proj_name')
        selected_room = request.POST.get('selectedroom')
        selected_model = request.POST.get('selectedmodel')  # Assuming this is intentional

        _style_templateslist_id = int(request.POST.get('style_templateslist_id'))  
        _looks = int(request.POST.get('looks'))  
        _styles = int(request.POST.get('styles'))  
        _artists = int(request.POST.get('artists'))  
        _color_palettes = int(request.POST.get('color_palettes'))  
        _artistic_params = int(request.POST.get('artistic_params'))  
        
 




        prompt = request.POST.get('prompt')
        negative_prompt = request.POST.get('negativePrompt')

        logedIn_user = request.user.username

        dataandtime = timezone.now()
        pub_date     = dataandtime.date()
        pub_time     = dataandtime.strftime('%H:%M:%S')


        # Print the values to the terminal
        print(f"Project Name: {proj_name}")
        print(f"Selected Room: {selected_room}")
        print(f"Selected Model: {selected_model}")
        print(f"Prompt: {prompt}")
        print(f"Negative Prompt: {negative_prompt}")


        print("_style_templateslist_id : ", _style_templateslist_id)  
        print("_looks : ", _looks)  
        print("_styles : ", _styles)  
        print("_artists : ", _artists)  
        print("_color_palettes : ", _color_palettes)  
        print("_artistic_params : ", _artistic_params) 

        style = 'minimal design'

        # Get the last ImgDetails object
        last_img_details = ImgDetails.objects.last()

        # Calculate the next ID
        next_id = last_img_details.id + 1 if last_img_details else 1
        

        # Add further processing logic here, if needed
        path = generate_img_reqapi(prompt, negative_prompt, img_id=next_id, 
                style_templateslist_id=_style_templateslist_id, look_id=_looks, styles_id=_styles, artists_id=_artists, color_palette_id=_color_palettes, artistic_params_id=_artistic_params)
        print("rev path : ", path)
        # path = testpath(text="hello world", img_id=12)
        detections=imagedetection(path)
        print("object detections : ", detections)

        


        # Create a new node
        ImgDetails.objects.create(user_name=logedIn_user, projName=proj_name, roomName=selected_room, prompt=prompt, negprompt=negative_prompt, modelName=selected_model, style=style, path=path, objectsinit=detections, pub_date=pub_date, pub_time=pub_time)

        # Redirect to a success page or another view
        return redirect('dashboard_v2', proj_name=proj_name)

    return render(request,'inhome_app/addproject.html')




@login_required
def addroom(request):
    if request.method == 'POST':
        proj_name   = request.POST.get('proj_name')
        room_name   = request.POST.get('room_name')

        user_name   = request.user.username

        userData = "ProjectDetails.objects.filter(user_name=user_name, name=proj_name)"

        if userData:
            for entry in userData:
                if entry.jsonData:
                    json_data = json.loads(entry.jsonData)


        project_details = "get_object_or_404(ProjectDetails, user_name=user_name, name=proj_name)"

        # Update the jsonData field
        new_json_data = f'{"updated_key": room_name}'  # Replace with your updated JSON data
        json_data[room_name]=""
        project_details.jsonData = new_json_data

        # Save the changes to the database
        project_details.save()


        # jsonData = ''
        
        # Create a new node
        # ProjectDetails.objects.create(name=proj_name, user_name=user_name,  pub_date=pub_date, pub_time=pub_time, jsonData=jsonData)

        # Redirect to a success page or another view
        return redirect('dashboard')  # Change 'node_list' to the actual URL name for the node list view

    return render(request,'inhome_app/addproject.html')



'''
project_id = 1  # Replace with the actual ID

# Retrieve the ProjectDetails object
project_details = get_object_or_404(ProjectDetails, id=project_id)

# Update the jsonData field
new_json_data = '{"updated_key": "updated_value"}'  # Replace with your updated JSON data
project_details.jsonData = new_json_data

# Save the changes to the database
project_details.save()

'''




@login_required
def view_data(request):
    if request.method == 'GET':
        # Get parameters from the GET request
        proj_name = request.GET.get('proj', '')

        logedIn_user = request.user.username


        # Validate the proj_name
        userData = "ProjectDetails.objects.filter(user_name=logedIn_user, name=proj_name)"
        # userData = ProjectDetails.objects.filter(user_name=logedIn_user, name=proj_name).first()

        # Initialize an empty list to store the keys
        jsonKeys = []
        # json_data = {}

        allViewPlace = {}

        if userData:
            # _json_data = json.loads(userData.jsonData)

            # Convert jsonData field to Python dictionary and extract keys
            for entry in userData:
                if entry.jsonData:
                    json_data = json.loads(entry.jsonData)
                    keys = list(json_data.keys())
                    # val=list(json_data.values())

                    jsonKeys.extend(keys)
            # print(json_data['hall'])
            # print(json_data)

            # Remove duplicates if needed
            jsonKeys = list(set(jsonKeys))
            print(jsonKeys)

            for item in jsonKeys:
                values = json_data[item]
                imgData = imgData = ImgDetails.objects.filter(id__in=values)

                if imgData != None:
                    print("userData : ", item)
                    # allViewPlace.append(imgData)
                    
                    # Iterate over the imgData queryset and add each record to allViewPlace
                    for img_entry in imgData:
                        allViewPlace[img_entry.id] = {
                            'user_name': img_entry.user_name,
                            'prompt': img_entry.prompt,
                            'negprompt': img_entry.negprompt,
                            'style': img_entry.style,
                            'path': img_entry.path,
                            'pub_date': img_entry.pub_date,
                            'pub_time': img_entry.pub_time,
                        }

                    print("imgData : ", imgData)

        print("allViewPlace : ", allViewPlace)

        
        # Pass the data to the template
        context = {'userSensorData': userData, 'viewJson': jsonKeys, 'allViewPlace': allViewPlace, 'proj_name':proj_name}
    

        return render(request, 'inhome_app/viewproj.html', context)
        
    else:
        return redirect('view_data')

'''

http://127.0.0.1:8000/view_data/?proj=alpha
'''





















import os
import requests
import base64
from PIL import Image
from io import BytesIO

def generate_img_reqapi(input_prompt, negative_prompt, img_id, style_templateslist_id=0, look_id=0, styles_id=0, artists_id=0, color_palette_id=0, artistic_params_id=0):

    # api_url = "http://127.0.0.1:5000/generate_image"  # Update with your ngrok URL if needed

    # server_url = "https://0f2f-34-80-203-200.ngrok-free.app/"
    server_url = "https://7ab6-35-240-206-94.ngrok-free.app/"
    api_url = f"{server_url}generate_image"  # Update with your ngrok URL if needed






    # Example usage:
    # input_prompt = "Generate an image of an old-style bedroom with a luxurious king-size bed, adorned with classic furniture, bathed in warm lighting, and featuring a charming French window overlooking serene scenery, gray pallet minimalistic: tv, sofa, table"

    # neg_prompt = "blurry"         

    style_templateslist_id = 1  # Selecting "cozy" from style_templateslist 
    look_id = 2  # Selecting "minimalistic and sleek" from looks
    styles_id = 3  # Selecting "industrial" from styles
    artists_id = 1  # Selecting "interior_designer2" from artists
    color_palette_id = 1  # Selecting "Earthy and Natural"
    artistic_params_id = 2  # Selecting "Furniture Styles (e.g., modern, vintage, eclectic)"

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

    prompt = generate_home_interior_config(input_prompt, style_templateslist_id, 
                                        look_id, styles_id, artists_id, color_palette_id, artistic_params_id)

    print("prompt :", prompt)

    # Example payload for retro style
    payload_retro = {
        "input_prompt": prompt,
        "input_neg_prompt": negative_prompt,
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
            # file_path = media_full_path + "\\" + img_id + "genimg.jpeg"
            file_path = os.path.join(media_full_path, f"{str(img_id)}genimg.jpeg")

            print("api download - video file_path: ", file_path)

            # os.makedirs(file_path, exist_ok=True)
            # saved_img_path = "current_new.jpeg"
            # image_path = response_retro.json()["image_path"]

            # Save the base64-encoded image to a file in JPEG format
            encoded_image = response_retro.json()["image_base64"]
            image_data = base64.b64decode(encoded_image)
            image = Image.open(BytesIO(image_data))
            image.save(file_path)

            
            print(f"Image saved at: {file_path}")
            return file_path

            # image.show()        # Open and display the saved image

        else:
            print("Error:", response_retro.json())

    except Exception as e:
        print("Error:", str(e))




def testpath(text, img_id):
    # Define the file path
    # path = media_full_path + "\\" + img_id + "genimg.jpeg"

    file_path = os.path.join(media_full_path, f"{str(img_id)}_output.txt")

    # Save the text to the file
    with open(file_path, 'w') as file:
        file.write(text)
    print("file_path :", file_path)
    return file_path

# C:\\Users\\Atharva Pawar\\Documents\\GitHub\\Hacks24-Team-SeaLinkers\\inhomegen_project\\securixapp\\static\\inhome_app\\generatedimg\\12_output.txt

# C:\Users\Atharva Pawar\Documents\GitHub\Hacks24-Team-SeaLinkers\inhomegen_project\inhome_app\static\inhome_app\generatedimg\gen1.jpeg

def encode_file_to_base64(path):
    with open(path, 'rb') as file:
        return base64.b64encode(file.read()).decode('utf-8')


def decode_and_save_base64(base64_str, save_path):
    with open(save_path, "wb") as file:
        file.write(base64.b64decode(base64_str))


def call_api(api_endpoint, **payload):
    data = json.dumps(payload).encode('utf-8')
    request = urllib.request.Request(
        f'{webui_server_url}/{api_endpoint}',
        headers={'Content-Type': 'application/json'},
        data=data,
    )
    response = urllib.request.urlopen(request)
    return json.loads(response.read().decode('utf-8'))




def call_img2img_api(filename,**payload):
    response = call_api('sdapi/v1/img2img', **payload)
    for index, image in enumerate(response.get('images')):
        # save_path = os.path.join(out_dir_i2i, f'img2img-{timestamp()}-{index}.png')
        save_path = out_dir+f"\{filename}"+".png"
        decode_and_save_base64(image, save_path)
    return save_path

def img2img(prompt,path,filename):
    init_images = [
        # encode_file_to_base64(r"C:\Users\Shaun\Downloads\current_new.jpeg.jpg"),
        encode_file_to_base64(path),

        # encode_file_to_base64(r"B:\path\to\img_2.png"),
        # "https://image.can/also/be/a/http/url.png",
    ]

    batch_size = 1
    payload = {
        "prompt": prompt,
        "seed": -1,
        "steps": 20,
        "width": 512,
        "height": 512,
        "denoising_strength": 0.58,
        # "denoising_strength": 0.78,
        "cfg_scale": 7,
        "sampler_name": "DPM++ 2M Karras",
        "n_iter": 1,
        "init_images": init_images,
        "batch_size": batch_size if len(init_images) == 1 else len(init_images),
        "alwayson_scripts": {
            "Refiner": {
                "args": [
                    True,
                    # "sd_xl_refiner_1.0",
                    "v1-5-pruned-emaonly.safetensors [6ce0161689]",
                    0.5
                ]
            }
        }
    }
    # if len(init_images) > 1 then batch_size should be == len(init_images)
    # else if len(init_images) == 1 then batch_size can be any value int >= 1
    return call_img2img_api(filename,**payload)





# API : sensor_latest_data 
# # @csrf_exempt
# def sensor_latest_data(request):
#     if request.method == 'GET':
#         # Get parameters from the GET request
#         _user_name = request.GET.get('user_name', '')
#         _api_key = request.GET.get('api_key', '')

#         # Validate the username, API key, and nodename
#         user_node_data = UserData.objects.filter(user_name=_user_name, api_key=_api_key).first()

#         if user_node_data:
#             latest_sensor_data = SensorData.objects.filter(user_name=_user_name).order_by('-pub_date', '-pub_time').first()

#             if latest_sensor_data:
#                 # Serialize the data into a dictionary
#                 serialized_data = {
#                     'user_name': latest_sensor_data.user_name,
#                     'pub_date': latest_sensor_data.pub_date,
#                     'pub_time': latest_sensor_data.pub_time,
#                     'heartPulse': latest_sensor_data.heartPulse,
#                     'dhtTemp': latest_sensor_data.dhtTemp,
#                     'dhtHum': latest_sensor_data.dhtHum,
#                     'gyrometer': [latest_sensor_data.gyroX, latest_sensor_data.gyroY, latest_sensor_data.gyroZ],
                    
#                     'accelerometer': [latest_sensor_data.acceleroX, latest_sensor_data.acceleroY, latest_sensor_data.acceleroZ]
#                 }
#                 return JsonResponse(serialized_data)
            
#             else:
#                 return JsonResponse({'error': 'No data found for the specified user_name'}, status=404)        


#             # return JsonResponse({'status': 'success'})
        
#         else:
#             return JsonResponse({'status': 'error', 'message': 'Invalid username or API key'})



# @csrf_exempt
# def sensor_data(request):
#     if request.method == 'GET':
#         # Get parameters from the GET request
#         _user_name = request.GET.get('user_name', '')

#         _api_key = request.GET.get('api_key', '')

#         _heartPulse = float(request.GET.get('heartPulse', None))
#         _dhtTemp = float(request.GET.get('dhtTemp', None))
#         _dhtHum = float(request.GET.get('dhtHum', None))

#         _gyroX = float(request.GET.get('gyroX', None))
#         _gyroY = float(request.GET.get('gyroY', None))
#         _gyroZ = float(request.GET.get('gyroZ', None))

#         _acceleroX = float(request.GET.get('acceleroX', None))
#         _acceleroY = float(request.GET.get('acceleroY', None))
#         _acceleroZ = float(request.GET.get('acceleroZ', None))

#         dataandtime = timezone.now()

#         # current_date = dataandtime.date()
#         current_time = dataandtime.strftime('%H:%M:%S')



#         # Validate the username, API key, and nodename
#         user_node_data = UserData.objects.filter(user_name=_user_name, api_key=_api_key).first()

#         if user_node_data:
#             # Save data to the database
#             sensor_data = SensorData(
#                 user_name=_user_name,

#                 heartPulse = _heartPulse,
#                 dhtTemp    = _dhtTemp,
#                 dhtHum = _dhtHum,
            
#                 gyroX=_gyroX,
#                 gyroY=_gyroY,
#                 gyroZ=_gyroZ,

#                 acceleroX = _acceleroX,
#                 acceleroY = _acceleroY,
#                 acceleroZ = _acceleroZ,

#                 pub_date=dataandtime,
#                 pub_time=current_time
#             )
#             sensor_data.save()

#             return JsonResponse({'status': 'success'})
        
#         else:
#             return JsonResponse({'status': 'error', 'message': 'Invalid username or API key'})

#     return JsonResponse({'status': 'error', 'message': 'Invalid request method'})



# def upload_file(request):
#     if request.method == 'POST':

#         title = request.POST.get('title')
#         mode = request.POST.get('mode')
#         code_file = request.FILES['code_file']

#         # Print the logged-in user's name to the console
#         # if request.user.is_authenticated:
#             # print("Logged-in User:", request.user.username)
        
#         logedIn_user = request.user.username

#         # Save the file to the specified location
#         file_path = f"{upload_file_full_path}\\{logedIn_user}_{code_file.name}"

#         if not os.path.exists(file_path):
#             # If the file doesn't exist, create it
#             os.makedirs(os.path.dirname(file_path), exist_ok=True)

#         # Assuming code_file is the uploaded file
#         with open(file_path, 'wb') as destination:
#             for chunk in code_file.chunks():
#                 destination.write(chunk)

#         result_file_path = f"{results_full_path}\\{logedIn_user}_{title}.json"

#         scan_file_final(file_path, result_file_path, mode = mode)


#         # Create a database entry if needed
#         SecurityFinding.objects.create(user_name=logedIn_user, file_name=title, file_path=file_path,result_file_path=result_file_path)

#         # Print the file name and path on the terminal
#         print(f"File title: {title}")
#         print(f"File Name: {code_file.name}")
#         print(f"File Path: {file_path}")

#         # Redirect to the dashboard or any desired page
#         return redirect('dashboard')  # Replace 'dashboard' with the actual URL or view name

#     return redirect('dashboard')  


# domain_link = "https://045d-35-229-130-116.ngrok-free.app/"

# def scan_file(mode='regex'):
# def scan_file_final(file_path, result_file_path, mode):
#     print("upload_GitLink() function running ...")
#     # url = "http://localhost:5000/download_repo"
#     # url = f"{domain_link}scanrepo"
#     url = f"{domain_link}file_scan"

#     # mode = 'regex'
#     # mode = 'semgrep'

#     # file_path = "api_sample_uploads\codeGoat - Copy (2).c++"
#     # file_path = "api_sample_uploads\codeGoat - Copy.java"
#     # file_path = "api_sample_uploads\codeGoat.py"

#     # Extract the file name
#     file_name = os.path.basename(file_path)

#     # Prepare the file content and other data
#     files = {'file_content': (file_name, open(file_path, 'r'))}
#     data = {'file_name': file_name, 'mode': mode}

#     response = requests.post(url, files=files, data=data)

#     # Print the first 500 characters of the response
#     # print(response.text[:500])    

#     if not os.path.exists(result_file_path):
#         # If the file doesn't exist, create it
#         os.makedirs(os.path.dirname(result_file_path), exist_ok=True)


#     # You can also save the response to a file for further analysis
#     with open(result_file_path, 'w') as file:
#         file.write(response.text)




# def showresult(request, myid):

#     # Retrieve the SecurityFinding object based on myid
#     finding = get_object_or_404(SecurityFinding, id=myid)

#     # Pass the finding object to the template
#     # context = {'finding': finding}

#     result_file_path =  finding.result_file_path
#     with open(result_file_path) as f:
#         data = json.load(f)

#     projectName = finding.file_name


#     # vulPer = len(data["results"])
#     results_list = data.get("results", [])
#     length_of_results_list = len(results_list)
#     print("Length of the 'results' list:", length_of_results_list)

#     scanned_list = data.get("paths", {}).get("scanned", [])
#     length_of_scanned_list = len(scanned_list)
#     print("Length of the 'scanned' list:", length_of_scanned_list)

#     # Assuming you have already calculated the lengths as mentioned earlier
#     vulPercentage = ((length_of_scanned_list  - length_of_results_list) / length_of_scanned_list) * 100

#     vulPercentage = round(vulPercentage, 2)

#     impact_categories = {'MEDIUM': [], 'LOW': [], 'HIGH': []}


#     for result in results_list:
#         impact = result['extra']['metadata']['impact']
#         if impact in impact_categories:
#             impact_categories[impact].append(result)

#     # # Printing items in each impact category
#     # for impact, items in impact_categories.items():
#     #     print(f'Category: {impact}')
#     #     for item in items:
#     #         print(f'Check ID: {item["check_id"]}')
#     #         print(f'Message: {item["extra"]["message"]}')
#     #         print()  # Empty line for separation

#     highVar = len(impact_categories['HIGH'])
#     lowVar = len(impact_categories['LOW'])
#     mediumVar = len(impact_categories['MEDIUM'])

#     total_items = highVar + lowVar + mediumVar

#     risk_percentage = (mediumVar / total_items) * 100

    

#     impact = {
#         'highVar' : highVar,
#         'lowVar' : lowVar,
#         'mediumVar' : mediumVar,
#         'risk_percentage' : round(risk_percentage,2),
#     }
    


#     return render("bandapp/showresult.html", results=data, projectName=projectName, vulPercentage=vulPercentage, impact=impact)

#     # return render(request, 'bandapp/dashboard.html', context)





# Register | Login | Logout Functions

def user_register(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        email    = request.POST['email']

        _api_key = generate_unique_api_key()

        
        # Check if the username is unique
        if not User.objects.filter(username=username).exists():
            dataandtime = timezone.now()

            # Create a new user
            user = User.objects.create_user(username=username, password=password, email=email)

            sensor_data = UserData(
                user_name=username,
                pub_date=dataandtime,
                api_key=_api_key
            )
            sensor_data.save()
            
            return redirect('user_login')  # Redirect to your login view
        else:
            error_message = 'Username already exists'
    else:
        error_message = None

    return render(request, 'inhome_app/register.html', {'error_message': error_message})

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')  # Redirect to your dashboard view
        else:
            error_message = 'Invalid username or password'
    else:
        error_message = None

    return render(request, 'inhome_app/login.html', {'error_message': error_message})

def user_logout(request):
    logout(request)
    return redirect('user_login')  # Redirect to your login view


def generate_api_key():
    key_length = 36  # Length of the API key
    dash_positions = [8, 13, 18, 23]  # Positions of dashes in the API key

    characters = "abcdefghijklmnopqrstwxyz0123456789"

    api_key = ''.join(random.choice(characters) if i not in dash_positions else '-' for i in range(key_length))
    return api_key

def generate_unique_api_key():
    while True:
        # api_key = str(uuid.uuid4())
        api_key = str(generate_api_key())
        if not UserData.objects.filter(api_key=api_key).exists():
            return api_key






# Example usage
# api_key = generate_api_key()
# print(api_key)

# def generate_api_key():
#     key_length = 36  # Length of the API key
#     dash_positions = [8, 13, 18, 23]  # Positions of dashes in the API key

#     characters = "abcdefghijklmnopqrstwxyz0123456789"

#     api_key = ''.join(random.choice(characters) if i not in dash_positions else '-' for i in range(key_length))
#     return api_key

# def generate_unique_api_key():
#     while True:
#         # api_key = str(uuid.uuid4())
#         api_key = str(generate_api_key())
#         if not Nodedata.objects.filter(api_key=api_key).exists():
#             return api_key


# def index(request):
#     products = Product.objects.all()

#     all_prods = []
#     catProds = Product.objects.values('category', 'Product_id')
#     cats = {item['category'] for item in catProds}
#     for cat in cats:
#         prod = Product.objects.filter(category=cat)
#         n = len(products)
#         all_prods.append([prod, n]) 

#     params = {
#         'catproducts' : all_prods,
#         'allproducts' : products,
#               }

#     return render(request,'tze/index.html', params)


# def business(request):
#     # return HttpResponse('Teamzeffort    |      business Page')
#     return render(request,'tze/business.html')

# def about(request):
#     return render(request,'tze/about.html')

# def contact(request):
#     coreMem = Contact.objects.filter(mem_tag="core")
#     teamMem = Contact.objects.filter(mem_tag="team")
#     # print(f"coreMem: {coreMem} \n teamMem: {teamMem}")

#     return render(request, 'tze/contact.html', {'core':coreMem,'team':teamMem })

# def productView(request, myslug):
#     # Fetch the product using the id
#     product = Product.objects.filter(slug=myslug)
#     prodCat = product[0].category
#     # print(prodCat)
#     recproduct = Product.objects.filter(category=prodCat)
#     # print(recproduct)

#     # randomObjects = random.sample(recproduct, 2)
#     randomObjects = random.sample(list(recproduct), 2)


#     return render(request, 'tze/prodView.html', {'product':product[0],'recprod':randomObjects })


# # def index(request):
# #     return HttpResponse('Teamzeffort    |      index Page')
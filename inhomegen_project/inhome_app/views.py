#  i have created this file - GTA
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import UserData, ImgDetails
import random
import os
import requests
import json


from django.utils import timezone


from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout, logout

from django.contrib.auth.decorators import login_required

from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt


from django.conf import settings
from django.core.files.storage import FileSystemStorage

# media_full_path = settings.MEDIA_ROOT + "\playapp_data"
# upload_file_full_path = settings.STATIC_MEDIA_ROOT + "\\static\\bandapp\\uploaded_files"
# results_full_path = settings.STATIC_MEDIA_ROOT + "\\static\\bandapp\\ResultsFiles"

# bandapp\static\bandapp\uploaded_files
# C:\\Users\\Atharva Pawar\\Documents\\GitHub\\SECUIRX-v2\\securix_v2_project\\bandapp\\static\\playapp\\ResultsFiles\\codeGoat.py


# media_full_path = settings.MEDIA_ROOT + "\playapp_data"
media_full_path = settings.STATIC_MEDIA_ROOT + "\\static\\inhome_app\\generatedimg"


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
    # return HttpResponse('Securix V2    |      index Page')

    # Get the logged-in user's username
    logedIn_user = request.user.username
    
    # Query the database to get all records for the logged-in user
    # userData = ProjectDetails.objects.filter(user_name=logedIn_user)
    userData = "ProjectDetails.objects.filter(user_name=logedIn_user)"





    # Pass the data to the template
    context = {'userSensorData': userData, 'viewJson': "jsonKeys"}
    
    # Render the template with the data
    return render(request, 'inhome_app/index.html', context)
    # return render(request, 'inhome_app/index.html', context)





@login_required
def generate(request):
    if request.method == 'POST':
        # Get the values from the form
        proj_name = request.POST.get('proj_name')
        selected_room = request.POST.get('selectedroom')
        selected_model = request.POST.get('selectedmodel')  # Assuming this is intentional

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

        style = 'minimal design'

        # Get the last ImgDetails object
        last_img_details = ImgDetails.objects.last()

        # Calculate the next ID
        next_id = last_img_details.id + 1 if last_img_details else 1

        # Add further processing logic here, if needed
        path = generate_img_reqapi(prompt, img_id=next_id)
        # path = testpath(text="hello world", img_id=12)
        
        # Create a new node
        # ImgDetails.objects.create(user_name=logedIn_user, projName=proj_name, roomName=selected_room, prompt=prompt, negprompt=negative_prompt, style=style, path=path,  pub_date=pub_date, pub_time=pub_time)

        # Redirect to a success page or another view
        return redirect('dashboard')  # Change 'node_list' to the actual URL name for the node list view

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

def generate_img_reqapi(prompt, img_id):


    # api_url = "http://127.0.0.1:5000/generate_image"  # Update with your ngrok URL if needed

    # server_url = "https://0f2f-34-80-203-200.ngrok-free.app/"
    server_url = "https://1a45-34-125-152-171.ngrok-free.app/"
    api_url = f"{server_url}generate_image"  # Update with your ngrok URL if needed

    # Example payload for retro style
    payload_retro = {
        # "input_prompt": "minimalistic living room",
        # "input_prompt": "Generate an image of an old-style bedroom with a luxurious king-size bed, adorned with classic furniture, bathed in warm lighting, and featuring a charming French window overlooking serene scenery, gray pallet minimalistic: tv, sofa, table ",
        "input_prompt": prompt,
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
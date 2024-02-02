from ultralytics import YOLO

from IPython.display import display, Image
import sys
import subprocess
import re

# Open a file for writing
path=r"C:\Users\Shaun\Downloads\current_new.jpeg.jpg"
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
            temp=str(obj[1:])
            objects[temp]=obj[0]
else:
    print("No objects detected.")
    objects["Objects"]="None"
print(str(objects).replace('\'','"'))
@echo off
start cmd /k "cd C:\Users\Shaun\Desktop\Stable Diffusion\stable-diffusion-webui\scripts && echo "Hello" && python img2img.py --prompt "Add a nice carpet" --init-img "C:\Users\Shaun\Downloads\current_new.jpeg.jpg" --strength 0.57 "
pause > nul
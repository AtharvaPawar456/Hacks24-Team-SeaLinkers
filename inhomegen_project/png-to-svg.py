#!/usr/bin/env python
# coding: utf-8

# In[6]:


# get_ipython().system('pip install vtracer')


# In[11]:


import vtracer


inp= "D:\Manu\Engineering\College\Hackathon\Indoor-Object-Detection\kitchen.png"
out = "test1.svg"

def img2svg(inpath, outpath):
    # Minimal example: use all default values, generate a multicolor SVG
    vtracer.convert_image_to_svg_py(inp, out)

    # Single-color example. Good for line art, and much faster than full color:
    vtracer.convert_image_to_svg_py(inp, out, colormode='binary')

    # All the bells & whistles
    vtracer.convert_image_to_svg_py(inp,
                                    out,
                                    colormode = 'color',        # ["color"] or "binary"
                                    hierarchical = 'stacked',   # ["stacked"] or "cutout"
                                    mode = 'spline',            # ["spline"] "polygon", or "none"
                                    filter_speckle = 4,         # default: 4
                                    color_precision = 6,        # default: 6
                                    layer_difference = 16,      # default: 16
                                    corner_threshold = 60,      # default: 60
                                    length_threshold = 4.0,     # in [3.5, 10] default: 4.0
                                    max_iterations = 10,        # default: 10
                                    splice_threshold = 45,      # default: 45
                                    path_precision = 3          # default: 8
                                    )


inp= "kitchen.png"
out = "test1.svg"
img2svg(inp, out)
# In[ ]:




'''
# USP:
- Image Generation and from generated image modify specific object
- 1024x1024 Resolution Interior Design
- from Interior Design detect the objects likes chair, table, etc
- recommend the product based on detected objects from Generated Interior Design
- Voice Input Prompt
- View full Image
- can buy the recommended product
- can save the svg file of the Generated Interior Design


'''
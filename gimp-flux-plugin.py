#!/usr/bin/python

# Import necessary libraries/modules
import urllib2  # For making HTTP requests
import tempfile  # For working with temporary files
import os  # For file operations
import json  # For working with JSON data
import ssl  # For SSL certificate handling
from gimpfu import *  # Import necessary functions and classes from the gimpfu module
import time

VERSION = 135
INIT_FILE = "init.jpeg"
GENERATED_FILE = "gen_0_GIMP.jpeg"

# Define file paths for initialization and generated images
initFile = os.path.join(tempfile.gettempdir(), INIT_FILE)
generatedFile = os.path.join(tempfile.gettempdir(), GENERATED_FILE)

# Ignore SSL certificate verification
ssl._create_default_https_context = ssl._create_unverified_context

def load_api_key():
    # Default API key value
    default_api_key = "0000000000"

    # Get the current working directory
    #current_dir = os.getcwd()
    current_dir = os.path.dirname(os.path.abspath(__file__))
    print("Current directory:", current_dir)  # Debugging line to show current working directory

    # Construct the full path to the fluxapi.key file
    key_file_path = os.path.join(current_dir, 'fluxapi.key')
    print("Key file path:", key_file_path)  # Debugging line to show key file path

    try:
        # Try to open and read the API key from the file
        with open(key_file_path) as file:
            api_key = file.read().strip()  # Strip to remove any leading/trailing whitespace
        # Use the default key if the file is empty or contains only whitespace
        return api_key or default_api_key  # Return the default if the API key is empty
    except IOError as e:  # Use IOError for file-related errors in Python 2
        # Print the error message for debugging
        print("Error reading key file:", e)
        # If the file does not exist, use the default API key
        return default_api_key


# Function to display generated images
def displayGenerated(image_data):
    # Get the current foreground color
    color = pdb.gimp_context_get_foreground()
    # Set foreground color to black
    pdb.gimp_context_set_foreground((0, 0, 0))

    try:
        # Assuming image_data is raw bytes
        if isinstance(image_data, str):  # Use 'str' for byte strings in Python 2
            # Write the raw bytes to the generated file
            with open(generatedFile, "wb") as imageFile:
                imageFile.write(image_data)
                imageFile.close()

            # Load and display the image in GIMP
            #imageLoaded = pdb.file_webp_load(generatedFile, generatedFile)  # Adjust if necessary for your image format
             # Load the image based on its content type
            
            imageLoaded = pdb.file_jpeg_load(generatedFile, generatedFile)
           
            pdb.gimp_display_new(imageLoaded)

            # Optionally, set the active layer if there are multiple layers
            if len(imageLoaded.layers) > 1:
                pdb.gimp_image_set_active_layer(imageLoaded, imageLoaded.layers[1])

        else:
            raise ValueError("Expected image data in bytes format")

    except Exception as e:
        print("Error processing image: {}".format(e))

    # Restore the original foreground color
    pdb.gimp_context_set_foreground(color)

# The main plugin function
def flux_plugin(image, drawable,promptStrength, steps, seed, prompt):
    API_URL = "https://api-inference.huggingface.co/models/black-forest-labs/FLUX.1-dev"

    stepss = [
        "Analyzing the prompt...",
        "Preprocessing input...",
        "Generating image...",
        "Applying enhancements...",
        "Finalizing output..."
    ]
    
    total_steps = len(stepss)

    pdb.gimp_progress_init("FLUX.1 [dev]", None)

    for i, step in enumerate(stepss):
        # Update progress message for each step
        pdb.gimp_progress_set_text(step)
        
        # Simulate the time each step takes (e.g., replace with actual processing)
        time.sleep(2)
        
        # Update the progress bar based on how many steps are completed
        pdb.gimp_progress_update(float(i + 1) / total_steps)

    try:
        params = {
            
            "guidance_scale": promptStrength,
            "num_inference_steps": int(steps),
            "seed": int(seed),
            #"negative_prompt": negativeprompt,
            
            
        }
        # Create the payload
        payload = {
            "inputs": prompt,
            "parameters" : params,

        }
        
        # Serialize the payload to JSON
        data = json.dumps(payload)
        
        # Create the headers
        headers = {
            "Content-Type": "application/json",  # Set the content type to JSON
            "Authorization": "Bearer {}".format(load_api_key())  # Your authorization token
        }

        print(headers)  # Add this line to debug
        #pdb.message(f"headers: {headers}")
        #pdb.gimp_message(f"headers: {headers}")

        
        # Create the request with the correct parameters
        request = urllib2.Request(url=API_URL, data=data, headers=headers)
        pdb.gimp_progress_set_text("Waiting for API response...")
        response = urllib2.urlopen(request)
        data = response.read()
        pdb.gimp_progress_set_text("Processing response...")
    
        displayGenerated(data)

    except urllib2.HTTPError as ex:
        try:
            data = ex.read()
            data = json.loads(data)

            message = data.get("message", str(ex))
        except Exception:
            message = str(ex)

        raise Exception(message)
    finally:
        # End GIMP progress
        pdb.gimp_progress_end()

    return

# Register the plugin with GIMP
register(
    "flux_plugin",
    "Generate image using FLUX model",
    "Generates an image using the specified prompt with the FLUX model.",
    "Your Name",
    "Alen Tito",
    "2024",
    "<Image>/AI/Flux",
    "*",
    [
        (PF_SLIDER, "promptStrength", "Prompt Strength", 8, (0, 20, 1)),
        (PF_SLIDER, "steps", "Steps", 25, (10, 150, 1)),
        (PF_STRING, "seed", "Seed", ""),
        (PF_TEXT, "prompt", "Prompt", ""),
    ],
    [],
    flux_plugin,
)

main()


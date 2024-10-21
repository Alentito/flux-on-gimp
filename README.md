# GIMP FLUX Plugin

This repository includes a GIMP plugin for communication with the locally installed **FLUX 1 [dev]** inference API, allowing AI-generated images from the Hugging Face model. The plugin is compatible with Linux, macOS, and Windows 11 (WSL2). Check the "Limitations" section to understand the plugin's restrictions.

## Installation

### Download Files
1. Download the repository files by clicking on "Code" and selecting "Download ZIP."
2. Extract the ZIP, and locate the file `gimp-flux-plugin.py` in the `local` subfolder. This is the main GIMP plugin code.
3. You do not need the other files in the ZIP.

### GIMP Setup
This plugin has been tested on GIMP 2.10 and should work with all 2.* versions, excluding 2.99 (which is based on Python 3).

1. Start GIMP, go to `Edit > Preferences`, scroll down to `Folders`, and expand the section. Click on `Plug-ins`.
2. Copy the path from the folder that includes your username.
3. Open your file explorer, navigate to the folder, and paste the `gimp-flux-plugin.py` file into it.
4. If you're using macOS or Linux, open a terminal and run:
    ```bash
    chmod 755 gimp-flux-plugin.py
5. Restart GIMP. You should see a new menu named "AI". If the menu doesn't appear, check the **Troubleshooting** section.

## FLUX Inference API

### Prerequisites:
- You will need an account on [huggingface.co](https://huggingface.co) to download the model.
- If you are running Windows 11, prepare WSL2 beforehand.

### Steps:
1. Create an account on Hugging Face.
2. Navigate to `Settings > Access Tokens`.
3. Click on "New Token," name it, select "Read" as the role, and generate the token.
4. Copy the token to use it in the plugin.

### Generate Images
- Open an image in GIMP.
- Navigate to `AI > FLUX` and start generating images based on the input prompt.

## Troubleshooting

### AI Menu Not Shown

#### Linux:
If you encounter the error:

    
    gimp: LibGimpBase-WARNING: gimp: gimp_wire_read(): error

This indicates that your GIMP installation may not include Python support. Verify by checking if `Filters > Python-Fu > Console` is available. If missing, reinstall GIMP from Flathub:

[Install GIMP from Flathub](https://flathub.org/apps/details/org.gimp.GIMP).

### macOS:
Ensure the plugin file permissions are set to 755. You might need to set these permissions via the terminal:

    
    chmod ugo+x *py

### macOS/Linux:
Run the plugin manually from the terminal to check for errors:

    
    python <path-to-plugin-folder>/gimp-flux-plugin.py

If you see an error related to "gimpfu" being unknown, ensure you are using Python 2 (required by GIMP). If other errors appear, try reinstalling GIMP.




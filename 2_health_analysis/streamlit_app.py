import os
import sys

# Resolve circular/shadow import by pointing python to the streamlit_app subfolder
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(current_dir, "streamlit_app"))

# Import all layout and logic from the app.py inside the folder
from app import *  # type: ignore # pyright: ignore[reportMissingImports]
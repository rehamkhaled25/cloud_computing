import os
from PIL import Image, ImageTk

def get_image(path, size):
    """Loads image from path, or returns None if file is missing."""
    try:
        if os.path.exists(path):
            img = Image.open(path)
            img = img.resize(size, Image.Resampling.LANCZOS)
            return ImageTk.PhotoImage(img)
    except Exception as e:
        print(f"Error loading {path}: {e}")
    return None
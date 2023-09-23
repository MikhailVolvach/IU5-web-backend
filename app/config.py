import os
from pathlib import Path


static_path = Path(os.path.dirname(os.path.abspath(__file__)), "static") # Путь до статических файлов
data_path = Path(static_path, "data") 
img_path = Path(static_path, "img")
icons_path = Path(static_path, "icons")

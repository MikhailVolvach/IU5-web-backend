import os
from pathlib import Path


media_path = Path(os.path.dirname(os.path.abspath(__file__)), "media") # Путь до медиа файлов
data_path = Path(media_path, "data") 
img_path = Path(media_path, "img")
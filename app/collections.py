from app.config import data_path, Path, img_path
from app.models.data_item import DataItem


data_collection = [
    DataItem("img/Heart_of_a_dog.jpg", "Булгаков М. А. Собачье сердце", Path(data_path, "Heart_of_a_dog.txt"), True, False),
    DataItem("img/Directory.png", "Директория KTS", Path(data_path, "KTS"), False, True),
    DataItem("img/Code.png", "Задача Tinkoff Start", Path(data_path, "Tinkoff_task.txt"), True, False),
]


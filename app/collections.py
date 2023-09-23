from app.config import data_path, Path
from app.models.data_item import DataItem


data_collection = [
    DataItem("img/Heart_of_a_dog.jpg", "Булгаков М. А. Собачье сердце", Path(data_path, "Heart_of_a_dog.txt")),
]


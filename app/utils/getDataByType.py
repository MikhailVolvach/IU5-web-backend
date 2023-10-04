from app.config import media_path, Path

def getDataByType(DataItem, id):
    item = DataItem.objects.filter(id=id)[0]
    
    data = None
    
    if DataItem.DataType.IMAGE == item.data_type:
        data = item.file.url
    else:
        # Код для получения текста из файла
        with open(Path(media_path, item.file.name), 'r') as f:
            data = f.read(1000)
            
    return data
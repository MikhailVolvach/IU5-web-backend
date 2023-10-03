from pathlib import Path

def getDataByType(DataItem, id):
    item = DataItem.objects.filter(id=id)[0]
    # data = {
    #     "img": Data.img,
    #     "title": Data.title,
    #     "file": Data.file,
    #     "encription_status": Data.encription_status,
    #     "status": Data.status,
    #     "data_type": Data.data_type,
    #     "data_encription_request": Data.data_encription_request,
    #     "data_content": ""
    # }
    data = None
    if DataItem.DataType.CODE == item.DataType:
        # Код для получения кода из файла
        pass
    elif DataItem.DataType.IMAGE == item.DataType:
        # Код для получения изображения из файла
        pass
    else:
        # Код для получения текста из файла
        pass
    
    return {item, data}
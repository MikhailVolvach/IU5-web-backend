from django.shortcuts import render
from app.collections import data_collection
from app.templatetags import getType

def getDataList(request):
    query = request.GET.get('data_search')
    
    if query:
        filtered_data = [data_item for data_item in data_collection if
            query.lower() in data_item.title.lower() or query.lower() in str(data_item.data).lower()] 
    else:
        filtered_data = data_collection
        query = ""

    return render(request, 'data_list.html', {'data': {
        'data_list':filtered_data, 
        'data_search': query
    }})
    
def getDataItem(request, id):
    return render(request, 'data_item.html', {
        'data': {
            'id': id,
            'data_item': data_collection[id],
        }
    })

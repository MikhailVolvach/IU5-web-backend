from django.shortcuts import render
from app.models.DataItem_model import DataItem
from app.utils.getDataByType import getDataByType

def getDataList(request):
    query = request.GET.get('data_search')
    
    if not query: query = ""
    
    return render(request, 'data_list.html', {'data': {
        'data_list': DataItem.objects.filter(title__icontains=query),
        'data_search': query
    }})
    
def getDataItem(request, id):
    # print(getDataByType(DataItem.objects.filter(id=id)[0]))
    getDataByType(DataItem, id)
    return render(request, 'data_item.html', {
        'data': {
            'id': id,
            'data_item': DataItem.objects.filter(id=id)[0]
        }
    })

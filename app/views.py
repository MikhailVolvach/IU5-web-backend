from django.shortcuts import render, redirect
from app.models.DataItem_model import DataItem
from app.utils.getDataByType import getDataByType

import psycopg2

def getDataList(request):
    query = request.GET.get('data_search')
    
    if not query: query = ""
    
    return render(request, 'data_list.html', {'data': {
        'data_list': DataItem.objects.filter(is_deleted=False).filter(title__icontains=query).order_by('id'),
        'data_search': query
    }})
    
def getDataItem(request, id):
    print(getDataByType(DataItem, id))
    return render(request, 'data_item.html', {
        'data': {
            'id': id,
            'data_item': DataItem.objects.filter(id=id)[0],
            'information': getDataByType(DataItem, id)
        }
    })

def deleteDataItem(request, id):
    conn = psycopg2.connect(dbname="iu5_web_db", host='localhost', user='iu5_web', password='1703', port=5432)
    cursor = conn.cursor()
    cursor.execute(f"UPDATE app_dataitem SET is_deleted='true' WHERE id={id}")
    conn.commit()
    cursor.close()
    conn.close()
    
    return redirect('getDataList')

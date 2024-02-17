from django.shortcuts import render, redirect
from app.models.DataItem_model import DataItem
from app.models.DataEncriptionRequest_model import DataEncriptionRequest
from app.utils.getDataByType import getDataByType

import psycopg2


def getDataList(request):
    query = request.GET.get('data_search')

    if not query: query = ""

    # print(DataItem.objects.filter(is_deleted=False).filter(title__icontains=query).order_by('id'))

    # DataItem.objects.filter(is_deleted=False).filter(title__icontains=query).order_by('id')

    items = DataItem.objects.filter(is_deleted=False).filter(title__icontains=query).order_by('id')
    request_list = DataEncriptionRequest.objects.filter(work_status=DataEncriptionRequest.Status.INTRODUCED)[0]
    # print("request=",request.id)
    if request:
        request_id = request_list.id

    else:
        request_id = None

    print(request_id)
    for item in items:
        item.img_url = item.img.url.replace("nginx", "localhost")

    return render(request, 'data_list.html', {'data': {
        'request_id': request_id,
        'data_list': items,
        'data_search': query
    }})


def getRequestPage(request, id):
    request_item = DataEncriptionRequest.objects.filter(id=id)[0]
    items = DataItem.objects.filter(is_deleted=False).filter().order_by('id')
    for item in items:
        item.img_url = item.img.url.replace("nginx", "localhost")

    return render(request, 'draft.html', {'data': {
        'data_list': items,
        'request': request_item
    }})


def getDataItem(request, id):
    print(getDataByType(DataItem, id))
    return render(request, 'data_item.html', {
        'data': {
            'id': id,
            'data_item': DataItem.objects.filter(id=id)[0],
            'imgUrl': DataItem.objects.filter(id=id)[0].img.url.replace("nginx", "localhost"),
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

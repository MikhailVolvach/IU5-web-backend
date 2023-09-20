from django.shortcuts import render
from app.collections import services_collection, requests_collection

def getServices(request):
    query = request.GET.get('services_search')
    
    if query:
        filtered_data = [service for service in services_collection if
            query.lower() in service.title.lower() or query.lower() in str(service.cost).lower()] 
    else:
        filtered_data = services_collection
        query = ""

    return render(request, "services.html", {'data': {
        'services_list':filtered_data, 
        'search_value': query
    }})
    
def getService(request, id):
    return render(request, 'service.html', {'data': {
        'id': id,
        'service': services_collection[id]
    }})

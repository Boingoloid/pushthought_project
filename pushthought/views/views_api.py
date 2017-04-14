# from django.http import  HttpResponse
# from ..models import Program
# import json
#
# from django.conf import settings
#
# def api(request):
#     obj = Program.objects.all()
#     newObject = json.dumps(obj)
#     return HttpResponse(newObject, content_type='application/json')
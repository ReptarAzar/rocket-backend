from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import simplejson

@csrf_exempt
def home(request):
    if request.method == 'POST':
        print "POST!"
        return HttpResponse("OK\r\n")
    else:
        print "NOT POST!"
        return HttpResponse("ERR")

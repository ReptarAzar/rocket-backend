from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import simplejson

@csrf_exempt
def home(request):
    if request.method == 'POST':
        print request.POST['checkin']
        try:
            checkin = simplejson.loads(request.POST['checkin'])
            print checkin['user']['firstName']
            print "4sq name captured!"
            return HttpResponse("OK\r\n")
        except:
            print "Name didn't work :-/"
            return HttpResponse("NOT OK\r\n")
    else:
        print "NOT POST!"
        return HttpResponse("ERR")
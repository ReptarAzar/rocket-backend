import datetime
from django.http import HttpResponse, HttpResponseServerError
from django.views.decorators.csrf import csrf_exempt
from models import FoursquareUser, Venue, Checkin
import simplejson, pycurl

@csrf_exempt
def home(request):
    if request.method == 'POST':
        try:
            # capture JSON data, convert to dictionary
            jsonData = simplejson.loads(request.POST['checkin'])

            # check to see if the user already exists
            try:
                user = FoursquareUser.objects.get(userId = jsonData['user']['id'])

            # if not, then create him!
            except Exception:

                # we have to check since since the twitter field isn't always there
                try:
                    twttr = jsonData['user']['contact']['twitter'],
                except:
                    twttr = None,

                # make the user model
                user = FoursquareUser(
                    userId = jsonData['user']['id'],
                    firstName = jsonData['user']['firstName'],
                    lastName = jsonData['user']['lastName'],
                    photo = jsonData['user']['photo'],
                    gender = jsonData['user']['gender'],
                    homeCity = jsonData['user']['homeCity'],
                    bio = jsonData['user']['bio'],
                    twitter = twttr
                )

                # save dat ish
                user.save()

            # check to see if the venue exists
            try:
                venue = Venue.objects.get(venueId = jsonData['venue']['id'])

            # if not, then create it!
            except Exception:

                # see if the contact stuff exists
                try:
                    phn = jsonData['venue']['contact']['phone']
                except:
                    phn = None
                try:
                    twttr = jsonData['venue']['contact']['twitter']
                except:
                    twttr = None

                # make the venue model
                venue = Venue(
                    venueId = jsonData['venue']['id'],
                    name = jsonData['venue']['name'],
                    phone = phn,
                    twitter = twttr,
                    address = jsonData['venue']['location']['address'],
                    lat = jsonData['venue']['location']['lat'],
                    lng = jsonData['venue']['location']['lng'],
                    postalCode = jsonData['venue']['location']['postalCode'],
                    city = jsonData['venue']['location']['postalCode'],
                    state = jsonData['venue']['location']['state'],
                    country = jsonData['venue']['location']['country'],
                    categoryId = jsonData['venue']['categories'][0]['id'],
                    categoryName = jsonData['venue']['categories'][0]['name'],
                    categoryPluralName = jsonData['venue']['categories'][0]['pluralName'],
                    categoryShortName = jsonData['venue']['categories'][0]['shortName'],
                    categoryIcon = jsonData['venue']['categories'][0]['icon'],
                    categoryPrimary = jsonData['venue']['categories'][0]['primary'],
                    statsCheckinsCount = jsonData['venue']['stats']['checkinsCount'],
                    statsUsersCount = jsonData['venue']['stats']['usersCount'],
                    statsTipsCount = jsonData['venue']['stats']['tipCount'],
                    statsLikesCount = jsonData['venue']['likes']['count'],
                    url = jsonData['venue']['url']
                )

                # save dat ish
                venue.save()

            checkin = Checkin(
                checkinId = jsonData['id'],
                createdAt = datetime.datetime.fromtimestamp(jsonData['createdAt']),
                timezone = jsonData['timeZone'],
                user = user,
                venue = venue
            )
            checkin.save()

            # ping the netduino!
            c = pycurl.Curl()
            c.setopt(c.URL, "http://69.193.126.141:8080")
            c.perform()
            return HttpResponse("OK\r\n")
        except Exception as steve:
            return HttpResponseServerError("ERROR" + " " + steve.message + "\r\n")
    else:
        print "NOT POST!"
        return HttpResponseServerError("ERROR NOT POST")

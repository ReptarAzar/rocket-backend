from django.contrib import admin
from api.models import FoursquareUser, Venue, Checkin

admin.site.register(FoursquareUser)
admin.site.register(Venue)
admin.site.register(Checkin)
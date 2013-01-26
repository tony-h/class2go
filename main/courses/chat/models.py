# From https://github.com/peterbe/django-sockjs-tornado

from datetime import datetime
from django.db import models

#For timzone support
#from django.utils.timezone import utc
#from pytz import timezone
#from settings import TIME_ZONE

def now():
    #If using timezone info such as one of the following lines, an error is generated:
    #  MySQL backend does not support timezone-aware datetimes when USE_TZ is False
    #print "DATETIME-UTC", datetime.utcnow().replace(tzinfo=utc)
    #print "DATETIME-TZ", datetime.now(timezone(TIME_ZONE))
    return datetime.now()


class Message(models.Model):
    name = models.CharField(max_length=200)
    message = models.TextField()
    date = models.DateTimeField(default=now)

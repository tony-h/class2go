# From https://github.com/peterbe/django-sockjs-tornado

import json
from sockjs.tornado import SockJSConnection
from .models import Message


class ChatConnection(SockJSConnection):
    _connected = set()

    def on_open(self, request):
        #print "OPEN"
        #print request.get_cookie('name')
        self._connected.add(self)
        #for each in Message.objects.all().order_by('date')[:10]:

        #TODO: Limit the number of messages to a particular count
        # or to a particular time (24 hours, or whatever)
        # Can't use order_by('date')[:10]: since that returns the first 10,
        # and not the last 10. Perhaps use .reverse() and then use [:100]
        
        #num_of_messages = Message.objects.count()
        #print num_of_messages
        
        for each in Message.objects.all().order_by('date'):
            self.send(self._package_message(each))
            #print self._package_message(each)

    def on_message(self, data):
        data = json.loads(data)
        #print "DATA", repr(data)
        
        #TODO: Create a use a specific table for each course
        #course_prefix = data['course_prefix'],
        #course_suffix = data['course_suffix'],        
        
        msg = Message.objects.create(
            name = data['name'],
            message = data['message']
        )
        self.broadcast(self._connected, self._package_message(msg))
        #print self._package_message(msg)

    def on_close(self):
        #print "CLOSE"
        self._connected.remove(self)

    def _package_message(self, m):
        return {'date': m.date.strftime('%H:%M:%S'),
                'message': m.message,
                'name': m.name}

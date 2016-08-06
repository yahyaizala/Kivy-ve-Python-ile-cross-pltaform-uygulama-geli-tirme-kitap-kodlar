from os.path import dirname,join,realpath
from plyer import notification
from plyer.utils import platform
from plyer.compat import PY2

class NotificationDemo(object):
    def __init__(self,title,message):
        self.title=title
        self.message=message

    def do_notify(self, mode='normal'):
        if PY2:
            self.title = self.title.decode('utf8')
            self.message = self.message.decode('utf8')

        kwargs = {'title': self.title, 'message': self.message}
        if mode == 'fancy':
            kwargs['app_name'] = "Doviz App"
            if platform == "win":
                kwargs['app_icon'] = join(dirname(realpath(__file__)),
                                          'notfy.ico')
                kwargs['timeout'] = 4
            else:
                kwargs['app_icon'] = join(dirname(realpath(__file__)),
                                          'notfy.png')
        notification.notify(**kwargs)
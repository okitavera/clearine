import subprocess
from gi.repository import Gdk

class Helper():
    def xrdb(self, request):
        result = {}
        query = subprocess.Popen(['xrdb', '-query'],stdout=subprocess.PIPE)
        for line in iter(query.stdout.readline, b''):
            lined = line.decode()
            key, value, *_ = lined.split(':')
            key = key.lstrip('*').lstrip('.')
            value = value.strip()
            result[key] = value

        return result[request]
    def to_rgba(self, hex):
        # convert hex color to RGBA
        color = Gdk.RGBA()
        color.parse(hex)
        return color

class SignalHandler():
    def __init__(self):
        self.SIGINT = False

    def SIGINT(self, signal, fram):
        self.SIGINT = True

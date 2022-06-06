from django.core.files.storage import FileSystemStorage
from django.conf import settings
from .authentication import *

class OverwiteStorageSystem(FileSystemStorage):
    
    def get_available_name(self, name, max_length=None):
        # if the file name already exists, remove it as if it was a true file system
        if self.exists(name):
            self.delete(name)
        return super().get_available_name(name, max_length)


def range_with_floats(start, stop, step=1):
    while stop > start:
        yield start
        start += step

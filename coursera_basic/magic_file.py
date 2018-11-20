"""
Файл с магическими методами
"""
import os
import os.path 
import tempfile

import tempfile

class File:
    def __init__(self, file_name):
        self.file_name = os.path.normpath(file_name)
        self.current_line = 0

    def __str__(self):
        return self.file_name

    def __add__(self, value):
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as fp:

            with open(self.file_name) as a:
                fp.write(a.read())

            with open(value.file_name) as b:
                fp.write(b.read())

            return File(fp.name)

    def __iter__(self):
        return self

    def __next__(self):
        try:
            with open(self.file_name, "r") as f:
                result = f.readlines()[self.current_line].rstrip()
                self.current_line += 1
        except:
            raise StopIteration

        return result

    def write(self, str_data):
        try:
            with open(self.file_name, "a") as f:
                f.write(str_data)
        except IOError:
            print("IO Error")
        except OSError:
            print("OS Error")
            
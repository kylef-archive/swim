import re


class Package(object):
    @classmethod
    def open(cls):
        with open('Package.swift') as fp:
            content = fp.read()

            match = re.search(r'name\s*:\s*["](.*)["]', content)
            if match:
                name = match.groups()[0]
                return cls(name=name)

    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name

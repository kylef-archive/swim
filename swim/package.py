import os
import tempfile
import json
from subprocess import Popen, PIPE


class Package(object):
    @classmethod
    def open(cls):
        with open('Package.swift') as fp:
            package_source = fp.read().replace('import PackageDescription', '')

        file_dirname = os.path.dirname(os.path.abspath(__file__))
        description = os.path.join(file_dirname, 'PackageDescription.swift')

        with open(description) as fp:
            contents = fp.read().replace('// package', package_source)

        with tempfile.NamedTemporaryFile() as fp:
            fp.write(contents)
            fp.flush()

            process = Popen(['swift', fp.name], stdout=PIPE, stderr=PIPE)
            output, err = process.communicate()
            if process.returncode != 0:
                raise Exception('Problem Building Package: {}'.format(err))

            package = json.loads(output)

        return cls(name=package['name'])

    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name

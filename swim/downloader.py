import os
import hashlib
import subprocess


def path_for_dependency(dependency):
    path = hashlib.sha1(dependency.url).hexdigest()
    return os.path.join('Packages', path)


def download_dependency(dependency):
    path = path_for_dependency(dependency)
    if not os.path.exists(path):
        subprocess.check_output(['git', 'clone', dependency.url, path])


def download_dependencies(dependencies):
    for dependency in dependencies:
        download_dependency(dependency)

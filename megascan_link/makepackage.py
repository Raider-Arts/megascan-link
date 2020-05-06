# ADOBE CONFIDENTIAL
#
# Copyright 2019 Adobe
# All Rights Reserved.
#
# NOTICE:  Adobe permits you to use, modify, and distribute this file in
# accordance with the terms of the Adobe license agreement accompanying it.
# If you have received this file from a source other than Adobe,
# then your use, modification, or distribution of it requires the prior
# written permission of Adobe.
#

import os
import sys
import fnmatch
import json
from zipfile import ZipFile


class IgnoreFileFilter(object):
    def __init__(self, filename):
        self.__globs = []
        self.__dirs_to_ignore = []

        if os.path.exists(filename):
            with open(filename, 'rt') as f:
                lines = f.readlines()

            for line in lines:
                line = line.strip()

                if line == '' or line.startswith('#'):
                    continue

                if line.endswith('/'):
                    self.__dirs_to_ignore.append(line[:-1])
                else:
                    self.__globs.append(line)

    def filter(self, filepath):
        # Ignore filter config files.
        if filepath.endswith('.sdpackageignore'):
            return False

        # Check that the file is not included in any glob.
        if self.__globs:
            filename = os.path.basename(filepath)

            for pattern in self.__globs:
                if fnmatch.fnmatch(filename, pattern):
                    return False

        # Check that the file is not inside any ignored directory.
        if self.__dirs_to_ignore:
            dirname = os.path.normpath(os.path.dirname(filepath))
            dirs = dirname.split(os.sep)

            for pattern in self.__dirs_to_ignore:
                for d in dirs:
                    if pattern == d:
                        return False

        return True


def read_metadata():
    if not os.path.exists('pluginInfo.json'):
        print("Missing metadata file")
        return None

    try:
        f = open('pluginInfo.json', 'rt')
        return json.load(f)
    except Exception as e:
        print('Error while checking metadata: %s' % e)
        f.close()
        return None

def check_metadata(metadata):
    if not 'name' in metadata:
        print('"name" metadata entry is missing')
        return False

    return True

def walk(directory):
    for dirpath, dirnames, filenames in os.walk(directory, topdown=True):
        for filename in filenames:
            yield os.path.join(dirpath, filename)

def add_file_to_package(zfile, plugin_name, filepath):
    print("Adding file %s to package" % filepath)
    archive_filepath = os.path.join(plugin_name, filepath)
    zfile.write(filepath, arcname=archive_filepath)

def main():
    this_dir = os.path.abspath(os.path.dirname(__file__))

    build_dir = os.path.join(this_dir, "build")

    if not os.path.exists(build_dir):
        try:
            os.makedirs(build_dir)
        except Exception as e:
            print('Could not create build directory')
            sys.exit(1)

    package_parent_dir = os.path.abspath(os.path.join(this_dir, '..'))
    package_dir_name = os.path.basename(this_dir)

    # Save the current dir and switch to the package dir.
    saved_dir = os.getcwd()
    os.chdir(this_dir)

    metadata = read_metadata()
    if not metadata:
        sys.exit(1)

    if not check_metadata(metadata):
        sys.exit(1)

    plugin_name = metadata['name']
    package_filepath = os.path.join(build_dir, plugin_name) + '.sdplugin'

    try:
        file_filter = IgnoreFileFilter('.sdpackageignore')

        with ZipFile(package_filepath, 'w') as zfile:
            for filepath in walk('.'):
                if os.path.abspath(filepath) == os.path.join(this_dir, 'pluginInfo.json'):
                    add_file_to_package(zfile, plugin_name, filepath)
                elif file_filter.filter(filepath):
                    add_file_to_package(zfile, plugin_name, filepath)

    except Exception as e:
        print("Error while packaging plugin: %s" % e)
        sys.exit(1)
    finally:
        # Restore the saved directory.
        os.chdir(saved_dir)

if __name__ == '__main__':
    main()

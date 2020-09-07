'''
This is a free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Net Failover Manager is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with This software.  If not, see <https://www.gnu.org/licenses/>.
'''

import os
import json
from collections import OrderedDict

from absl import app
from absl import flags
from absl import logging


flags.DEFINE_string('movies_folder', None,
                    'Folder in which the movies served by the HTTP server '
                    'are stored')

flags.DEFINE_string('url_prefix', None,
                    'Prefix for movies URLs, e.g.:'
                    'http://192.168.0.1/media/')

flags.DEFINE_string('output_menu_file', None, 'Path to the JSON menu file')

flags.mark_flag_as_required('movies_folder')
flags.mark_flag_as_required('url_prefix')
flags.mark_flag_as_required('output_menu_file')

flags.register_validator('movies_folder',
                         lambda value: os.path.isdir(value),
                         'the flag must specify a valid directory')

flags.register_validator('output_menu_file',
                         lambda value: os.path.exists(os.path.dirname(value)),
                         'the path is not valid')


FLAGS = flags.FLAGS

MENU_STRUCTURE = OrderedDict()


def printTree():
    for root, folders, files in os.walk(FLAGS.movies_folder):
        print('root: ' + root)
        for folder in folders:
            print('folder: ' + folder)
        for f in files:
            print('file:' + f)


def printMenuToJSON():
    print(json.dumps(MENU_STRUCTURE, indent=2))


FLAGS = flags.FLAGS

MENU_STRUCTURE = OrderedDict()


def printTree():
    for root, folders, files in os.walk(FLAGS.movies_folder):
        print('root: ' + root)
        for folder in folders:
            print('folder: ' + folder)
        for f in files:
            print('file:' + f)


def printMenuToJSON():
    if (os.path.exists(FLAGS.output_menu_file)):
        overwrite = input('The menu file ' + FLAGS.output_menu_file +
                          ' will be overwritten, ok? [y/N]')
        if overwrite != 'Y' and overwrite != 'y':
            exit(1)
    with open(FLAGS.output_menu_file, 'w') as menu_file:
        json.dump(MENU_STRUCTURE, menu_file, indent=2)


def initDictStruct():
    MENU_STRUCTURE['headline'] = 'Movies Collection'


def createMovieSubMenu(root, folder):
    menu_entry = {}
    menu_entry['icon'] = 'movie'
    menu_entry['label'] = folder
    menu_entry['data'] = {}

    menu_entry_data = menu_entry['data']
    menu_entry_data['type'] = 'pages'
    menu_entry_data['template'] = {}

    menu_entry_data_template = menu_entry_data['template']
    menu_entry_data_template['type'] = 'separate'
    menu_entry_data_template['layout'] = '0,0,4,3'
    menu_entry_data_template['color'] = 'msx-glass'

    menu_entry_data['items'] = createMoviesMenuEntries(root, folder)
    return menu_entry


def createMovieFoldersMenus(root):
    folders = [path for path in os.listdir(root) if os.path.isdir(
        os.path.join(root, path))]
    folders.sort()
    logging.info('Folders under ' + root + ': ')
    logging.info(folders)
    MENU_STRUCTURE['menu'] = [createMovieSubMenu(
        root, folder) for folder in folders]


def createMoviesMenuEntries(root, folder):
    files = []
    for path in os.listdir(os.path.join(root, folder)):
        if (not os.path.isdir(os.path.join(root, folder, path))
                and not path[-4:] == '.jpg'):
            files.append(path)
    files.sort()
    logging.info('Files in ' + folder)
    logging.info(files)
    items = []
    for filename in files:
        item = {
            'title': filename,
            'action': ''.join(
                ['video:', FLAGS.url_prefix, os.path.join(folder, filename)])
        }
        if os.path.exists(os.path.join(root, folder, filename + '.jpg')):
            # To create the images run:
            # IFS=$(echo -en '\n\b'); for i in $(ls); do \
            # ffmpeg -i $i -ss '00:05:00.000' -vframes1 ${i}.jpg; done
            item['image'] = ''.join(
                [FLAGS.url_prefix, os.path.join(folder, filename + '.jpg')])
            item['imageFiller'] = 'width-center'
        else:
            item['icon'] = 'msx-white-soft:movie'
        items.append(item)
    return items


def main(argv):
    if FLAGS.movies_folder is None:
        logging.error('Please define an input folder')
        exit(1)
    initDictStruct()
    createMovieFoldersMenus(FLAGS.movies_folder)
    printMenuToJSON()


if __name__ == '__main__':
    app.run(main)

from emoji_translator_utils.emoji_dict_utils import *
from collections import OrderedDict

import os

from emoji_translator_utils.emoji_dict_utils import unicode_to_fullstring

RAW_EMOJI_FILE = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'raw_emoji_categories.txt')
PARSED_EMOJI_FILE = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'parsed_emoji_categories.txt')

# retrieve categories as a dictionary of lists from an already parsed file
def emoji_categs_from_file():
    write_to_parsedfile()
    with open(PARSED_EMOJI_FILE) as emoji_db:
        lines = emoji_db.readlines()
    emoji_categs = OrderedDict()

    for line in lines:
        line = line.rstrip().lower()
        if line.startswith('-group'):
            emoji_categs[line] = list()
            current_categ = line
        else:
            emoji_categs[current_categ].append(line)

    return emoji_categs

# parse raw file to later retrieve categories
def write_to_parsedfile():
    with open(RAW_EMOJI_FILE) as raw_categs:
        lines = raw_categs.readlines()

    with open(PARSED_EMOJI_FILE, 'w+') as parsed_categs:
        known_emoji_set = {UNICODE_STRING[e].upper() for e in UNICODE_EMOJI}
        for line in lines:
            line = line.rstrip()
            if (not line.startswith('\n')
                and not line.startswith('#-subgroup')
                and not line.startswith('#')
                and not line == ''):
                if line.startswith('-group'):
                    parsed_categs.write(line.lower() + '\n')
                elif line in known_emoji_set:
                    parsed_categs.write(line.lower() + '\n')

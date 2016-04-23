#!/usr/bin/env python

import os
import sys
import re
import mistune
from md2keynote import KeynoteRenderer, process_path
from applescripting import OSAScript


METADATA = r'^\s*(\w+)\s*:\s*(.*?)\s*$'


def preprocess(file):
    # file could be 1) absolute, 2) using ~, 3) using $HOME, or 4) relative (to CWD)
    file = process_path(file, os.getcwd())
    
    meta = {'_BaseDir':os.path.dirname(file)}
    path_keys = ['File']
    lines = []
    with open(file) as f:
        in_metadata = True
        for raw_line in f:
            line = raw_line.decode('utf-8')
            if in_metadata:
                m = re.match(METADATA, line)
                if (m):
                    key = m.group(1)
                    value = m.group(2)
                    meta[key] = value
                else:
                    in_metadata = False
            if not in_metadata:
                lines.append(line)
        text = "".join(lines)
    # Process paths given in metadata section
    # Prepend relative paths with abs path of dir containing the .md file
    for key in path_keys:
        if key in meta:
            meta[key] = process_path(meta[key], meta['_BaseDir'])
            
    return meta, text


def main():

    if len(sys.argv) != 2:
        print 'Usage:\n\t{} <file>\n'.format(sys.argv[0])
        sys.exit(1)
        
    md_file = sys.argv[1]

    with open(os.path.join(os.path.dirname(__file__), "helpers/keynote.applescript")) as f:
        source = f.read().decode('utf-8')
    keynote = OSAScript(source)

    # Extract user options from markdown metadata
    meta, text =  preprocess(md_file)
    theme = meta.get('Theme', 'White')
    doc = keynote.newPresentation(theme)

    user_options = {}
    # Handle buggy templates by overriding some defaults
    if theme in ["Modern Type", "Parchment", "Blueprint", "Graph Paper", "Craft", "Exhibition", "Editorial"]:
        user_options['_FlipQuote'] = True
    default_options = KeynoteRenderer.defaults()
    for known_key, default_value in default_options.iteritems():
        if known_key not in meta:
            continue
        if type(default_value) is bool:
            user_options[known_key] = bool(meta[known_key].upper() == 'TRUE')
        elif type(default_value) is int:
            user_options[known_key] = int(meta[known_key])
        else:
            user_options[known_key] = meta[known_key]
    
    md = mistune.Markdown(renderer=KeynoteRenderer(keynote, doc, user_options))
    md.parse(text)
    keynote.finalize(doc)
    if 'File' in meta:
        keynote.savePresentation(doc, meta['File'])
        keynote.openPresentation(meta['File'])


if __name__ == '__main__':
    sys.exit(main())
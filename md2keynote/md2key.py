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

    meta, text =  preprocess(md_file)
    theme = meta.get('Theme', 'White')
    doc = keynote.newPresentation(theme)

    options = KeynoteRenderer.defaults()
    # Handle buggy templates
    if theme in ["Modern Type", "Parchment", "Blueprint", "Graph Paper", "Craft", "Exhibition", "Editorial"]:
        options['_FlipQuote'] = True
    # Get user options from markdown metadata
    known_options = options.keys()
    user_options = {x: meta[x] for x in known_options if x in meta}
    options.update(user_options)

    md = mistune.Markdown(renderer=KeynoteRenderer(keynote, doc, options))
    md.parse(text)
    keynote.finalize(doc)
    if 'File' in meta:
        keynote.savePresentation(doc, meta['File'])
        keynote.openPresentation(meta['File'])


if __name__ == '__main__':
    sys.exit(main())
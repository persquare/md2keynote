# -*- coding: utf-8 -*-
from applescripting import OSAScript


if __name__ == '__main__':

    with open("keynote.applescript") as f:
        source = f.read().decode('utf-8')

    keynote = OSAScript(source)
    doc = keynote.newPresentation("White")
    # print keynote.themeMasters(doc)
    slide = keynote.createSlide(doc, "Title & Subtitle", "Foo is the new Bar", "Per Persson")
    slide = keynote.createSlide(doc, "Title, Bullets & Photo", "My items", "item 1\nitem 2")
    keynote.addImage(doc, "/Users/per/Desktop/bild.png")
    keynote.finalize(doc)



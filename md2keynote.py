# -*- coding: utf-8 -*-
from applescripting import OSAScript


if __name__ == '__main__':

    with open("keynote.applescript") as f:
        source = f.read().decode('utf-8')

    keynote = OSAScript(source)
    doc = keynote.newPresentation("EricssonFinal")
    print keynote.themeMasters(doc)
    status = keynote.createSlide(doc, "Title & Subtitle", "Foo is the new Bar", "Per Persson")
    status = keynote.createSlide(doc, "Title & Bullets", "My items", "item 1\nitem 2")
    keynote.finalize(doc)
    print status


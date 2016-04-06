
from applescripting import OSAScript


if __name__ == '__main__':

    with open("keynote.applescript") as f:
        source = f.read().decode('utf-8')

    keynote = OSAScript(source)
    doc = keynote.newPresentation("White")
    # # print keynote.themeMasters(doc)
    # slide = keynote.createSlide(doc, "Title & Subtitle")
    # keynote.addTitle(doc, "Foo is the new Bar", "Per Persson")
    # keynote.addBody(doc, "Per Persson")
    #
    # slide = keynote.createSlide(doc, "Title, Bullets & Photo")
    # keynote.addTitle(doc, "My items")
    # keynote.addBody(doc, "item 1\nitem 2")
    # keynote.addImage(doc, "/Users/per/Desktop/bild.png")
    index = keynote.createSlide(doc, "Quote")
    keynote.addText(doc, index, 1, "QE2")
    keynote.addText(doc, index, 2, "\"Keep Calm\"")
    # Use [] for no styling
    keynote.addStyledTextItem(doc, index, "theText", [(65535,0,0), (0,65535,0), (0,0,65535)], (100, 200), 36, "Menlo")
    keynote.addPresenterNotes(doc, index, "XYZ")
    keynote.finalize(doc)
    # keynote.deleteAllSlides(doc)
    keynote.savePresentation(doc, "/Users/eperspe/Documents/test88.key")



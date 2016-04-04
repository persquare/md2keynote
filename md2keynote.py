# -*- coding: utf-8 -*-

import os
import re
import mistune
from applescripting import OSAScript

METADATA = r'^\s*(\w+)\s*:\s*(.*?)\s*$'

def process_path(path):
    return os.path.abspath(os.path.expandvars(os.path.expanduser(path)))

def preprocess(file):
    path_keys = ['File']
    meta = {}
    lines = []
    with open(file) as f:
        in_metadata = True
        for line in f:
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
    # Process paths
    for key in path_keys:
        if key in meta:
            meta[key] = process_path(meta[key])

    return meta, text


class KeynoteRenderer(mistune.Renderer):
    """The default HTML renderer for rendering Markdown.
    """
    def __init__(self, keynote, doc, **kwargs):
        super(KeynoteRenderer, self).__init__(**kwargs)
        self.keynote = keynote
        self.doc = doc
        self._count = 1 # Starts with a dummy slide
        self._reset_state()

    def _reset_state(self):
        self._state = {}
        self._order = []
        self._paragraphs = []


    def new_slide(self):
        self._count += 1

        keys = self._state.keys()
        key_count = len(keys)

        handler = self.malformed_slide
        if key_count == 0:
            handler = self.new_blank_slide
        elif key_count == 1:
            handler = {
                'title': self.new_title_center_slide,
                'images': self.new_photo_slide,
                'quote': self.new_quote_slide,
                'bullets' : self.new_bullet_slide
            }.get(keys[0], self.malformed_slide)
        elif key_count == 2:
            if 'title' in keys:
                if 'subtitle' in keys:
                    handler = self.new_title_subtitle_slide
                elif 'bullets' in keys:
                    handler = self.new_title_bullets_slide
        elif key_count == 3:
            if 'title' in keys and 'images' in keys:
                if 'subtitle' in keys:
                    handler = self.new_title_photo_slide
                elif 'bullets' in keys:
                    handler = self.new_title_bullets_photo_slide
        try:
            handler()
        except Exception as e:
            print e
            self.malformed_slide()
        finally:
            self._reset_state()


    def malformed_slide(self):
        print "Slide {} is malformed, skipping".format(self._count)
        print
        print self._state
        print
        print "    ", self._state.get('title', '---')
        print "    ", self._state.keys()
        print "    ", self._paragraphs
        print "    ", self._order
        print


    def new_blank_slide(self):
        master = 'Blank'
        self.keynote.createSlide(self.doc, master)
        self.add_notes(master)

    def new_title_center_slide(self):
        master = 'Title - Center'
        self.keynote.createSlide(self.doc, master)
        self.keynote.addTitle(self.doc, self._count, self._state['title'])
        self.add_notes(master)

    def new_photo_slide(self):
        if len(self._state['images']) == 1:
            master = 'Photo'
        else:
            master = 'Photo - 3 Up'
        self.keynote.createSlide(self.doc, master)
        images = self._state['images']
        for n in range(0, min(len(images), 3)):
            self.keynote.addImage(self.doc, self._count, n+1, images[-(n+1)][0])
        self.add_notes(master)

    def new_quote_slide(self):
        master = 'Quote'
        self.keynote.createSlide(self.doc, master)
        self.keynote.addText(self.doc, self._count, 2, self._state['quote'])
        self.keynote.addText(self.doc, self._count, 1, self._paragraphs[1])
        self.add_notes(master)

    def new_bullet_slide(self):
        master = 'Bullets'
        self.keynote.createSlide(self.doc, master)
        self.keynote.addBody(self.doc, self._count, '\n'.join(self._state['bullets']))
        self.add_notes(master)

    def new_title_subtitle_slide(self):
        master = 'Title & Subtitle'
        self.keynote.createSlide(self.doc, master)
        self.keynote.addTitle(self.doc, self._count, self._state['title'])
        self.keynote.addBody(self.doc, self._count, self._state['subtitle'])
        self.add_notes(master)

    def new_title_bullets_slide(self):
        master = 'Title & Bullets'
        self.keynote.createSlide(self.doc, master)
        self.keynote.addTitle(self.doc, self._count, self._state['title'])
        self.keynote.addBody(self.doc, self._count, '\n'.join(self._state['bullets']))
        self.add_notes(master)

    def new_title_bullets_photo_slide(self):
        master = 'Title, Bullets & Photo'
        self.keynote.createSlide(self.doc, master)
        self.keynote.addTitle(self.doc, self._count, self._state['title'])
        self.keynote.addBody(self.doc, self._count, '\n'.join(self._state['bullets']))
        self.keynote.addImage(self.doc, self._count, 1, self._state['images'][0][0])
        self.add_notes(master)

    def new_title_photo_slide(self):
        if self._order == ['title', 'image', 'subtitle']:
            master = 'Photo - Horizontal'
        else:
            master = 'Photo - Vertical'
        self.keynote.createSlide(self.doc, master)
        self.keynote.addTitle(self.doc, self._count, self._state['title'])
        self.keynote.addBody(self.doc, self._count, self._state['subtitle'])
        self.keynote.addImage(self.doc, self._count, 1, self._state['images'][0][0])
        self.add_notes(master)

    def add_notes(self, master):
        start_index = {
            'Photo - 3 Up': 0,
            'Photo': 0,
            'Blank': 0,
            'Bullets': 0,
            'Title - Center': 1,
            'Title - Top': 1,
            'Title & Bullets': 1,
            'Title, Bullets & Photo': 1,
            'Title & Subtitle': 2,
            'Photo - Horizontal': 2,
            'Photo - Vertical': 2,
            'Quote': 2
        }.get(master)

        # Bullets counts as paragraphs
        start_index += len(self._state.get('bullets', []))
        notes = self._paragraphs[start_index:]
        if notes:
            self.keynote.addPresenterNotes(self.doc, self._count, "\n\n".join(notes))


    def block_code(self, code, lang=None):
        """Rendering block level code. ``pre > code``.

        :param code: text content of the code block.
        :param lang: language of the given code.
        """
        return 'block_code\n'

    def block_quote(self, text):
        """Rendering <blockquote> with the given text.

        :param text: text content of the blockquote.
        """
        self._state['quote'] = text
        return ''

    def block_html(self, html):
        """Rendering block level pure html content.

        :param html: text content of the html snippet.
        """
        return 'block_html\n'

    def header(self, text, level, raw=None):
        """Rendering header/heading tags like ``<h1>`` ``<h2>``.

        :param text: rendered text content for the header.
        :param level: a number for the header level, for example: 1.
        :param raw: raw text content of the header.
        """
        kind = None
        if level == 1:
            kind = 'title'
        elif level == 2:
            kind = 'subtitle'
        if kind:
            self._state[kind] = text.strip()
            self._order.append(kind)
        return ''

    def hrule(self):
        """Rendering method for ``<hr>`` tag."""
        self.new_slide()
        return ''

    def list(self, body, ordered=True):
        """Rendering list tags like ``<ul>`` and ``<ol>``.

        :param body: body contents of the list.
        :param ordered: whether this list is ordered or not.
        """
        self._state['bullets'] = body.strip().split('\n')
        return ''

    def list_item(self, text):
        """Rendering list item snippet. Like ``<li>``."""
        return '{}\n'.format(text)

    def paragraph(self, text):
        """Rendering paragraph tags. Like ``<p>``."""
        return text

    def table(self, header, body):
        """Rendering table element. Wrap header and body in it.

        :param header: header part of the table.
        :param body: body part of the table.
        """
        return 'table\n'

    def table_row(self, content):
        """Rendering a table row. Like ``<tr>``.

        :param content: content of current table row.
        """
        return 'table_row\n'

    def table_cell(self, content, **flags):
        """Rendering a table cell. Like ``<th>`` ``<td>``.

        :param content: content of current table cell.
        :param header: whether this is header or not.
        :param align: align of current table cell.
        """
        return 'table_cell\n'

    def double_emphasis(self, text):
        """Rendering **strong** text.

        :param text: text content for emphasis.
        """
        return 'double_emphasis\n'

    def emphasis(self, text):
        """Rendering *emphasis* text.

        :param text: text content for emphasis.
        """
        return 'emphasis\n'

    def codespan(self, text):
        """Rendering inline `code` text.

        :param text: text content for inline code.
        """
        return 'codespan\n'

    def linebreak(self):
        """Rendering line break like ``<br>``."""
        return 'linebreak\n'

    def strikethrough(self, text):
        """Rendering ~~strikethrough~~ text.

        :param text: text content for strikethrough.
        """
        return 'strikethrough\n'

    def text(self, text):
        """Rendering unformatted text.

        :param text: text content.
        """
        text = text.strip()
        if text:
            self._paragraphs.append(text)
        return text

    def autolink(self, link, is_email=False):
        """Rendering a given link or email address.

        :param link: link content or email address.
        :param is_email: whether this is an email or not.
        """
        return 'autolink\n'

    def link(self, link, title, text):
        """Rendering a given link with content and title.

        :param link: href link for ``<a>`` tag.
        :param title: title content for `title` attribute.
        :param text: text content for description.
        """
        return 'link\n'

    def image(self, src, title, text):
        """Rendering a image with title and text.

        :param src: source link of the image.
        :param title: title text of the image.
        :param text: alt text of the image.
        """
        self._state.setdefault('images', [])
        self._state['images'].append([process_path(src), title, text])
        self._order.append('image')
        return ''

    def inline_html(self, html):
        """Rendering span level pure html content.

        :param html: text content of the html snippet.
        """
        return 'inline_html\n'

    def newline(self):
        """Rendering newline element."""
        return 'newline\n'

    def footnote_ref(self, key, index):
        """Rendering the ref anchor of a footnote.

        :param key: identity key for the footnote.
        :param index: the index count of current footnote.
        """
        return 'footnote_ref\n'

    def footnote_item(self, key, text):
        """Rendering a footnote item.

        :param key: identity key for the footnote.
        :param text: text content of the footnote.
        """
        return 'footnote_item\n'

    def footnotes(self, text):
        """Wrapper for all footnotes.

        :param text: contents of all footnotes.
        """
        return 'footnotes\n'





if __name__ == '__main__':

    with open("keynote.applescript") as f:
        source = f.read().decode('utf-8')
    keynote = OSAScript(source)

    meta, text =  preprocess("test.md")
    doc = keynote.newPresentation("White")
    md = mistune.Markdown(renderer=KeynoteRenderer(keynote, doc))
    result = md.parse(text)
    keynote.finalize(doc)
    if 'File' in meta:
        keynote.savePresentation(doc, meta['File'])
        keynote.openPresentation(meta['File'])

    #
# if __name__ == '__main__':
#
#     with open("keynote.applescript") as f:
#         source = f.read().decode('utf-8')
#
#     keynote = OSAScript(source)
#     doc = keynote.newPresentation("White")
#     # print keynote.themeMasters(doc)
#     slide = keynote.createSlide(doc, "Title & Subtitle")
#     keynote.addTitle(doc, "Foo is the new Bar", "Per Persson")
#     keynote.addBody(doc, "Per Persson")
#
#     slide = keynote.createSlide(doc, "Title, Bullets & Photo")
#     keynote.addTitle(doc, "My items")
#     keynote.addBody(doc, "item 1\nitem 2")
#     keynote.addImage(doc, "/Users/per/Desktop/bild.png")
#     keynote.finalize(doc)
#     # keynote.deleteAllSlides(doc)
#     keynote.savePresentation(doc, "/Users/per/Documents/test88.key")



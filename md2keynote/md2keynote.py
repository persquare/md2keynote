# -*- coding: utf-8 -*-

import os
import copy
import tempfile
import mistune
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatter import Formatter
from seqdiag import parser, builder, drawer
from blockdiag.utils.fontmap import FontMap
from applescripting import OSAScript


def process_path(filepath, basepath):
    filepath = filepath.decode('string_escape')
    filepath = os.path.expanduser(filepath)
    filepath = os.path.expandvars(filepath)
    filepath = os.path.normpath(os.path.join(basepath, filepath))

    return filepath


class RunFormatter(Formatter):
    def __init__(self, **options):
        Formatter.__init__(self, **options)
        # create a dict of (start, end) tuples that wrap the
        # value of a token so that we can use it in the format
        # method later
        self.styles = {}
        for token, style in self.style:
            # a style item is a tuple in the following form:
            # colors are readily specified in hex: 'RRGGBB'
            if style['color']:
                 self.styles[token] =  style['color']

    def format(self, tokensource, outfile):
        for ttype, value in tokensource:
            while ttype and ttype not in self.styles:
                ttype = ttype.parent
            outfile.write(len(value) * self.styles.get(ttype, "000000"))

def rgb_to_ASRGB(rgb):
    asrgb = tuple([257*int(rgb[i:i+2], 16) for i in range(0, len(rgb), 2)])
    return asrgb

def run_to_ASRGB(run):
    return [rgb_to_ASRGB(run[i:i+6]) for i in range(0, len(run), 6)]




class KeynoteRenderer(mistune.Renderer):
    """The default HTML renderer for rendering Markdown.
    """

    def __init__(self, keynote, doc, options=None, **kwargs):
        super(KeynoteRenderer, self).__init__(**kwargs)
        self.keynote = keynote
        self.doc = doc
        self._reset_state()
        self._options = self.defaults()
        if options:
            self._options.update(options)

    @staticmethod
    def defaults():
        return copy.copy({'HighlightCode':True, 'CodeFont': 'Menlo', 'CodeFontSize': 16, '_FlipQuote': False, '_BaseDir':os.getcwd()})

    def _reset_state(self):
        self._state = {}
        self._order = []
        self._paragraphs = []
        self._count = 0


    def new_slide(self):

        keys = self._state.keys()
        key_count = len(keys)

        handler = self.malformed_slide
        if key_count == 0:
            handler = self.new_blank_slide
        elif key_count == 1:
            handler = {
                'title': self.new_title_center_slide,
                'media': self.new_photo_slide,
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
            if 'title' in keys and 'media' in keys:
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
        self._count = self.keynote.createSlide(self.doc, master)
        self.add_notes(master)

    def new_title_center_slide(self):
        master = 'Title - Center'
        self._count = self.keynote.createSlide(self.doc, master)
        self.keynote.addTitle(self.doc, self._count, self._state['title'])
        self.add_notes(master)

    def new_photo_slide(self):
        if len(self._state['media']) == 1:
            master = 'Photo'
            i = 1
        else:
            master = 'Photo - 3 Up'
            i = 3
        self._count = self.keynote.createSlide(self.doc, master)
        media = self._state['media'][0:3]
        # Must iterate backwards since we might delete placeholder images if media is not image
        for m in media:
            self.add_media(i, m, master)
            i -= 1
        self.add_notes(master)

    def new_quote_slide(self):
        master = 'Quote'
        quote_index, attr_index = 2, 1
        if self._options['_FlipQuote']:
            quote_index, attr_index = attr_index, quote_index
        self._count = self.keynote.createSlide(self.doc, master)
        self.keynote.addText(self.doc, self._count, quote_index, self._state['quote'])
        self.keynote.addText(self.doc, self._count, attr_index, self._paragraphs[1])
        self.add_notes(master)

    def new_bullet_slide(self):
        master = 'Bullets'
        self._count = self.keynote.createSlide(self.doc, master)
        self.keynote.addBody(self.doc, self._count, '\n'.join(self._state['bullets']))
        self.add_notes(master)

    def new_title_subtitle_slide(self):
        master = 'Title & Subtitle'
        self._count = self.keynote.createSlide(self.doc, master)
        self.keynote.addTitle(self.doc, self._count, self._state['title'])
        self.keynote.addBody(self.doc, self._count, self._state['subtitle'])
        self.add_notes(master)

    def new_title_bullets_slide(self):
        master = 'Title & Bullets'
        self._count = self.keynote.createSlide(self.doc, master)
        self.keynote.addTitle(self.doc, self._count, self._state['title'])
        self.keynote.addBody(self.doc, self._count, '\n'.join(self._state['bullets']))
        self.add_notes(master)

    def new_title_bullets_photo_slide(self):
        master = 'Title, Bullets & Photo'
        self._count = self.keynote.createSlide(self.doc, master)
        self.keynote.addTitle(self.doc, self._count, self._state['title'])
        self.keynote.addBody(self.doc, self._count, '\n'.join(self._state['bullets']))
        # Allow more code snippet than there are placeholders
        count = 1
        for media in self._state['media']:
            self.add_media(count, media, master)
            count += 1
        self.add_notes(master)

    def new_title_photo_slide(self):
        if self._order == ['title', 'image', 'subtitle']:
            master = 'Photo - Horizontal'
        else:
            master = 'Photo - Vertical'
        self._count = self.keynote.createSlide(self.doc, master)
        self.keynote.addTitle(self.doc, self._count, self._state['title'])
        self.keynote.addBody(self.doc, self._count, self._state['subtitle'])
        self.add_media(1, self._state['media'][0], master)
        self.add_notes(master)


    def add_media(self, placeholderIndex, media, master):
        if len(media) == 3:
            # media is image
            self.keynote.addImage(self.doc, self._count, placeholderIndex, media[0])
        else:
            # media is code
            fontsize = self._options['CodeFontSize']
            fontname = self._options['CodeFont']
            source, style = media
            slots = self.media_slots(master)
            if placeholderIndex <= slots:
                self.keynote.addStyledTextItemAsMedia(self.doc, self._count, placeholderIndex, source, style, fontsize, fontname)
            else:
                position = (100*(placeholderIndex - slots), 100*(placeholderIndex - slots))
                self.keynote.addStyledTextItem(self.doc, self._count, source, style, position, fontsize, fontname)

    # def add_code(self):
    #     if not 'code' in self._state:
    #         return
    #     x, y = 0, 0
    #     fontsize = self._options.get('CodeFontSize', 18)
    #     fontname = self._options.get('CodeFont', 'Menlo')
    #
    #     for code, styling in self._state['code']:
    #         x += 100
    #         y += 100
    #         self.keynote.addStyledTextItem(self.doc, self._count, code, styling, (x, y), fontsize, fontname)


    def media_slots(self, master):
        return {
            'Photo - 3 Up': 3,
            'Photo': 1,
            'Blank': 0,
            'Bullets': 0,
            'Title - Center': 0,
            'Title - Top': 0,
            'Title & Bullets': 0,
            'Title, Bullets & Photo': 1,
            'Title & Subtitle': 0,
            'Photo - Horizontal': 1,
            'Photo - Vertical': 1,
            'Quote': 0
        }.get(master, 0)



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

    def media_from_seqdiag(self, code, lang):
        fmt = 'pdf'
        tempdir = tempfile.gettempdir()
        n = len(self._state.setdefault('media', []))
        mediafile = os.path.join(tempdir, "{}_{}_{}.{}".format(self.doc, self._count, n, fmt))
        fontmap = FontMap()
        # FIXME: Get font from master slide body text
        fontmap.set_default_font('/Library/Fonts/Arial.ttf')
        tree = parser.parse_string(code)
        diagram = builder.ScreenNodeBuilder.build(tree)
        draw = drawer.DiagramDraw(fmt, diagram, mediafile, fontmap=fontmap, nodoctype=True)
        draw.draw()
        draw.save()
        self.image(mediafile, "title", "alt text")


    def media_from_code(self, code, lang):
        styling = []
        if self._options['HighlightCode']:
            try:
                lexer = get_lexer_by_name(lang, stripall=False)
                run = highlight(code, lexer, RunFormatter())
                styling = run_to_ASRGB(run)
            except:
                styling = []
        self._state.setdefault('media', [])
        self._state['media'].append([code, styling])
        self._order.append('media')


    def block_code(self, code, lang=None):
        """Rendering block level code. ``pre > code``.

        :param code: text content of the code block.
        :param lang: language of the given code.
        """
        code = code.rstrip()
        handler = {
            'seqdiag':self.media_from_seqdiag,
        }.get(lang, self.media_from_code)
        handler(code, lang)
        return ''

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
        self._state.setdefault('media', [])
        self._state['media'].append([process_path(src, self._options['_BaseDir']), title, text])
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






Date   : 2016-04-04
Theme  : White
File   : ~/Documents/md2keynote.key
CodeFont : Menlo
CodeFontSize : 18


# Presentation Zen with Markdown

## md2keynote

----

# Map markdown to content

- heading 1 becomes title
- heading 2 becomes subtitle
- item list becomes bullets
- image link and code becomes image
- quote + text becomes quote + attribution 
- horisontal line marks end of slide
- text paragraphs becomes presenters notes


        # Map markdown to content
        
        - heading 1 becomes title
        - heading 2 becomes subtitle
        - item list becomes bullets
        - image link and code becomes image
        - quote + text becomes quote + attribution 
        - horisontal line marks end of slide
        - text paragraphs becomes presenters notes
        
        ----

----

# Embrace Master Slides

- Custom masters must implement:
- Title & Subtitle
- Photo - Horizontal
- Title - Center
- Photo - Vertical
- Title - Top
- Title & Bullets
- Title, Bullets & Photo
- Bullets
- Photo - 3 Up
- Quote                 
- Photo
- Blank

![master slides][1]

----

# Metadata in markdown

- Theme (theme selection)
- File (to save in)
- CodeFont (for code blocks)
- CodeFontSize (for code blocks)


        Date   : 2016-04-04
        Theme  : White
        File   : ~/Documents/md2keynote.key
        CodeFont : Menlo
        CodeFontSize : 18

----

# Known issues

- No bold or emphasis in bullets
- No sub-bullets
- Code blocks are centered
- Spaces in file references must be escaped (\x20)

----

# Showcase

## The 12 Masters

----

# Title & Subtitle

## Subtitle

Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.

Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.

----

# Photo - Horizontal

![alt text][2]

## Subtitle

Note the ordering of image and subtitle compared to 'Photo - Vertical' below

----

# Title - Center

----

# Photo - Vertical

## Subtitle

![alt text][2]

Note the ordering of image and subtitle compared to 'Photo - Horizontal' above

----

# Title - Top

----

# Title & Bullets

- item 1
- item 2

----

# Title, Bullets & Photo

- item 1
- item 2

![alt text][2]

----

- bullets only slide
- bullet 2

----

![alt text][2]

```python
# Code blocks (indented or fenced) behave
# as images wrt choosing a template and 
# images and code blocks can be used 
# interchangeably

def hello():
    print "Hello World!"
```

![alt text][2]

----

> a quote

attribution text

Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.

----

![alt text][2]

----


Blank slide

----


[1]: slide_layout.png 
[2]: /Library/Desktop\x20Pictures/Frog.jpg



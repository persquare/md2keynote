Date   : 2016-04-04
Theme  : White
File   : ~/Documents/test2.key
Author : Per Persson


# Title & Subtitle

## Subtitle

Notes

More notes

----

# Photo - Horizontal

![alt text][1]

## Subtitle

Notes

More notes

----


# Title - Center

Notes

More notes

----

# Photo - Vertical

## Subtitle

![alt text][1]

Notes

More notes

----

# Code - Vertical

## Subtitle

    Block code
    monospace text

Notes

More notes


# Title - Top

Notes

More notes

----


# Title & Bullets

- item 1
- item 2

Notes

More notes

----


# Title, Bullets & Photo

- item 1
- item 2

![alt text][1]

Notes

More notes

----

# Title, Bullets & Code

- item 1
- item 2

```python
print "Hello fenced code"
```

Notes

More notes

----


- bullet 1
- bullet 2

Notes

More notes

----


![alt text][1]

![alt text][2]

![alt text][3]

Notes

More notes

----


![alt text][1]

```calvinscript
/*
TOP RIGHT
*/

/* Actors */
src : std.CountTimer(sleep=10)
sensor : sensor.Environmental()
display : io.Display()

/* Connections */
src.integer > sensor.trigger
sensor.data > display.text
```

```calvinscript
/*
BOTTOM RIGHT
*/

/* Actors */
src : std.CountTimer(sleep=10)
sensor : sensor.Environmental()
display : io.Display()

/* Connections */
src.integer > sensor.trigger
sensor.data > display.text
```

Notes

More notes

----


----


```calvinscript
/*
LEFT
*/

/* Actors */
src : std.CountTimer(sleep=10)
sensor : sensor.Environmental()
display : io.Display()

/* Connections */
src.integer > sensor.trigger
sensor.data > display.text
```

```calvinscript
/*
TOP RIGHT
*/

/* Actors */
src : std.CountTimer(sleep=10)
sensor : sensor.Environmental()
display : io.Display()

/* Connections */
src.integer > sensor.trigger
sensor.data > display.text
```

```calvinscript
/*
BOTTOM RIGHT
*/

/* Actors */
src : std.CountTimer(sleep=10)
sensor : sensor.Environmental()
display : io.Display()

/* Connections */
src.integer > sensor.trigger
sensor.data > display.text
```


Code

More notes

----

> a quote

attribution text

Notes

More notes

----


![alt text][1]

Notes

More notes

----

```calvinscript
/* Actors */
src : std.CountTimer(sleep=10)
sensor : sensor.Environmental()
display : io.Display()

/* Connections */
src.integer > sensor.trigger
sensor.data > display.text
```

Notes

More notes

----


Notes

More notes

----

[1]: ~/Desktop/raven.png "Text"
[2]: ~/Desktop/raven2.jpg "Text"
[3]: ~/Desktop/raven3.jpg "Text"


<!--![alt text](~/Desktop/raven.jpg "Img title")-->

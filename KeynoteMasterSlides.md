# md2keynote syntax

- Horizontal rule indicates end of slide
- Trailing paragraphs becomes presenter's notes

## Title slides
These are slides that preceeds a distinct section of the presentation

### Title & Subtitle 

    # Title
    
    ## Subtitle
    
    ----
 
### Photo - Horizontal

    # Title
    
    ![An image][1]
    
    ## Subtitle
    
    ----

   
### Title - Center        

    # Title
    
    ----

### Photo - Vertical

    # Title
    
    ## Subtitle
    
    ![An image][1]
    
    ----

## Content slides
These are slides that convey a message, typically as bullets    

### Title - Top    

**NOT USED**. Conflicts 'Title - Center' above 

    # Title
    
    ----  
 
### Title & Bullets

    # Title  
    
    - item
    - item
    
    ----
   
### Title, Bullets & Photo

    # Title  
    
    - item
    - item
    
    ![An image][1]
    
    ----

or

    # Title  
    
    ![An image][1]
    
    - item
    - item
    
    ----

### Bullets 


    - item
    - item
    
    ----

## Special slides
These are slides that have a particular layout and are less frequently used

### Photo - 3 Up   

Order is left, top right, bottom right

    ![An image][1]
    ![An image][2]
    ![An image][3]
    
    ----

### Quote     

    > a quote
    
    attribution text
    
    ----

### Photo 

    ![An image][1]
    
    ----

### Blank  

    ----


# Discrimination order

1. empty state => 'Blank'           #keys = 0
2. title => 'Title - Center'        #keys = 1
3. single image => 'Photo'          #keys = 1
4. three images => 'Photo - 3 Up'   #keys = 1
5. quote => 'Quote'                 #keys = 1
    - optional attribution in paragraphs[2]
6. bullets => 'Bullets'             #keys = 1
7. title, subtitle => 'Title & Subtitle' #keys = 2
8. title, bullets => 'Title & Bullets' #keys = 2
9. title, images, bullets => 'Title, Bullets & Photo' #keys = 3
10. title, subtitle, images  =>      #keys = 3
    - use order to distinguish
        - title, image, subtitle => 'Photo - Horizontal'
        - title, subtitle, image => 'Photo - Vertical'
 

    

# Default slide styles

	Modern Portfolio             White                           Custom 
	----------------             -----                           -------------
	u'Title & Subtitle'          u'Title & Subtitle'             u'Title and subtitle' # Wrong name
	u'Photo - Horizontal'        u'Photo - Horizontal'           u'Title'                     
	u'Title - Center'            u'Title - Center'               u'Title copy'
	u'Photo - Vertical'          u'Photo - Vertical'             u'Title only'
	u'Title - Top'               u'Title - Top'                  u'Title and single'
	u'Title & Bullets'           u'Title & Bullets'              u'Title & image right'
	u'Title, Bullets & Photo'    u'Title, Bullets & Photo'       u'Title & image left'
	u'Bullets'                   u'Bullets'                      
	u'Photo - 3 Up'              u'Photo - 3 Up'                 
	u'Quote'                     u'Quote'                        
	u'Photo'                     u'Photo'                        
	u'Blank'                     u'Blank'                        u'Blank'
                             


![Slide Layout][1]





[1]: ./slide_layout.png

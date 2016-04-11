on newPresentation(themeName)
	tell application "Keynote"
		-- FIXME: Make this selectable?
		set targetWidth to 1024 -- 1440 <-- higher resolution
		set targetHeight to 768 -- 1080 <-- higher resolution

		set props to {document theme:theme (themeName as string), width:targetWidth, height:targetHeight}

		set thisDocument to make new document with properties props
		return id of thisDocument
	end tell
end newPresentation

on openPresentation(posixPath)
	tell application "Keynote"
		open posixPath
	end tell
end openPresentation

on savePresentation(docId, posixPath)
	tell application "Keynote"	
        set theDocument to document id docId
		save theDocument in POSIX file posixPath
        delete theDocument
        open posixPath 
	end tell
end savePresentation	

on closePresentation(docId)
	tell application "Keynote"	
        set theDocument to document id docId
		close theDocument
	end tell
end savePresentation	


on createSlide(docId, masterSlideName)
	tell application "Keynote"
		tell document id docId
			set thisSlide to make new slide with properties {base slide:master slide masterSlideName}
		end tell
		return slide number of thisSlide
	end tell
end createSlide

on deleteAllSlides(docId)
	tell application "Keynote"
		tell document id docId to delete every slide
	end tell
end deleteAllSlides

on finalize(docId)
	tell application "Keynote"
		tell document id docId to delete slide 1
	end tell
end finalize

on themeMasters(docId)
	--	  tell application "Keynote" to get the name of every master slide of thisDocument
	tell application "Keynote"
		set names to the name of every master slide of document id docId
		return names
	end tell
end themeMasters

on addImage(docId, slideIndex, n, filepath)
  tell application "Keynote"
	tell slide slideIndex of document id docId
		-- TO REPLACE A PLACEHOLDER OR EXISTING IMAGE:
		set thisPlaceholderImageItem to image n
		-- change the value of the “file name” property of the image to be an HFS file reference to the replacement image file
	    set macPath to POSIX file filepath as Unicode text
		set file name of thisPlaceholderImageItem to ¬
			alias macPath
	end tell
  end tell
end addImage


on addTitle(docId, slideIndex, thisSlideTitle)
	tell application "Keynote"
    	tell slide slideIndex of document id docId
			set the object text of the default title item to thisSlideTitle
		end tell
	end tell
end addTitle

on addBody(docId, slideIndex, thisSlideBody)
	tell application "Keynote"
    	tell slide slideIndex of document id docId
            set the object text of the default body item to thisSlideBody
		end tell
	end tell
end addTitle

on addPresenterNotes(docId, slideIndex, theNotes)
	tell application "Keynote"
    	tell slide slideIndex of document id docId
			set presenter notes to theNotes
		end tell
	end tell
end addPresenterNotes

on addText(docId, slideIndex, itemIndex, theText)
  tell application "Keynote"
  	tell slide slideIndex of document id docId
		set thisPlaceholderItem to text item itemIndex
		set object text of thisPlaceholderItem to theText
	end tell
  end tell
end addText

on addStyledTextItemAsMedia(docId, slideIndex, mediaIndex, theText, theStyleList, theSize, theFont)
	tell application "Keynote"
		tell slide slideIndex of document id docId
            set thisImage to image mediaIndex
            -- copy {position:position of thisImage, width:width of thisImage, height:height of thisImage} to info
            copy position of thisImage to thePosition
            delete thisImage
        end tell        
    end tell    
    my addStyledTextItem(docId, slideIndex, theText, theStyleList, thePosition, theSize, theFont)
end addStyledTextItemAsMedia

on addStyledTextItem(docId, slideIndex, theText, theStyleList, thePosition, theSize, theFont)
	tell application "Keynote"
		tell slide slideIndex of document id docId
			set thisTextItem to make new text item with properties {object text:theText}
			tell thisTextItem
				-- set type size
				set the size of its object text to theSize
				-- set typeface
				set the font of its object text to theFont
				-- adjust its vertical positon
				set its position to thePosition
				-- style the text
				repeat with i from 1 to my min(the length of theStyleList, the length of theText)
					set thisRGBColorValue to item i of theStyleList
					set the color of character i of object text to thisRGBColorValue
				end repeat
			end tell
		end tell
	end tell
end addStyledTextItem

on min(a, b)
	if a < b then
		set x to a
	else
		set x to b
	end if
	return x
end min



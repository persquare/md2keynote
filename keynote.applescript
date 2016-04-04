on newPresentation(themeName)
	tell application "Keynote"
		activate
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
		activate	
        set theDocument to document id docId
		save theDocument in POSIX file posixPath
        delete theDocument
        open posixPath 
	end tell
end savePresentation	

on closePresentation(docId)
	tell application "Keynote"	
		activate	
        set theDocument to document id docId
		close theDocument
	end tell
end savePresentation	


on createSlide(docId, masterSlideName)
	tell application "Keynote"
		tell document id docId
			set thisSlide to make new slide with properties {base slide:master slide masterSlideName}
		end tell
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

on addText(docId, slideIndex, n, theText)
  tell application "Keynote"
  	tell slide slideIndex of document id docId
		set thisPlaceholderItem to text item n
		set object text of thisPlaceholderItem to theText
	end tell
  end tell
end addText


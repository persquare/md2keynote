on newPresentation(themeName)
	tell application "Keynote"
		activate
		-- set the chosenTheme to themeName


		set targetWidth to 1024 -- 1440 <-- higher resolution
		set targetHeight to 768 -- 1080 <-- higher resolution

		set thisDocument to ¬
			make new document with properties ¬
				{document theme:theme (themeName as string)}
				--{document theme:theme (themeName as string), width:targetWidth, height:targetHeight}
		return name of thisDocument
	end tell
end newPresentation


on savePresentation(docname, posixPath)
	tell application "Keynote"
		save document named docname in POSIX file posixPath
	end tell
end savePresentation	

on createSlide(docname, masterSlideName, thisSlideTitle, thisSlideBody)
	try
		tell application "Keynote"
			tell document named docname
				set thisSlide to make new slide with properties {base slide:master slide masterSlideName}
				tell thisSlide
					-- set the transition properties to {transition effect:dissolve, transition duration:defaultTransitionDuration, transition delay:defaultTransitionDelay, automatic transition:defaultAutomaticTransition}
					if title showing is true then
						set the object text of the default title item to thisSlideTitle
					end if
					if body showing is true then
						set the object text of the default body item to thisSlideBody
					end if
				end tell
			end tell
	  return thisSlide
		end tell
	on error
		return 0
	end try
end createSlide

on finalize(docname)
	tell application "Keynote"
		tell document named docname to delete slide 1
	end tell
end finalize

on themeMasters(docname)
	--	  tell application "Keynote" to get the name of every master slide of thisDocument
	tell application "Keynote"
		set names to the name of every master slide of document named docname
		return names
	end tell
end themeMasters

on addImage(docname, filepath)
  (*
	FIXME: Use slide ID to adress slide instead of "current slide"
  *)
  tell application "Keynote"
	tell document named docname
		tell the current slide
			
			-- TO REPLACE A PLACEHOLDER OR EXISTING IMAGE:
			set thisPlaceholderImageItem to image 1
			-- change the value of the “file name” property of the image to be an HFS file reference to the replacement image file
		set macPath to POSIX file filepath as Unicode text
			set file name of thisPlaceholderImageItem to ¬
				alias macPath
			
		end tell
	end tell
  end tell
end addImage


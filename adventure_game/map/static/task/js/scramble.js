$(".scramble").each ->
  $this = $(this)
  $letters = $this.find(".scrambled-letter").not(".drag-clone")
  $spacers = $this.find(".spacer")
  unscrambledWord = $this.data("unscrambled")
  scrambledWord = $this.data("scrambled")
  spacerHTML = "<span class=\"spacer\"></span>"
  
  # If no scrambled version of the word was provided, create one by randomizing the letters    
  if $letters.length is 0 and scrambledWord is `undefined` and unscrambledWord isnt `undefined`
    
    # This do-while loop will prevent the scrambled word from being the same as the unscrambled one due to terribly bad luck
    randomize = ->
      0.5 - Math.random()
    loop
      scrambledWord = unscrambledWord.split("").sort(randomize).join("")
      break unless scrambledWord is unscrambledWord
  
  # Create the letters based on the data attribute
  if scrambledWord isnt `undefined` and $letters.length is 0
    $.map scrambledWord.split(""), (letter) ->
      $this.append "<span class=\"scrambled-letter\">" + letter + "</span>"

    $letters = $this.find(".scrambled-letter").not(".drag-clone")
  
  # Function to surround all letters in spacers
  insertSpacers = ->
    $this.find(".spacer").remove()
    $letters.before(spacerHTML).last().after spacerHTML
    $spacers = $this.find(".spacer")
    return
  insertSpacers()
  
  # Function to return whatever the currently arranged word is    
  parseWord = ->
    word = ""
    $letters.each ->
      word += $(this).text().replace(/[^a-zA-Z]/g, "")
    word.toLowerCase()
  
  # Function to return whether the currently arranged letter sequence is the correct/unscrambled one  
  isCorrect = ->
    parseWord() is unscrambledWord.toLowerCase()

  # What happens when you mousedown/clickenhold on a letter
  $letters.on "mousedown", (e) ->
    e.stopPropagation();
    
    $thisLetter = $(this)
    thisLetterWidth = $thisLetter.outerWidth()
    thisLetterHeight = $thisLetter.outerHeight()
    $this.addClass "dragging"
    
    # Establish a clone of the currently selected letter and add it to the DOM
    $letterClone = $thisLetter.clone(false)
    $letterClone.insertBefore $thisLetter
    
    # If this is a "middle" letter (letters on both sides), one of the spacers needs to be specified as extra
    if $thisLetter.prevAll(".scrambled-letter").length > 0 and $thisLetter.nextAll(".scrambled-letter").length > 0
      $thisLetter.nextAll(".spacer").first().addClass "extra"
      
    # Hide the letter you clicked, because we're going to put the clone of it under the cursor as it moves
    $thisLetter.addClass "invisible"
    $letterClone.addClass "drag-clone"
        
    # Function to position the clone w/ the mouse
    moveLetterWithMouse = (e) ->
      $letterClone.css
        top: e.clientY - (thisLetterHeight * 0.5)
        left: e.clientX - (thisLetterWidth * 0.5)

    # Run the function once to place the letter clone wherever your cursor is when you clicked    
    moveLetterWithMouse e
    
    # Function to snap letter to place when letting go
    snapLetterToPlace = ->
      # Unhide the original letter (it should still be .invisible however)
      $thisLetter.show()
      
      # Add the .snap-to-place class to the clone (which will enable CSS transitions) and then change its position to line up w/ the real letter
      realLetterOffset = $thisLetter.offset()
      $letterClone.addClass("snap-to-place").css
        top: realLetterOffset.top
        left: realLetterOffset.left

      # Kill the clone, show the real one after the animation has enough time to finish
      setTimeout (->
        $letterClone.remove()
        $thisLetter.removeClass "invisible"
      ), 500

    # Function to drop tile into spacer
    dropIntoSpacer = ($thisSpacer) =>  
      # Move original letter <span> to right before the spacer being hovered over
      $thisLetter.show().addClass("invisible").insertBefore $thisSpacer
      
      # Re-establish the $letters object to use the new natural DOM order
      $letters = $this.find(".scrambled-letter").not(".drag-clone")
      
      # Delete and re-establish the spacers
      insertSpacers()
      snapLetterToPlace()
      
      # See if you got the word correct
      $this.trigger "unscrambled"  if isCorrect()

    # When you're dragging a tile, if you approach the edge of a letter tile, assume you're aiming for that side of it 
    $letters.not('.drag-clone').not('.invisible').mousemove( (e) ->
      $thisMouseMoveLetter = $(this)
      letterOffset = $thisMouseMoveLetter.offset()     
      leftOffset = e.offsetX || e.clientX - letterOffset.left
      letterWidth = $thisMouseMoveLetter.outerWidth()
      halfPoint = letterWidth / 2
      prevLetters = $thisLetter.prevAll('.scrambled-letter').not('.drag-clone').not('.invisible').length
      nextLetters = $thisLetter.nextAll('.scrambled-letter').not('.drag-clone').not('.invisible').length
      
      $spacers.filter('.hover').removeClass("hover")
      
      if prevLetters > 0 and leftOffset > 0 and leftOffset < halfPoint
        $thisMouseMoveLetter.prevAll('.spacer').not('.extra').first().addClass "hover"
      else if nextLetters > 0 and leftOffset < letterWidth and leftOffset > halfPoint
        $thisMouseMoveLetter.nextAll('.spacer').not('.extra').first().addClass "hover"
    
    ).mouseup(->
      # If you mouseup in such a circumstance, drop the tile
      $thisSpacer = $spacers.filter('.hover').first()
      dropIntoSpacer($thisSpacer) if $thisSpacer.length > 0
      
    ).mouseleave(->
      $spacers.filter('.hover').removeClass("hover")
    )


    $spacers.not('.extra').hover(->
    
      # When you hover over a spacer:
      $(this).addClass "hover" 
      
      # Hide the real letter (which was previously only .invisible) once you've hovered over a spacer
      # so that its empty placeholder will disappear and (seemingly) reappear wherever you hover
      $thisLetter.hide()
      
    , ->
      # When you exit hovering a spacer:
      $(this).removeClass "hover"
    ).mouseup ->
      
      # Mouseup function on spacer, triggers when you "let go" of the letter you're dragging
      $thisSpacer = $(this)
      
      dropIntoSpacer($thisSpacer)
            
      return

    # Also attach the mouse drag events to the whole body, so you can drag the letter anywhere and still see it  
    $("body").mousemove(moveLetterWithMouse).on "mouseup", ->
      if $this.hasClass("dragging") or $(".drag-clone").length > 0
        $("body").unbind "mousemove", moveLetterWithMouse
        $spacers.unbind "mousemove mouseover mouseout mouseenter mouseleave mouseup"
        $letters.unbind "mousemove mouseleave"
        snapLetterToPlace()
        $this.removeClass "dragging"
        
    $this.on "unscrambled", ->
      $this.addClass "solved"


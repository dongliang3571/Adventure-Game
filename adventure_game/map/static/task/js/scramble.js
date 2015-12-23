function callscramble() {
  $(".scramble").each(function() {
    var $letters, $spacers, $this, insertSpacers, isCorrect, parseWord, randomize, scrambledWord, spacerHTML, unscrambledWord;
    $this = $(this);
    $letters = $this.find(".scrambled-letter").not(".drag-clone");
    $spacers = $this.find(".spacer");
    unscrambledWord = $this.data("unscrambled");
    scrambledWord = $this.data("scrambled");
    spacerHTML = "<span class=\"spacer\"></span>";
    if ($letters.length === 0 && scrambledWord === undefined && unscrambledWord !== undefined) {
      randomize = function() {
        return 0.5 - Math.random();
      };
      while (true) {
        scrambledWord = unscrambledWord.split("").sort(randomize).join("");
        if (scrambledWord !== unscrambledWord) {
          break;
        }
      }
    }
    if (scrambledWord !== undefined && $letters.length === 0) {
      $.map(scrambledWord.split(""), function(letter) {
        return $this.append("<span class=\"scrambled-letter\">" + letter + "</span>");
      });
      $letters = $this.find(".scrambled-letter").not(".drag-clone");
    }
    insertSpacers = function() {
      $this.find(".spacer").remove();
      $letters.before(spacerHTML).last().after(spacerHTML);
      $spacers = $this.find(".spacer");
    };
    insertSpacers();
    parseWord = function() {
      var word;
      word = "";
      $letters.each(function() {
        return word += $(this).text().replace(/[^a-zA-Z]/g, "");
      });
      return word.toLowerCase();
    };
    isCorrect = function() {
      return parseWord() === unscrambledWord.toLowerCase();
    };
    return $letters.on("mousedown", function(e) {
      var $letterClone, $thisLetter, dropIntoSpacer, moveLetterWithMouse, snapLetterToPlace, thisLetterHeight, thisLetterWidth;
      e.stopPropagation();
      $thisLetter = $(this);
      thisLetterWidth = $thisLetter.outerWidth();
      thisLetterHeight = $thisLetter.outerHeight();
      $this.addClass("dragging");
      $letterClone = $thisLetter.clone(false);
      $letterClone.insertBefore($thisLetter);
      if ($thisLetter.prevAll(".scrambled-letter").length > 0 && $thisLetter.nextAll(".scrambled-letter").length > 0) {
        $thisLetter.nextAll(".spacer").first().addClass("extra");
      }
      $thisLetter.addClass("invisible");
      $letterClone.addClass("drag-clone");
      moveLetterWithMouse = function(e) {
        return $letterClone.css({
          top: e.clientY - (thisLetterHeight * 0.5),
          left: e.clientX - (thisLetterWidth * 0.5)
        });
      };
      moveLetterWithMouse(e);
      snapLetterToPlace = function() {
        var realLetterOffset;
        $thisLetter.show();
        realLetterOffset = $thisLetter.offset();
        $letterClone.addClass("snap-to-place").css({
          top: realLetterOffset.top,
          left: realLetterOffset.left
        });
        return setTimeout((function() {
          $letterClone.remove();
          return $thisLetter.removeClass("invisible");
        }), 500);
      };
      dropIntoSpacer = (function(_this) {
        return function($thisSpacer) {
          $thisLetter.show().addClass("invisible").insertBefore($thisSpacer);
          $letters = $this.find(".scrambled-letter").not(".drag-clone");
          insertSpacers();
          snapLetterToPlace();
          if (isCorrect()) {
            return $this.trigger("unscrambled");
          }
        };
      })(this);
      $letters.not('.drag-clone').not('.invisible').mousemove(function(e) {
        var $thisMouseMoveLetter, halfPoint, leftOffset, letterOffset, letterWidth, nextLetters, prevLetters;
        $thisMouseMoveLetter = $(this);
        letterOffset = $thisMouseMoveLetter.offset();
        leftOffset = e.offsetX || e.clientX - letterOffset.left;
        letterWidth = $thisMouseMoveLetter.outerWidth();
        halfPoint = letterWidth / 2;
        prevLetters = $thisLetter.prevAll('.scrambled-letter').not('.drag-clone').not('.invisible').length;
        nextLetters = $thisLetter.nextAll('.scrambled-letter').not('.drag-clone').not('.invisible').length;
        $spacers.filter('.hover').removeClass("hover");
        if (prevLetters > 0 && leftOffset > 0 && leftOffset < halfPoint) {
          return $thisMouseMoveLetter.prevAll('.spacer').not('.extra').first().addClass("hover");
        } else if (nextLetters > 0 && leftOffset < letterWidth && leftOffset > halfPoint) {
          return $thisMouseMoveLetter.nextAll('.spacer').not('.extra').first().addClass("hover");
        }
      }).mouseup(function() {
        var $thisSpacer;
        $thisSpacer = $spacers.filter('.hover').first();
        if ($thisSpacer.length > 0) {
          return dropIntoSpacer($thisSpacer);
        }
      }).mouseleave(function() {
        return $spacers.filter('.hover').removeClass("hover");
      });
      $spacers.not('.extra').hover(function() {
        $(this).addClass("hover");
        return $thisLetter.hide();
      }, function() {
        return $(this).removeClass("hover");
      }).mouseup(function() {
        var $thisSpacer;
        $thisSpacer = $(this);
        dropIntoSpacer($thisSpacer);
      });
      $("body").mousemove(moveLetterWithMouse).on("mouseup", function() {
        if ($this.hasClass("dragging") || $(".drag-clone").length > 0) {
          $("body").unbind("mousemove", moveLetterWithMouse);
          $spacers.unbind("mousemove mouseover mouseout mouseenter mouseleave mouseup");
          $letters.unbind("mousemove mouseleave");
          snapLetterToPlace();
          return $this.removeClass("dragging");
        }
      });
      return $this.on("unscrambled", function() {
        return $this.addClass("solved");
      });
    });
  });

}

$(function(){
  $sbutton = $("#scramble");
  $show_game = $("#game");

  $sbutton.on("click", function(){
    $.ajax({
      type: 'GET',
      url: '/adventure/special_game_json',
      success: function(data) {
        var game = data.special_game;
        $show_game.html(game);
        callscramble();
      },

      error: function(){

      }
    });
  });

  $sbutton.click();
});

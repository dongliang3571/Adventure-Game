$(function(){
  $infobutton = $("#information");
  $window = $("#window");
  $space = $(".space2")



  var information = "<h2>HELP THE WIZARD</h2>"

  $infobutton.on("click", function(){
    window_class = $window.attr("class")
    if (window_class == "space") {
      $window.attr("class","window");
      $infobutton.text("information <<");
      $.ajax({
        type: 'GET',
        url: '/get_adventure_detail',
        success: function(data) {
          $.each(data, function(i, da) {
            $window.html(da.name);
          });


        }
      });
    }
    else{
      $window.attr("class","space");
      $infobutton.text("information >>");
      $window.html("");
    }
  });
});

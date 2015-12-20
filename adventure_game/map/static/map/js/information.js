$(function(){
  $infobutton = $("#information");
  $window = $("#window");
  $space = $(".space2")





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

            var information = "<h2>" + da.name + "</h2>" +
                              "<h3 style='color: red;'>Items needed:</h3>" +
                              "<p style='font-size: 1.5em;'>{{ items_needed }}</p>" +
                              "<h3 style='color: red;'>Expenses:</h3>" +
                              "<p style='font-size: 1.5em;'>{{ expenses }}</p>" +
                              "<h3 style='color: red;'>Locations:</h3>" +
                              "<p style='font-size: 1.5em;'>{{ locations }}</p>";

            $window.html(information);
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

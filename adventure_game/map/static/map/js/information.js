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

            var information = "<h2 style='color:blue;margin-left: 30px;'>" + da.name + "</h2>" +
                              "<h3 style='color: red;margin-left: 30px;'>Items needed:</h3>" +
                              "<p style='font-size: 1.5em;margin-left: 30px;'>" + da.items + "</p>" +
                              "<h3 style='color: red;margin-left: 30px;'>Expenses:</h3>" +
                              "<p style='font-size: 1.5em;margin-left: 30px;'>" + da.expenses + "</p>" +
                              "<h3 style='color: red;margin-left: 30px;'>Locations:</h3>" +
                              "<p style='font-size: 1.5em;margin-left: 30px;font-family:Monaco, monospace;'>" + da.locations + "</p>" +
                              "<iframe style='margin-left: 50px;margin-left: 50px;border-radius: 25px;' src=" + da.mapaddress + " width='500' height='400' frameborder='0' style='border:0' allowfullscreen></iframe>" +
                              "<img style='float:right; margin-right: 150px;width:270px;' src=" + da.theme_character_url + " class='img-responsive'>";
                              // "<img style='float:right; margin-right: 150px;width:270px;' src='https://pixabay.com/static/uploads/photo/2012/04/12/13/12/devil-29973_960_720.png' class='img-responsive'>";

            $window.html(information);
          });
        },
        error: function(){
          $window.html("<p style='color: red;margin-left: 30px;'>Failed to retrived data, check your internet connection.</p>");
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

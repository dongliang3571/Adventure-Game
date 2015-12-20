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
                              "<p style='font-size: 1.5em;margin-left: 30px;'>" + da.locations + "</p>" +
                              "<iframe style='margin-left: 50px;margin-left: 50px;border-radius: 25px;' src=" + da.mapaddress + " width='500' height='400' frameborder='0' style='border:0' allowfullscreen></iframe>" +
                              "<img style='float:right; margin-right: 150px;width:270px;' src='http://vignette3.wikia.nocookie.net/scribblenauts/images/f/fc/Wizard_Male.png/revision/latest?cb=20130215182314' class='img-responsive'>";

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

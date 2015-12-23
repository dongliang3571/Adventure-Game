$(function (){
  var $myjson = $('#json');
  $.ajax({
    type: 'GET',
    url: '/getjson',
    success: function(data) {
      $.each(data, function(i, da) {
        $myjson.append('<li>{{ usea }}people   '+da.people+' age '+da.age+'</li>');
      });


    }
  });

});

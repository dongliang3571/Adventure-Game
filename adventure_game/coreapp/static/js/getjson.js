$(function (){
  var $myjson = $('#json');
  final ="";
  sfinal = "";
  function getMessage(){
    $.ajax({
      type: 'GET',
      url: '/getmessage',
      success: function(data) {
        $.each(data, function(i, da) {
          final = final + da.message;

          sfinal = final;
        });

        $myjson.text(final);
        final = "";

      }
    });
  }

  setInterval(getMessage, 10);
});


// var canvas_girl = document.getElementById("girl");

var canvas_tree = document.getElementById("env");
canvas_tree.width = 120;
canvas_tree.height = 150;
var canvas_tem = document.getElementsByClassName("boy");
var canvas_boy = canvas_tem[0];
canvas_boy.width=80;
canvas_boy.height=80;
var count=0;

// var female = new Image();
var male = new Image();
var tree = new Image();
// var grand_terminal = new Image();
// var empire_building = new Image();
// var metropolitan_museum = new Image();
// var statue_liberty = new Image();
// var central_park = new Image();
// var number1 = new Image();
// var number2 = new Image();
// var number3 = new Image();
// var number4 = new Image();
// var number5 = new Image();

// female.src = "../static/map/images/characters/girl2.png";
male.src="../static/map/images/characters/boy_sprite.png";
tree.src="http://i444.photobucket.com/albums/qq168/grandmadeb_rmvx/Shareable%20Artists/BenBen%20CONFIRMED/BenBen%20Trees%20Seasonal_zps6pwibcy7.png";

// grand_terminal.src="../static/map/images/buildings/grand.png";
// empire_building.src="../static/map/images/buildings/Empire_State_Building.png";
// metropolitan_museum.src="../static/map/images/buildings/metropolitan.png";
// statue_liberty.src="../static/map/images/buildings/statue_liberty.png";
// central_park.src="../static/map/images/buildings/central.png";
//
// number1.src="../static/map/images/numbers/number1.png"
// number2.src="../static/map/images/numbers/number2.png"
// number3.src="../static/map/images/numbers/number3.png"
// number4.src="../static/map/images/numbers/number4.png"
// number5.src="../static/map/images/numbers/number5.png"

var ticksPerFrame = 10;
var frameIndex_girl = 0;
var frameIndex_boy = 6;
var numberOfFrames_girl = 3;
var numberOfFrames_boy = frameIndex_boy+2;
var tickCount = 0;

function sprite(options) {

    var that = {};

    that.context = options.context;
    that.width = options.width;
    that.height = options.height;
    that.image = options.image;
    that.frameIndex = options.frameIndex;

    that.render = function() {
      that.context.clearRect(0, 0, that.width, that.height);

       // Draw the animation
       that.context.drawImage(
          that.image,
          that.frameIndex * that.width,
          // that.frameIndex * that.height,
          0,
          that.width,
          that.height,
          0,
          0,
          that.width-20,
          that.height-20);


   };

   that.render_static = function(x,y,j,k){
     that.context.drawImage(that.image,0,0,x,y,0,0,j,k);
   };

  //  that.update = function () {
  //   //  canvas.width = window.innerWidth;
  //   //  canvas.height = window.innerHeight;
   //
  //       tickCount += 1;
   //
  //       if (tickCount > ticksPerFrame) {
  //         tickCount = 0;
  //         frameIndex += 1;
  //         if (frameIndex >= numberOfFrames) {
  //           frameIndex = 0;
  //         }
  //       }
  //     };


    return that;
}



// var female_sprite = sprite({
//     context: canvas_girl.getContext("2d"),
//     width: 32,
//     height: 48,
//     image: female,
//     frameIndex: frameIndex_girl
// });

var male_sprite = sprite({
    context: canvas_boy.getContext("2d"),
    width:  96,
    height: 96,
    image: male,
    frameIndex: frameIndex_boy
});

var tree_sprite = sprite({
    context: canvas_tree.getContext("2d"),
    width: 768,
    height: 768,
    image: tree,
    frameIndex:0
});
//
// var empire_building_sprite = sprite({
//     context: canvas.getContext("2d"),
//     width: 32,
//     height: 48,
//     image: empire_building
// });
//
// var metropolitan_museum_sprite = sprite({
//     context: canvas.getContext("2d"),
//     width: 32,
//     height: 48,
//     image: metropolitan_museum
// });
//
// var statue_liberty_sprite = sprite({
//     context: canvas.getContext("2d"),
//     width: 32,
//     height: 48,
//     image: statue_liberty
// });
//
// var central_park_sprite = sprite({
//     context: canvas.getContext("2d"),
//     width: 32,
//     height: 48,
//     image: central_park
// });
//
// var number1_sprite = sprite({
//     context: canvas.getContext("2d"),
//     width: 256,
//     height: 256,
//     image: number1
// });
//
// var number2_sprite = sprite({
//     context: canvas.getContext("2d"),
//     width: 256,
//     height: 256,
//     image: number2
// });
//
// var number3_sprite = sprite({
//     context: canvas.getContext("2d"),
//     width: 256,
//     height: 256,
//     image: number3
// });
//
// var number4_sprite = sprite({
//     context: canvas.getContext("2d"),
//     width: 256,
//     height: 256,
//     image: number4
// });
//
// var number5_sprite = sprite({
//     context: canvas.getContext("2d"),
//     width: 256,
//     height: 256,
//     image: number5
// });

// function draw(){
//   number1_sprite.render_number(300,500);
//   number2_sprite.render_number(400,450);
//   number3_sprite.render_number(400,450);
//   number4_sprite.render_number(400,450);
//   number5_sprite.render_number(400,450);
// }

// function update(){
//   female_sprite.update();
//   // male_sprite.update();
//
// }
function render_tree(){
  tree_sprite.render_static(200,310,100,150);
}
function render_boy(){
  male_sprite.render();
  male_sprite.frameIndex +=1;
  if (male_sprite.frameIndex > numberOfFrames_boy) {
    male_sprite.frameIndex=frameIndex_boy;
  }
}
// setInterval(render_girl, 250);
// $(function(){
//   $('#next').on('click',function(){
//     $('#path4').append(" <b>Appended text</b>.");
//   })
// });
$(document).on('keypress', function(e) {
    if(e.KeyCode == 13) {
        alert('You pressed enter!');
    }
});


// $(document).ready(function(){
//     $("#next").click(function(){
//       count=count+1;
//       if (count>4) {
//         count=4;
//       }
//       if (count==1) {
//         $("#boy").attr('class','boy boy1');
//       }
//       else if(count==2){
//         $("#boy").attr('class','boy boy1 boy2');
//       }
//       else if(count==3){
//         $("#boy").attr('class','boy boy1 boy2 boy3');
//       }
//       else if(count==4){
//         $("#boy").attr('class','boy boy1 boy2 boy3 boy4');
//       }
//
//
//     });
//
//     $("#previous").click(function(){
//       count=count-1;
//       if (count<0) {
//         count=0;
//       }
//       if (count==3) {
//         $("#boy").attr('class','boy boy1 boy2 boy3');
//       }
//       else if(count==2){
//         $("#boy").attr('class','boy boy1 boy2');
//       }
//       else if (count==1) {
//         $("#boy").attr('class','boy boy1');
//       }
//       else if (count==0) {
//         $("#boy").attr('class','boy');
//       }
//     });
// });

$(function() {
  setInterval(render_boy,250);
  setInterval(render_tree,10);

});
// function gameLoop () {
  // update();
  // female.addEventListener("load",render());
  // draw();

  // window.requestAnimationFrame(gameLoop);
// }




// number1.addEventListener("load", gameLoop);

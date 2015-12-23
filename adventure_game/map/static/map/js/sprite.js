
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

male.src="http://i.imgur.com/BoJpt3z.png";
tree.src="http://i444.photobucket.com/albums/qq168/grandmadeb_rmvx/Shareable%20Artists/BenBen%20CONFIRMED/BenBen%20Trees%20Seasonal_zps6pwibcy7.png";


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

    return that;
}


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

$(document).on('keypress', function(e) {
    if(e.KeyCode == 13) {
        alert('You pressed enter!');
    }
});




$(function() {
  setInterval(render_boy,250);
  setInterval(render_tree,10);

});

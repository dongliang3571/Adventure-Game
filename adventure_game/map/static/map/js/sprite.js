var canvas = document.getElementById("coinAnimation");
var female = new Image();
var male = new Image();
var grand_terminal = new Image();
var empire_building = new Image();
var metropolitan_museum = new Image();
var statue_liberty = new Image();
var central_park = new Image();
var number1 = new Image();
var number2 = new Image();
var number3 = new Image();
var number4 = new Image();
var number5 = new Image();

female.src = "static/images/characters/girl2.png";
male.src="static/images/characters/boy_sprite.png";

grand_terminal.src="static/images/buildings/grand.png";
empire_building.src="static/images/buildings/Empire_State_Building.png";
metropolitan_museum.src="static/images/buildings/metropolitan.png";
statue_liberty.src="static/images/buildings/statue_liberty.png";
central_park.src="static/images/buildings/central.png";

number1.src="static/images/numbers/number1.png"
number2.src="static/images/numbers/number2.png"
number3.src="static/images/numbers/number3.png"
number4.src="static/images/numbers/number4.png"
number5.src="static/images/numbers/number5.png"

var ticksPerFrame = 10;
var numberOfFrames = 4;
var frameIndex = 0;
var tickCount = 0;

function sprite(options) {

    var that = {};

    that.context = options.context;
    that.width = options.width;
    that.height = options.height;
    that.image = options.image;

    that.render = function() {
      that.context.clearRect(0, 0, that.width, that.height);

       // Draw the animation
       that.context.drawImage(
          that.image,
          frameIndex * that.width,
          0,
          that.width,
          that.height,
          0,
          0,
          that.width,
          that.height);

   };

   that.render_number = function(x,y){
     that.context.drawImage(that.image,0,0,that.width,that.height,x,y,50,50);
   };

   that.update = function () {
     canvas.width = window.innerWidth;
     canvas.height = window.innerHeight;

        tickCount += 1;

        if (tickCount > ticksPerFrame) {
          tickCount = 0;
          frameIndex += 1;
          if (frameIndex >= numberOfFrames) {
            frameIndex = 0;
          }
        }
      };


    return that;
}



var female_sprite = sprite({
    context: canvas.getContext("2d"),
    width: 32,
    height: 48,
    image: female
});

var male_sprite = sprite({
    context: canvas.getContext("2d"),
    width: 32,
    height: 48,
    image: male
});

var grand_terminal_sprite = sprite({
    context: canvas.getContext("2d"),
    width: 32,
    height: 48,
    image: grand_terminal
});

var empire_building_sprite = sprite({
    context: canvas.getContext("2d"),
    width: 32,
    height: 48,
    image: empire_building
});

var metropolitan_museum_sprite = sprite({
    context: canvas.getContext("2d"),
    width: 32,
    height: 48,
    image: metropolitan_museum
});

var statue_liberty_sprite = sprite({
    context: canvas.getContext("2d"),
    width: 32,
    height: 48,
    image: statue_liberty
});

var central_park_sprite = sprite({
    context: canvas.getContext("2d"),
    width: 32,
    height: 48,
    image: central_park
});

var number1_sprite = sprite({
    context: canvas.getContext("2d"),
    width: 256,
    height: 256,
    image: number1
});

var number2_sprite = sprite({
    context: canvas.getContext("2d"),
    width: 256,
    height: 256,
    image: number2
});

var number3_sprite = sprite({
    context: canvas.getContext("2d"),
    width: 256,
    height: 256,
    image: number3
});

var number4_sprite = sprite({
    context: canvas.getContext("2d"),
    width: 256,
    height: 256,
    image: number4
});

var number5_sprite = sprite({
    context: canvas.getContext("2d"),
    width: 256,
    height: 256,
    image: number5
});

function draw(){
  number1_sprite.render_number(300,500);
  number2_sprite.render_number(400,450);
  number3_sprite.render_number(400,450);
  number4_sprite.render_number(400,450);
  number5_sprite.render_number(400,450);
}

function update(){
  female_sprite.update();
  // male_sprite.update();

}
function render(){
  female_sprite.render();
  // male_sprite.render();
}

function gameLoop () {
  update();
  // render();
  // draw();
  // window.requestAnimationFrame(gameLoop);

}



number1.addEventListener("load", gameLoop);

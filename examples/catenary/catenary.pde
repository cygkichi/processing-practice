import gifAnimation.*;
GifMaker gifExport;

float a;

void setup()
{
  frameRate(60);
  size(1000, 1000);
  gifExport = new GifMaker(this, "catenary.gif");
  gifExport.setRepeat(0);
  gifExport.setQuality(10);
  gifExport.setDelay(200);
}

void draw()
{
  int i;
  background(255);
  for(i=0; i<100; i++){
    draw_catenary(random(1000),sq(random(30)),-random(30)-20);
  }
  // GIF
  if(frameCount <= 20){
    gifExport.addFrame();
  } else {
    gifExport.finish();
  }
}

void draw_catenary(float x, float y, float a){
  int i;
  float x0,x1,y0,y1;
  fill(255, 255, 0);
  x0 = 0;
  y0 = a*cosh((x0-x)/a) + y;
  for(i=1; i<1000; i++){
    x1 = i;
    y1 = a*cosh((x0-x)/a) + y;
    line(x0,y0,x1,y1);
    x0 = x1;
    y0 = y1;
  }
  endShape(CLOSE);
}

float cosh(float x){
  return (exp(x)+exp(-x))/2;
}

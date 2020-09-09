import gifAnimation.*;
GifMaker gifExport;

boolean MAKEGIF = true;


int xsize = 1000;
int ysize = 1000;
int r     = 425;

color bg_color     = #faf3dd;
color circle_color = #ffbb91;
color rect_color   = #64958f;
color line_color   = #065c6f;
color pi_color     = #ff0900;
color line_width = 2;
color unit = 50;
//ffbb91

int n = 100;
float[] xs       = new float[n];
float[] nhit  = new float[n];
float[] nmiss = new float[n];


void setup()
{ 
  frameRate(60);
  size(1000, 1000);
  if(MAKEGIF){
    gifExport = new GifMaker(this, "pi.gif");
    gifExport.setRepeat(0);
    gifExport.setQuality(10);
    gifExport.setDelay(200);
  }
  int i;
  float dx = float(2*r)/float(n-1); 
  for(i=0; i<n; i++){
    nhit[i]  = 0;
    nmiss[i] = 0;
    xs[i] = i*dx;
  }
  
}

void draw()
{
  int i;
  float x0, y0;
  background(bg_color);
  noStroke();
  fill(rect_color);
  rect(xsize/2-r,ysize/2-r,2*r,r);
  fill(circle_color);
  arc(xsize/2, ysize/2, 2*r, 2*r, PI, TWO_PI);

  strokeWeight(line_width);
  stroke(pi_color);
  x0 = xsize/2-r;
  y0 = ysize/2+r;
  line(x0, y0-PI*unit, x0+2*r, y0-PI*unit); //PI-value
  stroke(line_color);
  line(x0, y0, x0+2*r, y0); //x-axis
  line(x0, y0, x0, y0+ysize/2-2*r);   //y-axis
  stroke(rect_color);
  for(i=0;i<n-1;i++){
    line(x0+xs[i  ], y0-4*nhit[i  ]/(nhit[i  ]+nmiss[i  ])*unit,
         x0+xs[i+1], y0-4*nhit[i+1]/(nhit[i+1]+nmiss[i+1])*unit); //x-axis
  }  

  // sift (except n-1)
  for(i=0;i<n-1; i++){
    nhit[i]  = nhit[i+1];
    nmiss[i] = nmiss[i+1];
  }
  //calc pi
  float x,y;
  x = random(2) - 1;
  y = random(1);
  circle(xsize/2+x*r,ysize/2-y*r,10);
  if(x*x+y*y<1){
    nhit[n-1] ++ ;
  }else{
    nmiss[n-1] ++ ;
  }

  if(MAKEGIF){
    if(frameCount <= 200){
      gifExport.addFrame();
    } else {
      gifExport.finish();
    }
  }
}

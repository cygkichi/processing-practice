import gifAnimation.*;
GifMaker gifExport;

int N = 1000;
int xsize = 1000;
int y1size = 800;
int y2size = 200;
int ysize = y1size + y2size;

float alpha = 0.45;
float dx = float(xsize) / float(N);
float[] x = new float[N];
float[] u = new float[N];
float[] du = new float[N];

boolean[] is_top    = new boolean[N];
boolean[] is_bottom = new boolean[N];

int np = 1000000;
int ip = 0;
float[] px = new float[np];
float[] py = new float[np];

int istep=0;
void setup()
{
  frameRate(60);
  size(1000, 1000);
  int i,j;
  for(i=0; i<N; i++){
    x[i] = i*dx;
    u[i] = random(y2size*2) - y2size*0.5;
  }
  gifExport = new GifMaker(this, "scalespace.gif");
  gifExport.setRepeat(0);
  gifExport.setQuality(10);
  gifExport.setDelay(20);
}

void draw()
{
  background(color(242,235,209));
  line(0,y1size,xsize,y1size);
  int i;
  for(i=0; i<N-1; i++){
    line(x[i], ysize-u[i], x[i+1], ysize-u[i+1]);
  }
  line(x[N-1], ysize-u[N-1], x[N-1]+dx, ysize-u[0]);

  // calc top and bottom
  float du0, du1;
  for(i=0;i<N;i++){
    if(i==0){
      du0 = u[  i] - u[N-1];
      du1 = u[i+1] - u[  i];
    }else if(i==N-1){
      du0 = u[  i] - u[i-1];
      du1 = u[  0] - u[  i];
    }else{
      du0 = u[  i] - u[i-1];
      du1 = u[i+1] - u[  i];
    }    
    if(du0>0 && du1<0){
      is_top[i] = true;
    }else{
      is_top[i] = false;
    }
    if(du0<0 && du1>0){
      is_bottom[i] = true;
    }else{
      is_bottom[i] = false;
    }
  }
  for(i=0;i<N; i++){
    if(is_top[i]){
      fill(color(255, 204, 0));
      circle(x[i], ysize-u[i],10);
      px[ip] = x[i];
      py[ip] = istep;
      ip++;
    }
    if(is_bottom[i]){
      fill(color(0, 204, 255));
      circle(x[i], ysize-u[i],10);
      px[ip] = x[i];
      py[ip] = istep;
      ip++;
    } 
  }
  
  // time step
  du[0]   = alpha*(u[1]-2*u[  0]+u[N-1]);
  du[N-1] = alpha*(u[0]-2*u[N-1]+u[N-2]);
  for(i=1; i<N-1; i++){
    du[i] = alpha*(u[i+1]-2*u[i]+u[i-1]);
  }
  for(i=0; i<N; i++){
    u[i] = u[i] + du[i];
  }
  
  //plot point
  for(i=0; i<ip; i++){
    point(px[i], y1size-py[i]);
  }
  for(i=0;i<N; i++){
    if(is_top[i]){
      fill(color(255, 204, 0));
      circle(x[i], y1size-istep,10);
    }
    if(is_bottom[i]){
      fill(color(0, 204, 255));
      circle(x[i], y1size-istep,10);
    } 
  }  

  // GIF
  if(istep%5==0){
    if(frameCount <= 60*15){
      gifExport.addFrame();
    } else {
      gifExport.finish();
    }
  }
  istep++;  
}

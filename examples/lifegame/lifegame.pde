import gifAnimation.*;
GifMaker gifExport;

int nx = 100;
int ny = 100;

int cell_size = 10;
boolean is_move = true; 
boolean is_debug = false;
boolean[][] state = new boolean[nx][ny];
boolean[] rule = new boolean[8];


void setup()
{
  frameRate(60);
  size(1000, 1000);
  int i, j;
  for(i=0; i<nx; i++)
    for(j=0; j<ny; j++)
      state[i][j] = boolean(int(random(2)));  

  gifExport = new GifMaker(this, "lifegame.gif");
  gifExport.setRepeat(0);
  gifExport.setQuality(10);
  gifExport.setDelay(20);
}

void draw()
{
  background(255);
  int i, j, x, y;
  // draw
  noStroke();
  for(i=0; i<nx; i++){
    x = i*cell_size;
    for(j=0; j<ny; j++){
      y = j*cell_size;
      if(state[i][j]){
        fill(color(236,6,3));
      }else{
        fill(color(13,253,253));
      }
      rect(x,y,cell_size,cell_size);
      
      //debug text
      if(is_debug){
        int tx,ty;
        fill(color(0,0,0,0));
        tx = x ; 
        ty = y + cell_size / 2;
        text(str(state[i][j]),tx,ty);
      }
    }
  }
  
  // count and change
  // draw
  if(is_move){
    boolean[][] next_state = new boolean[nx][ny];
    for(i=0; i<nx; i++){
      for(j=0; j<ny; j++){
        int ip,im,jp,jm; //(i,j)(plus,minus)
        ip = (i==nx-1) ? 0    : i+1;
        im = (i==0   ) ? nx-1 : i-1;
        jp = (j==ny-1) ? 0    : j+1;
        jm = (j==0   ) ? ny-1 : j-1;
        int counter = 0;
        counter += int(state[ip][jp]);
        counter += int(state[ip][j ]);
        counter += int(state[ip][jm]);
        counter += int(state[i ][jp]);
        counter += int(state[i ][jm]);
        counter += int(state[im][jp]);
        counter += int(state[im][j ]);
        counter += int(state[im][jm]);

        //debug text  
        if(is_debug){
          int tx,ty;
          fill(color(0,0,0,0));
          x = i*cell_size;
          y = j*cell_size;
          tx = x ; 
          ty = y + cell_size / 2;
          text(str(counter),tx,ty+15);
        }       
        if(state[i][j]){
          if(counter == 2 || counter ==3 ){
            next_state[i][j] = true;
          }else{
            next_state[i][j] = false;
          }
        }else{
          if(counter == 3 ){
            next_state[i][j] = true;
          }else{
            next_state[i][j] = false;
          }
        }
      }
    }
    for(i=0; i<nx; i++){
      for(j=0; j<ny; j++){
          state[i][j] = next_state[i][j];
      }
    }
  }
  // GIF
  if(frameCount <= 60*3){
    gifExport.addFrame();
  } else {
    gifExport.finish();
  }
}

void mousePressed() 
{ 
  switch(mouseButton){
    case LEFT:
      int xindex, yindex;
      xindex = int(mouseX/cell_size);
      yindex = int(mouseY/cell_size);
      state[xindex][yindex] = state[xindex][yindex]?false:true;
      break;
    case RIGHT:
      is_move = is_move?false:true;
      break;
  }
} 

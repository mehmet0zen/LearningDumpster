int _width = 20, _height = 20;
int offsetX = 0, offsetY = 0;
int current = 0;
float x, y;
float[] xCordinates = new float[640000];
float[] yCordinates = new float[640000];

void setup() {
  size(800, 800);
  background(0);
}

void draw() {
  
  if (mouseButton != 0) {
    x = _width * round((mouseX - offsetX) / (_width + offsetX));
    y = _height * round((mouseY - offsetY) / (_height + offsetY));
    xCordinates[current] = x;
    yCordinates[current] = y;
    rect(x, y, _width, _height);
    current++;
   } 
   else if (mouseButton == 0) {
     for(int i = 0; i < current; i++) {
        rect(xCordinates[i], yCordinates[i], 20, 20);
        fill(random(0, 255), random(0,255), 20, 10);
     }
     noCursor();
     fill(mouseX, mouseY, 20, 40);
   }
  
}

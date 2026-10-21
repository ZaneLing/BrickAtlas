#include <math.h>
#include <stdint.h>
/* Orthographic, double-sided triangle rasterization with a real depth buffer. */
void raster(int n, const float *tri, const unsigned char *colors, const int *ids,
            int w,int h,unsigned char *rgb,float *depth,int *labels) {
 for(int t=0;t<n;t++) {
  const float *p=tri+9*t;
  float area=(p[3]-p[0])*(p[7]-p[1])-(p[4]-p[1])*(p[6]-p[0]);
  if(fabsf(area)<1e-6f)continue;
  int x0=fmaxf(0,floorf(fminf(p[0],fminf(p[3],p[6]))));
  int x1=fminf(w-1,ceilf(fmaxf(p[0],fmaxf(p[3],p[6]))));
  int y0=fmaxf(0,floorf(fminf(p[1],fminf(p[4],p[7]))));
  int y1=fminf(h-1,ceilf(fmaxf(p[1],fmaxf(p[4],p[7]))));
  for(int y=y0;y<=y1;y++)for(int x=x0;x<=x1;x++) {
   float px=x+.5f,py=y+.5f;
   float b=((px-p[0])*(p[7]-p[1])-(py-p[1])*(p[6]-p[0]))/area;
   float c=((p[3]-p[0])*(py-p[1])-(p[4]-p[1])*(px-p[0]))/area;
   float a=1-b-c;
   if(a < -1e-5f || b < -1e-5f || c < -1e-5f)continue;
   float z=a*p[2]+b*p[5]+c*p[8];int i=y*w+x;
   if(z>depth[i]+1e-5f) {
    depth[i]=z;labels[i]=ids[t];
    for(int k=0;k<3;k++)rgb[3*i+k]=colors[3*t+k];
   }
  }
 }
}

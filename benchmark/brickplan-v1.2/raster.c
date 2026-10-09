#include <math.h>
#include <stdint.h>
/* Orthographic triangle z-buffer. Larger z faces the camera. */
void raster(int n, const float *v, const uint8_t *colors,
            int w, int h, float *depth, uint8_t *rgb, int *owner,
            const int *ids) {
  for (int t=0;t<n;t++) {
    const float *a=v+9*t,*b=a+3,*c=a+6;
    float den=(b[1]-c[1])*(a[0]-c[0])+(c[0]-b[0])*(a[1]-c[1]);
    if (fabsf(den)<1e-8f) continue;
    int x0=fmaxf(0,floorf(fminf(a[0],fminf(b[0],c[0]))));
    int x1=fminf(w-1,ceilf(fmaxf(a[0],fmaxf(b[0],c[0]))));
    int y0=fmaxf(0,floorf(fminf(a[1],fminf(b[1],c[1]))));
    int y1=fminf(h-1,ceilf(fmaxf(a[1],fmaxf(b[1],c[1]))));
    for(int y=y0;y<=y1;y++) for(int x=x0;x<=x1;x++) {
      float u=((b[1]-c[1])*(x+.5f-c[0])+(c[0]-b[0])*(y+.5f-c[1]))/den;
      float q=((c[1]-a[1])*(x+.5f-c[0])+(a[0]-c[0])*(y+.5f-c[1]))/den;
      float r=1-u-q;
      if(u<0 || q<0 || r<0) continue;
      float z=u*a[2]+q*b[2]+r*c[2];
      int k=y*w+x;
      if(z>depth[k]) {
        depth[k]=z; owner[k]=ids[t];
        for(int ch=0;ch<3;ch++) rgb[3*k+ch]=colors[3*t+ch];
      }
    }
  }
}

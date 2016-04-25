#include <proj_api.h>

#include <stdio.h>

int main(int argc, char **argv) {
  projPJ pj_merc, pj_latlong;
  double x = 20, y = 30;

  if (!(pj_merc = pj_init_plus("+proj=merc +ellps=clrk66 +lat_ts=33")) )
    exit(1);
  if (!(pj_latlong = pj_init_plus("+proj=latlong +ellps=clrk66")) )
    exit(1);
  //while (scanf("%lf %lf", &x, &y) == 2) {
    x *= DEG_TO_RAD;
    y *= DEG_TO_RAD;
    pj_transform(pj_latlong, pj_merc, 1, 1, &x, &y, NULL );
    printf("%.2f\t%.2f\n", x, y);
  //}
  exit(0);
}

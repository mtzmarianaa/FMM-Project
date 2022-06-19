#pragma once

typedef struct coord coordS;

void coord_alloc(coordS **coordinates );

void coord_dealloc(coordS **coordinates);

void coord_init(coordS *coordinates, double *x, double *y, int nPoints);

void print_coord(coordS *coordinates);
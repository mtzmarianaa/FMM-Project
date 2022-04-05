/*
FMM (Fast Marching Method) naive implementation in 2D
Following (kind of) the idea of Dijkstra's algorithm 
which I also implemented.
 */

#include <stdio.h>
#include <stdlib.h>
#include <math.h>

void FMM_2D( double x_min, double x_max, double y_min, double y_max, int start[2], double distance[M*N], int M, int N);

double speed(double x, double y);

void printQGridFromQueue(int Q[M*N]);

void printGridFromDistance(double distance[M*N]);

int main(){
	int M = 5, N = 5;

    double x_min, x_max, y_min, y_max;
    int start[2];
    x_min = 0.0;
    x_max = 10.0;
    y_min = 0.0;
    y_max = 10.0;
    start[0] = 2;
    start[1] = 2;

	double *distance = malloc(M*N*sizeof(double));
	if (distance == NULL) {
		printf("oh no!\n");
		exit(EXIT_FAILURE);
	}

    FMM_2D( x_min, x_max, y_min, y_max, start, distance, M, N);

	free(distance);

    return EXIT_SUCCESS;
}

double speed(double x, double y){
    /*
    Function that defines the 1/f function used in the eikonal equation |u| = 1/f
    */
    return 1.0;
}

void printQGridFromQueue(int Q[M*N]){
    for(int i = N-1; i>-1; i --){
        for(int j = 0; j<M; j++){
            printf("%d ", Q[i*N + j] );
        }
        printf("\n");
    }
    printf("\n");
}

void printGridFromDistance(double distance[M*N]){
    for(int i = N-1; i>-1; i --){
        for(int j = 0; j<M; j++){
            printf("%fl ", distance[i*N + j] );
        }
        printf("\n");
    }
    printf("\n");
}


void FMM_2D( double x_min, double x_max, double y_min, double y_max, int start[2], double *distance, int M, int N){
    /*
     Naive implementation of the fast marching method in a 2D grid. In the priority queue:
         - 0: far
         1: trial
         2: valid
     Hence the objective is to have the priority queue with just 2's. 
     IN:  x_min : from where in the x direction
             - x_max : to where in the x direction
             - y_min : from where in the y direction
             - y_max : to where in the y direction
             - start : two coordinates (from 0 to M-1 and from 0 to N-1) on where to start
        
    Now this is a 2D grid and we're going to "flatten" it in the row by row way, starting from the top and moving all the way 
    to the bottom (from southwst to northeast). Hence our vector is going to be a MxN vector (which represents the grid)
    */
   // INITIALIZATION PART
     // alive points (the starting point(s)), trial points (narrow band points), and far away points
     int Q[M*N], i, j, next_valid, coordinate;
     double minDistance, x_linspace[N], y_linspace[M], h_x, h_y;

     // stepsize in x direction is h_x, stepsize in y direction is h_y
     h_x = (x_max - x_min)/N;
     h_y = (y_max - y_min)/N;

     // Start the linspace in the x and y directions
     for(i = 0; i<N; i++){
         x_linspace[i] = x_min + i*h_x;
     }
     for(i = 0; i<M; i++){
         y_linspace[i] = y_min + i*h_y;
     }
    // Initialize the queue and the distances with infinity
     for (i = 0; i< M*N; i++)
     {
         Q[i] = 0;
         distance[i] = INFINITY;
     }


     // Add the starting point
     Q[start[0]*N + start[1] ] = 2;
     distance[start[0]*N + start[1] ] = 0;

     // Initialize the points that are connected to that starting point (at most 4 points are connected to this starting point)
     // We need to know if we have all those 4 points or now (we don't want -1 as an index)
     // We also know that these are the only connected points to our start point so we can initialize here
     // the distance of those points.
     if (start[0] !=0  ){ // we're not in the most southern part, we do have a neighbour south
         Q[N*(start[0]-1) + start[1] ] = 1;
         distance[N*(start[0]-1) + start[1] ] = speed( x_linspace[start[0]], y_linspace[start[1]]-1 )*h_y;
     }
     if ( start[1] != 0 ){ // we're not in a west edge, we can have a neighbour to the left
         Q[ N*start[0] + start[1] -1 ] = 1;
         distance[ N*start[0] + start[1] -1 ] = speed( x_linspace[start[0] -1 ], y_linspace[ start[1] ] )*h_x;
     }
     if (start[1] != (N-1) ){ // we're not in a east edge, we can have a neighbour to the right
         Q[N*start[0] + start[1] + 1] = 1;
         distance[N*start[0] + start[1] + 1] = speed( x_linspace[start[0] + 1], y_linspace[start[1]] )*h_x;
     }
     if (start[0] != (M-1)){ // we're not in a north edge, we can have a neighbour north
         Q[ N*(start[0]+1) + start[1] ] = 1;
         distance[ N*(start[0]+1) + start[1] ] = speed( x_linspace[start[0]], y_linspace[start[1] + 1] )*h_y;
     }
     printQGridFromQueue(Q); // in case we need this
     printGridFromDistance(distance);

     // ITERATION PART

     // We iterate for each point in our grid
     for(i = 0; i < M*N; i ++)
     {
          minDistance = INFINITY;
          // Find the next optimal point (the one with minimum distance)
          for(j = 0; j<M*N; j ++)
          {
              if(distance[j] < minDistance && Q[j] == 1 )
              {
                  minDistance = distance[j];
                  next_valid = j;
              }
          }
          // Now that we've found the next point to put on valid, we update
          Q[next_valid] = 2;
          //printQGridFromQueue(Q); // Check
          // Now we need to add its neighbours, mark them as trial but we know where their neighbours are
          // but we just need to mark them as trial if they are currently marked as far
          if( next_valid >= N && Q[next_valid - N] == 0 ){ // if this happens then the next valid point is not in the most southern part of the grid
              Q[next_valid - N] = 1;
          }
          if ( next_valid%N != 0 && Q[next_valid -1] == 0  ){ // if this happens then the next valid point is not in the west edge
              Q[next_valid -1] = 1;
          }
          if ( next_valid%(N-1) != 0 && Q[next_valid + 1] == 0 ){ // if this happens then the next valid point is not in the east edge
              Q[next_valid + 1] = 1;
          }
          if(next_valid <= N*(M-1)-1 && Q[next_valid + N] == 0 ){ // if this happens then the next valid point is not in the northern edge of the grid
              Q[next_valid + N] = 1;
          }
          //printQGridFromQueue(Q); // Check

          // Now we need to update the current distances of those points that are marked as trial

          for(i = -1; i<= 1; i ++){ // the new valid point can only affect 9 surrounding points at most (including itself)
              for (j = -1; j<= 1; j ++){
                  coordinate = next_valid + i*N +j; // the point in that 9 stencil we're currently considering
                  if( coordinate >= N && Q[coordinate] == 1 ){ // not in the southern part
                      

                  }
              }

          }

     }



     minDistance = 0.0;
     
     }
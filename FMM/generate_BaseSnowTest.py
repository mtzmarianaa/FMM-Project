# Generate test geometry specifying h

h = 0.5
h_string = str(h)


# Generation of test geometry and producing its triangular mesh
# I also generated a triangular mesh in a square because I'm going to 
# first test my fmm method here (very naivly)
import matplotlib.pyplot as plt
import numpy as np
from math import pi, sqrt, floor, ceil
import meshpy.triangle as triangle
from matplotlib.patches import Arc
import numpy.linalg as la
from matplotlib.colors import ListedColormap

############# Generate the two circles

my_dpi=96

def circ_base(t):
    '''
    Parametrization of the base cirlce (base of the snowman) for the test geometry.
    t can be a number or an array or numbers. If t is a number the output are the
    coordinates [x, y]. If t is an array the output is a n, 2 array, the first 
    column corresponds to the coordinates of x, the second to the coordinates of y.
    '''
    points = np.zeros((len(t), 2))
    points[:, 0] = 10*np.cos(t)
    points[:, 1] = 10*np.sin(t)
    return points



############# Useful functions

def round_trip_connect(start, end):
    return [(i, i + 1) for i in range(start, end)] + [(end, start)]

def connect(start, end):
    return [(i, i + 1) for i in range(start, end)]

# def needs_refinement(vertices, area):
#         bary = np.sum(np.array(vertices), axis=0) / 3
#         max_area = 1 + (la.norm(bary, np.inf) - 1) * 0.1
#         return bool(area > max_area)

def needs_refinement(vertices, area):
        vertices_arr = np.array(vertices)
        edge1 = la.norm( np.subtract(vertices_arr[0, :], vertices_arr[1, :]) )
        edge2 = la.norm( np.subtract(vertices_arr[1, :], vertices_arr[2, :]) )
        edge3 = la.norm( np.subtract(vertices_arr[0, :], vertices_arr[2, :]) )
        max_h = h
        average_edge_length = (edge1 + edge2 + edge3)/3
        return bool(average_edge_length > max_h)
    
def nPoints(h):
    '''
    With this function we know how many points we need in the top of the snowman and in the bottom, depending on which h we want
    WE ASSUME THAT WE ARE DISTRIBUTING UNIFORMLY THESE POINTS
    '''
    nBottom = ceil(45*pi/h) 
    return nBottom

Nbase = nPoints(h)

t = np.linspace(1/4, 9/4, num = Nbase , endpoint = False)
t = np.multiply(t, pi)

points_base = circ_base(t)
    

# The points on the outline of the snowman
points =  [(-15, -10)] # start with x0 so that in each mesh we know its index
points.extend([ (points_base[i, 0], points_base[i, 1]) for i in range( len(points_base) ) ] )
# Add the facets
facets = round_trip_connect(1, len(points) -1 ) # we don't want to connnect x0

plt.figure(1)
plt.plot( points_base[:, 0], points_base[:, 1], '-.', c='#6800ff', alpha = 0.3 )
plt.show(block=False)

##############################################################################
##############################################################################
##############################################################################
##############################################################################
###### SQUARE ON THE OUTSIDE

edges_square = [(-18, -18), (18, -18), (18, 24), (-18, 24)]

# Add them to the points
points_square = points + edges_square
# Add the facets
facets_square = facets + round_trip_connect(len(points), len(points_square)-1) 

# Add them to the triangulation (this is a new triangulation)
info_square = triangle.MeshInfo()
info_square.set_points(points_square)
info_square.set_facets(facets_square)

mesh_square = triangle.build(info_square,volume_constraints= True, refinement_func=needs_refinement)

mesh_square_points = np.array(mesh_square.points) # These are the points we want to export
mesh_square_tris = np.array(mesh_square.elements) # These are thee faces we want to export
mesh_square_neigTriangles = np.array(mesh_square.neighbors) # These are the neighbors we want to export
# Now we want to create an np array where the rows are the #of the point, the columns each one of its neighbours
# This is the most naive way of creating such thing, might be useful to optimize it later (?)
# We look in the row of the mesh.elements file
N_points_square = len(mesh_square_points)
mesh_square_neigh = []
MaxN_square = 0
# Create the list of lists
for p in range(N_points_square):
    list_p = []
    for t in range(len(mesh_square_tris)):
        list_p += [point for point in mesh_square_tris[t, :] if p in mesh_square_tris[t, :] and point != p and point not in list_p]
    mesh_square_neigh.append( list_p )

# Create the list for the incident faces

mesh_IncidentFaces_sq = []
for p in range(N_points_square):
    list_faces = []
    for t in range(len(mesh_square_tris)):
        if (p in mesh_square_tris[t, :]):
            list_faces += [t]
    mesh_IncidentFaces_sq.append(list_faces)
    
# Create the labels per face


faces_label = []
colors = []
r = 5*sqrt(2)
for fi in range(len(mesh_square_tris)):
    # we need to get the coordinates of the 3 points that define that upper triangle
    p1 =  mesh_square_points[mesh_square_tris[fi, 0] , :]
    p2 =  mesh_square_points[mesh_square_tris[fi, 1] , :]
    p3 =  mesh_square_points[mesh_square_tris[fi, 2] , :]
    if ( sqrt(p1[0]**2 + p1[1]**2)<= 10 ) and ( sqrt(p2[0]**2 + p2[1]**2)<= 10 ) and (sqrt(p3[0]**2 + p3[1]**2)<= 10):
        faces_label += [3]
        colors += [0.3]
    elif( (sqrt(p1[0]**2 + p1[1]**2) + sqrt(p2[0]**2 + p2[1]**2) + sqrt(p3[0]**2 + p3[1]**2))<= 30  ):
        faces_label += [3]
        colors += [0.3]
    else:
        faces_label += [1]
        colors += [0.1]




# # #Plot
plt.figure(figsize=(800/my_dpi, 800/my_dpi), dpi=my_dpi)
fig = plt.gcf()
ax = fig.gca()
plt.gca().set_aspect('equal')
plt.triplot(mesh_square_points[:, 0], mesh_square_points[:, 1], mesh_square_tris, '-.', lw=0.5, c='#6800ff')
circle_b = plt.Circle((0, 0), 10, color="#000536",fill=False)
ax.add_patch(circle_b)
ax.add_patch(Arc((0,  5*sqrt(2)), (5*sqrt(2))*2,  (5*sqrt(2))*2, theta1=0.0, theta2=180, edgecolor="#000536", lw=1.5))
plt.title('Delaunay triangulation of base of test geometry with rectangle, H = '+h_string)
plt.show(block=False)


viridis = plt.get_cmap('magma', 256)
new_colors = viridis(np.linspace(0, 1, 256))
blue = new_colors[15]
purple = new_colors[45]
mid = floor(len(new_colors)/2)
new_colors = [blue]*mid
new_colors += [purple]*mid
newcmp = ListedColormap(new_colors)


plt.figure(figsize=(800/my_dpi, 800/my_dpi), dpi=my_dpi)
fig = plt.gcf()
plt.gca().set_aspect('equal')
plt.tripcolor(mesh_square_points[:, 0], mesh_square_points[:, 1], mesh_square_tris, faces_label, cmap = "magma")
plt.triplot(mesh_square_points[:, 0], mesh_square_points[:, 1], mesh_square_tris, '-.', lw=0.5, c='#00fffb')
plt.title('Delaunay triangulation of base test geometry, H = '+h_string)
plt.show(block = False)
plt.savefig('/Users/marianamartinez/Documents/NYU-Courant/FMM-bib/Figures/TestBaseSnow/H7/H7_Triangulation.png', dpi=my_dpi * 10)


## Save them as well

np.savetxt('TestBaseSnow/H7/H7_BoundaryPoints_Sq.txt', np.array(edges_square), delimiter =', ', fmt = '%.8f' )

facets_arr = np.array(facets_square)
np.savetxt('TestBaseSnow/H7/H7_Facets_Sq.txt', facets_arr.astype(int), delimiter =', ', fmt ='%.0f' )

np.savetxt('TestBaseSnow/H7/H7_MeshPoints_Sq.txt', mesh_square_points, delimiter =', ', fmt = '%.8f' )

np.savetxt('TestBaseSnow/H7/H7_Faces_Sq.txt', mesh_square_tris.astype(int), delimiter =', ', fmt ='%.0f' )

np.savetxt('TestBaseSnow/H7/H7_NeighTriangles_Sq.txt', mesh_square_neigTriangles.astype(int), delimiter =', ', fmt ='%.0f')

separator = "," 

with open("TestBaseSnow/H7/H7_Neigh_Sq.txt", "w") as out_file:
    for l in mesh_square_neigh:
        out_string = separator.join(str(x) for x in l) + "\n"
        out_file.write(out_string)
        
with open("TestBaseSnow/H7/H7_IncidentFaces_Sq.txt", "w") as out_file:
    for l in mesh_IncidentFaces_sq:
        out_string = separator.join(str(x) for x in l) + "\n"
        out_file.write(out_string)
        
with open("TestBaseSnow/H7/H7_FacesLabel_Sq.txt", "w") as out_file:
    for l in faces_label:
        out_string = separator.join(str(l)) + "\n"
        out_file.write(out_string)
        

#plt.show()
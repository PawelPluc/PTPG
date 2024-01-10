import numpy as np
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import matplotlib.pyplot as plt

from logic.importer import Figure_import

class FigurePlot:

    def __init__(self):

        self.figure_import = self.load_data()

        self.length = self.figure_import.laser_length
        self.coords = self.figure_import.coordinates

        # self.file_name = None
        # self.laser_symmetry = None
        # self.number_layers = None
        # self.temperature = None

        self.positions = [(i[1],0,i[2]) for i in self.coords]
        self.sizes = [( i[3] - i[1],self.length, i[4] - i[2]) for i in self.coords]
        self.colors = ["y","b","r","purple","brown","pink"][:len(self.sizes)]

    def load_data(self):
        """
        Loads the data about the figure itself.
        """
        data = Figure_import()
        if not data.load_data():
            raise ValueError("Data failed to load.")   
        
        return data
        
    def cuboid_data( self, o, size=(1,1,1)):
            """auxilary function for plotting"""
            X = [[[0, 1, 0], [0, 0, 0], [1, 0, 0], [1, 1, 0]],
                [[0, 0, 0], [0, 0, 1], [1, 0, 1], [1, 0, 0]],
                [[1, 0, 1], [1, 0, 0], [1, 1, 0], [1, 1, 1]],
                [[0, 0, 1], [0, 0, 0], [0, 1, 0], [0, 1, 1]],
                [[0, 1, 0], [0, 1, 1], [1, 1, 1], [1, 1, 0]],
                [[0, 1, 1], [0, 0, 1], [1, 0, 1], [1, 1, 1]]]
            X = np.array(X).astype(float)
            for i in range(3):
                X[:,:,i] *= size[i]
            X += np.array(o)
            return X
    

    def plotCubeAt(self, positions,sizes=None,colors=None,array=False, **kwargs):
        """auxilary function for plotting"""
        if not isinstance(colors,(list,np.ndarray)): colors=["C0"]*len(positions)
        if not isinstance(sizes,(list,np.ndarray)): sizes=[(1,1,1)]*len(positions)
        g = []
        for p,s,c in zip(positions,sizes,colors):
            g.append( self.cuboid_data(p, size=s) )

        if array:
            return g
        else:
            return Poly3DCollection(np.concatenate(g),  
                                    facecolors=np.repeat(colors,6), **kwargs)


    def plot(self):
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        ax.set_aspect('equal')

        pc = self.plotCubeAt( self.positions, self.sizes, colors=self.colors, alpha=0.4, edgecolor="k")
        ax.add_collection3d(pc)    
        ax.grid(False)

        # ax.add_collection3d(Poly3DCollection(poly3d, facecolors='y', linewidths=1, alpha=0.2))

        # ax.set_xlim([0,10])
        # ax.set_ylim([0,10])
        # ax.set_zlim([0,10])


        plt.show()
        return

    def plane_normal(self, p1, p2, p3):
            # Calculate vectors lying on the plane
            v1 = np.array(p2) - np.array(p1)
            v2 = np.array(p3) - np.array(p1)

            # Calculate the cross product of the vectors to find the normal
            normal = np.cross(v1, v2)

            normal = normal.astype(np.float64)

            # Normalize the normal vector
            # normal /= np.linalg.norm(normal)

            return normal
        
    def calculate_plane(self, point1, point2, point3, limit):
        # checking if the plane is vertical or horizontal
        if point1[0] == point2[0] and point1[0] == point3[0]:
            orientation = 0
        elif point1[1] == point2[1] and point1[1] == point3[1]:
            orientation = 1
        elif point1[2] == point2[2] and point1[2] == point3[2]:
            orientation = 2
        else:
            orientation = 3


        plane_point = np.array(point1)

        # Calculate the normal vector
        normal = self.plane_normal(point1, point2, point3)

        # transforming the array elements to floats
        # so it can be transformed later
        normal = normal.astype(np.float64)

        # a plane is a*x+b*y+c*z+d=0
        # [a,b,c] is the normal. Thus, we have to calculate
        # d and we're set
        d = -plane_point.dot(normal)

        # create x,y
        add_plane = 2
        xx, yy = np.meshgrid(range(-(limit[0]+add_plane),limit[1]+add_plane),
                            range(-(limit[0]+add_plane),limit[1]+add_plane))


        # calculate corresponding z
        if normal[2] == 0:
            if orientation == 2:
                z = (-normal[0] * xx - normal[1] * yy - d)  / 1
                z = np.ones_like(z) * plane_point[2]
            if orientation == 0:
                z = (-normal[0] * xx - normal[1] * yy - d)  / 1
                xx = np.ones_like(xx) * plane_point[0]

            if orientation == 1:
                z = (-normal[0] * xx - normal[1] * yy - d)  / 1
                yy = np.ones_like(yy) * plane_point[1]

            if orientation == 3:
                z = (-normal[0] * xx - normal[1] * yy - d)  / 1
                z = np.ones_like(z) * plane_point[2]

        else:
            z = (-normal[0] * xx - normal[1] * yy - d)  /normal[2]

        return xx, yy, z, plane_point, normal, orientation
    

    def line_plane_intersection(self, p0, p1, plane_point, plane_normal):
        """Function to find intersection points between edges and the plane"""

        # Convert inputs to numpy arrays for vector operations
        p0 = np.array(p0)
        p1 = np.array(p1)
        plane_point = np.array(plane_point)
        plane_normal = np.array(plane_normal)

        # Calculate direction vector of the line
        direction = p1 - p0

        # Calculate the denominator for the parametric equation of the line
        denominator = np.dot(direction, plane_normal)

        # Check if the line and plane are not parallel
        if abs(denominator) > 1e-6:  # Avoid division by zero
            t = np.dot(plane_point - p0, plane_normal) / denominator

            # Ensure the intersection point is within the line segment
            if 0 <= t <= 1:
                intersection_point = p0 + t * direction
                return intersection_point.tolist()  # Convert numpy array to a list

        # If the line and plane are parallel or no intersection within the line segment
        return None
    
    def project_3d_point_to_2d(self, point_3d, plane_normal, proj):
        # Convert inputs to numpy arrays for vector operations

        point_3d = np.array(point_3d)

        point_3d = np.concatenate((point_3d[-proj:], point_3d[:-proj]))

        plane_normal = np.array(plane_normal)

        # Ensure the plane normal is a unit vector
        plane_normal /= np.linalg.norm(plane_normal)

        # Project the 3D point onto the plane
        projection = point_3d - np.dot(point_3d, plane_normal) * plane_normal

        return projection.tolist()  # Convert numpy array to a list


    # Function to compute the centroid of points
    def centroid(self, points):
        x = [p[0] for p in points]
        y = [p[1] for p in points]
        centroid_x = sum(x) / len(points)
        centroid_y = sum(y) / len(points)
        return (centroid_x, centroid_y)

    # Function to compute the polar angle of a point relative to the centroid
    def polar_angle(self, point, centroid):
        x, y = point[0] - centroid[0], point[1] - centroid[1]
        return np.arctan2(y, x)
    

    def plot_cross_section(self, point1, point2, point3, projection=0, limit=(0,10), flip_v=0, flip_h=0, rotate=0):

        xx, yy, z, plane_point, normal, orientation = self.calculate_plane( point1=point1,
                                                                            point2=point2,
                                                                            point3=point3,
                                                                            limit=limit)
        

        fig = plt.figure()
        ax1 = fig.add_subplot( 1, 2, 1, projection='3d')
        ax1.set_aspect('equal')

        ax2 = fig.add_subplot( 1, 2, 2)
        ax2.set_aspect('equal')


        pc = self.plotCubeAt( self.positions, self.sizes, colors=self.colors, alpha=0.4, edgecolor="k")
        cubes = self.plotCubeAt(self.positions, self.sizes, colors=self.colors, array=True, alpha=0.4, edgecolor="k")
        ax1.add_collection3d(pc)
        ax1.grid(False)

        ax1.plot_surface(xx, yy, z, alpha=0.2)

        # Calculate intersections between cube edges and the plane
        intersections = {}
        for cube_num, cube_vertices in enumerate(cubes):
            intersections[cube_num] = []
            for vertices in cube_vertices:
                for edge in [[0,1], [1,2], [2,3], [3,0]]:
                    intersection = self.line_plane_intersection( vertices[edge[0]],
                                                        vertices[edge[1]], plane_point, normal)
                    
                    intersections[cube_num].append(intersection)

            intersections[cube_num] = [x for x in intersections[cube_num] if type(x) == list]
            intersections[cube_num] = list(map(list, set(map(tuple, intersections[cube_num]))))


        # color_list = ["red", "blue", "pink", "orange", "purple"]
        color_list = self.colors

        for cube, c in zip(intersections, color_list[:len(intersections)]):
            for inter in intersections[cube]:
                ax1.scatter( inter[0], inter[1], inter[2], color=c, marker="o")


        ax1.scatter( point1[0], point1[1], point1[2], color="black", marker="x")
        ax1.scatter( point2[0], point2[1], point2[2], color="black", marker="x")
        ax1.scatter( point3[0], point3[1], point3[2], color="black", marker="x")


        # ax1.set_xlim([limit[0],limit[1]])
        # ax1.set_ylim([limit[0],limit[1]])
        # ax1.set_zlim([limit[0],limit[1]])

        # Set labels for axes
        ax1.set_xlabel('x [um]')
        ax1.set_ylabel('y [um]')
        ax1.set_zlabel('z [um]')


        # 2D part

        projected_intersections_x = {}
        projected_intersections_y = {}

        # choosing the right indexes
        if orientation == 0:
            ind_1 = 1
            ind_2 = 2
        elif orientation == 1:
            ind_1 = 0
            ind_2 = 2
        else:
            ind_1 = 0
            ind_2 = 1


        # flip_v = 1
        # flip_h = 1
        # rotate = 1

        flip_v = 1 + (-2) * flip_v
        flip_h = 1 + (-2) * flip_h

        if rotate:
            ind_1, ind_2 = ind_2, ind_1

        
        if orientation in (0,1,2):
            projection = 0
        

        for cube, c in zip(intersections, color_list[:len(intersections)]):
            projected_intersections_x[cube] = []
            projected_intersections_y[cube] = []
            for inter in intersections[cube]:
                proj = self.project_3d_point_to_2d( inter, normal, proj=projection)
                projected_intersections_x[cube].append( proj[ind_1] * flip_v)
                projected_intersections_y[cube].append( proj[ind_2] * flip_h)


            if len( projected_intersections_x[cube]) > 2:

                ax2.scatter( projected_intersections_x[cube],
                            projected_intersections_y[cube],
                            color=c)
                

                xf = projected_intersections_x[cube]
                yf = projected_intersections_y[cube]
                pf = [[x,y] for x,y in zip(xf, yf)]

                center = self.centroid(pf)
                pf = sorted(pf, key=lambda point: self.polar_angle(point, center))
                pf.append( pf[0])

                xf = [p[0] for p in pf]
                yf = [p[1] for p in pf]


                ax2.plot( xf, yf, color=c)

        plt.show()
        return
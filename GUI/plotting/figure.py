import numpy as np
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import matplotlib.pyplot as plt

class FigurePlot:

    def __init__(self, figure_import):

        self.figure_import = figure_import
        self.data = figure_import.data

        self.length = self.data['laser_length']
        self.coords = self.data['coordinates']

        self.positions = [(i[1],0,i[2]) for i in self.coords]
        self.sizes = [( i[3] - i[1],self.length, i[4] - i[2]) for i in self.coords]
        self.colors = ["y","b","r","purple","brown","pink"][:len(self.sizes)]

    
    def cuboid_data2( self, o, size=(1,1,1)):
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
    

    def plotCubeAt2( self, positions,sizes=None,colors=None, **kwargs):
        """auxilary function for plotting"""
        if not isinstance(colors,(list,np.ndarray)): colors=["C0"]*len(positions)
        if not isinstance(sizes,(list,np.ndarray)): sizes=[(1,1,1)]*len(positions)
        g = []
        for p,s,c in zip(positions,sizes,colors):
            g.append( self.cuboid_data2(p, size=s) )
        return Poly3DCollection(np.concatenate(g),  
                                facecolors=np.repeat(colors,6), **kwargs)


    def plot(self):
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        ax.set_aspect('equal')

        pc = self.plotCubeAt2( self.positions, self.sizes, colors=self.colors, alpha=0.4, edgecolor="k")
        ax.add_collection3d(pc)    
        ax.grid(False)

        # ax.add_collection3d(Poly3DCollection(poly3d, facecolors='y', linewidths=1, alpha=0.2))

        ax.set_xlim([0,10])
        ax.set_ylim([0,10])
        ax.set_zlim([0,10])

        plt.show()
        return

import os
import math
import numpy
from matplotlib import pyplot
from mpl_toolkits import mplot3d

HEADER_SIZE = 80
COUNT_SIZE = 4

class STL:

    dtype = numpy.dtype([
        ('normals', numpy.float32, (3, )),
        ('vectors', numpy.float32, (3, 3)),
        ('attr', numpy.uint16, (1, ))
    ])
    # dtype = dtype.newbyteorder('<')

    def __init__(self, path: str):
        self.path = path
        self.header: str = None
        self.no_of_facets: int = None

        self._load()

    
    def _load(self):
        if not os.path.exists(self.path):
            raise Exception('Filename does not exists')
        with open(file=self.path, mode='rb') as fh:
            self.header = fh.read(HEADER_SIZE).decode().strip()
            self.no_of_facets = int.from_bytes(
                fh.read(COUNT_SIZE),
                byteorder = 'little'
            )
            self.data = self._load_binary(fh)
    
    # @classmethod
    def _load_binary(self, fh):
        data = numpy.frombuffer(
            buffer = fh.read(),
            dtype = self.dtype,
            count = self.no_of_facets
        )
        return data.copy()
    
    @classmethod
    def rotation_matrix(self, axis, theta=0):
        axis = numpy.asarray(axis)
        if not axis.any():
            return numpy.identity(3)

        theta = 0.5 * numpy.asarray(theta)

        axis = axis / numpy.linalg.norm(axis)

        a = math.cos(theta)
        b, c, d = - axis * math.sin(theta)
        angles = a, b, c, d
        powers = [x * y for x in angles for y in angles]
        aa, ab, ac, ad = powers[0:4]
        ba, bb, bc, bd = powers[4:8]
        ca, cb, cc, cd = powers[8:12]
        da, db, dc, dd = powers[12:16]

        return numpy.array([[aa + bb - cc - dd, 2 * (bc + ad), 2 * (bd - ac)],
                            [2 * (bc - ad), aa + cc - bb - dd, 2 * (cd + ab)],
                            [2 * (bd + ac), 2 * (cd - ab), aa + dd - bb - cc]])
    
    def rotate_using_matrix(self, rotation_matrix):

        identity = numpy.identity(rotation_matrix.shape[0])
        if not rotation_matrix.any() or (identity == rotation_matrix).all():
            return

        def _rotate(matrix):
            return matrix.dot(rotation_matrix)

        # Rotate the normals
        self.normals[:] = _rotate(self.normals[:])

        # Rotate the vectors
        for i in range(3):
            self.vectors[:, i] = _rotate(self.vectors[:, i])


    def rotate(self, axis, theta):
        self.rotate_using_matrix(
            self.rotation_matrix(axis, theta)
        )
    
    @property
    def vectors(self):
        return self.data['vectors']
    
    @vectors.setter
    def vectors(self, value):
        self.data['vectors'] = value
    
    @property
    def normals(self):
        return self.data['normals']
    
    @normals.setter
    def normals(self, value):
        self.data['normals'] = value

    @property
    def points(self):
        return self.vectors.reshape(self.data.size, 9)

    @property
    def x(self):
        return self.points[:, 0::3]
    
    @property
    def y(self):
        return self.points[:, 1::3]

    @property
    def z(self):
        return self.points[:, 2::3]
    
    def display(self):
        fig = pyplot.figure()
        ax = fig.add_subplot(1, 1, 1, projection='3d')

        coll = mplot3d.art3d.Poly3DCollection(self.vectors[(self.vectors < 10).any(axis=2)], edgecolors='C3')
        ax.add_collection(coll)

        ax.auto_scale_xyz(
            self.x.flatten(),
            self.y.flatten(),
            self.z.flatten()
        )

        # Labels
        ax.set_xlabel('x (mm)')
        ax.set_ylabel('y (mm)')
        ax.set_zlabel('z (mm)')
        ax.set_title(self.header)

        pyplot.show()
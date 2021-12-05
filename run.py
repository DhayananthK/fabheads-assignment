import math

# user-defined modules
from base import STL
from slicer import Slicer

def main():
    path = r'./stl_models/assignment.stl'
    stl = STL(path=path)
    print(stl.no_of_facets)
    # stl.rotate([1.0, 0.0, 0.0], math.radians(-90))
    # stl.display()

    slicer = Slicer(stl=stl)
    # Varying the S value will give us layers
    # S = 1 to 25
    slicer.slice(S=7)
    slicer.display()

    

if __name__ == '__main__':
    main()
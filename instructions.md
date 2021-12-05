# Fabheads Assignment Instructions

## Instructions
### STL (base.py)
The STL object is used to read the binary stl file, rotate, display
1. STl Object
```
stl = STL(path)
# param path: str filepath for the stl file 
```
2. rotate
```
stl.rotate(axis=[1.0, 0.0, 0.0], theta=math.radians(90))
# param axis: list axis to rotate
# [x, y, z] - [1.0, 0.0, 0.0] This will rotate the x axis
# param theta: angle to rotate pass it as an radian (import math)
```
3. display
```
stl.display()
```

### Slicer (slicer.py)
The Slicer object is used to slice the binary stl file.
1. Slicer
```
slicer = Slicer(stl=stl)
```
2. slicer
```
slicer.slice(S=10)
# param S: int layered thickness
```
3. display
```
slicer.display()
```
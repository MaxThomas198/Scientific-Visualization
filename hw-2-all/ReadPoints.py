#Read output from Matlab

# We will work with vtk objects
import vtk
# We also need to be able to split strings
import string

#Read Points
def readPoints(file):
  
    # Create an array of Points
    points = vtk.vtkPoints()

    #Open the file
    file = open(file)
    
    # Read one line
    line = file.readline()

    # Loop through lines
    while line:
        # Split the line into data
        data = line.split()

        # Skip the commented lines
        if data and data[0] != '#':
            try:
                # Convert data into floats 
                x, y, z = float(data[0]), float(data[1]), float(data[2])

                # Insert floats into the point array 
                points.InsertNextPoint(x, y, z)
            except:
                print("could not load one point")

        # read next line
        line = file.readline()

    return points;
    

# Read Vectors.
# This method works in the same way as readPoints but returns a different type of array
def readVectors(file):
    # Create a Double array which represents the vectors
    vectors = vtk.vtkDoubleArray()
    # Define number of elements
    vectors.SetNumberOfComponents(3)

    file = open(file)
    line = file.readline()
    while line:
        data = line.split()
        if data and data[0] != '#':
            try:
                x, y, z = float(data[0]), float(data[1]), float(data[2])

                vectors.InsertNextTuple3(x, y, z)
            except:
                print("could not load one vector")
        line = file.readline()
    return vectors

#Read Scalars
def readScalars(file):
  
    # Create an array of Scalars
    scalars = vtk.vtkFloatArray()

    #Open the file
    file = open(file)
    
    # Read one line
    line = file.readline()

    # Loop through lines
    while line:
        # Split the line into data
        data = line.split()

        # Skip the commented lines
        if data and data[0] != '#':
            try:
                # Convert data into floats 
                rad = float(data[0])

                # Insert floats into the point array
                scalars.InsertNextValue(rad)
            except:
                print("could not load a scalar")

        # read next line
        line = file.readline()

    return scalars;

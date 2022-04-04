# File:        ctscan.py
# Description: MPR rendering

import vtk

# image reader
filename1 = "ctscan_ez.vtk"
reader1 = vtk.vtkStructuredPointsReader()
reader1.SetFileName( filename1 )
reader1.Update()

W,H,D = reader1.GetOutput().GetDimensions()
a1,b1 = reader1.GetOutput().GetScalarRange()
print("Range of image: %d--%d" %(a1,b1))

filename2 = "ctscan_ez_bin.vtk"
reader2 = vtk.vtkStructuredPointsReader()
reader2.SetFileName( filename2 )
reader2.Update()

a2,b2 = reader2.GetOutput().GetScalarRange()
print("Range of segmented image: %d--%d" %(a2,b2))

# renderer and render window
ren = vtk.vtkRenderer()
ren.SetBackground(.2, .2, .2)
renWin = vtk.vtkRenderWindow()
renWin.SetSize( 512, 512 )
renWin.AddRenderer( ren )

# render window interactor
iren = vtk.vtkRenderWindowInteractor()
iren.SetRenderWindow( renWin )

#
# add your code here for MPR and the liver surface
#
# Help to get started...
#
picker=vtk.vtkCellPicker() # use same picker for all
picker.SetTolerance(0.005)

ipwx = vtk.vtkImagePlaneWidget()
ipwx.SetPicker(picker)
ipwx.SetInputData(reader1.GetOutput())
ipwx.SetCurrentRenderer(ren)
ipwx.SetInteractor(iren)
ipwx.PlaceWidget()
ipwx.SetPlaneOrientationToXAxes()
ipwx.SetSliceIndex(int(W/2))
ipwx.DisplayTextOn()
ipwx.EnabledOn()

### INSERT YOUR CODE HERE
liver = vtk.vtkContourFilter()
liver.SetInputConnection(reader2.GetOutputPort())
liver.SetValue(0, 200)
liverMapper = vtk.vtkPolyDataMapper()
liverMapper.SetInputConnection(liver.GetOutputPort())
liverActor = vtk.vtkActor()
liverActor.SetMapper(liverMapper)
###

# create an outline of the dataset
outline = vtk.vtkOutlineFilter()
outline.SetInputData( reader1.GetOutput() )
outlineMapper = vtk.vtkPolyDataMapper()
outlineMapper.SetInputData( outline.GetOutput() )
outlineActor = vtk.vtkActor()
outlineActor.SetMapper( outlineMapper )

# the actors property defines color, shading, line width,...
outlineActor.GetProperty().SetColor(0.8,0.8,0.8)
outlineActor.GetProperty().SetLineWidth(2.0)

# add the actors
ren.AddActor( outlineActor )
## ADD YOUR ACTORS HERE
ren.AddActor(liverActor)
##
renWin.Render()

# create window to image filter to get the window to an image
w2if = vtk.vtkWindowToImageFilter()
w2if.SetInput(renWin)

# create png writer
wr = vtk.vtkPNGWriter()
wr.SetInputData(w2if.GetOutput())

# Python function for the keyboard interface
# count is a screenshot counter
count = 0
toggle = 2
def Keypress(obj, event):
    global count, iv, toggle
    key = obj.GetKeySym()
    if key == "s":
        renWin.Render()
        w2if.Modified() # tell the w2if that it should update
        fnm = "screenshot%02d.png" %(count)
        wr.SetFileName(fnm)
        wr.Write()
        print("Saved '%s'" %(fnm))
        count = count+1
    elif key == "l":
        if toggle % 2:
            liverActor.VisibilityOn()
            toggle = toggle + 1
        else:
            liverActor.VisibilityOff()
            toggle = toggle + 1


    # add your keyboard interface here
    # elif key == ...

# add keyboard interface, initialize, and start the interactor
iren.AddObserver("KeyPressEvent", Keypress)
iren.Initialize()
iren.Start()

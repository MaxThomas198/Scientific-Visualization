"""Molecular dynamics.

This script should display the atoms (and their connections) in a
molecular dynamics simulation dataset.

You can run the script from the command line by typing
python molecules.py

"""

import vtk
import molecules_io


# Define a class for the keyboard interface
class KeyboardInterface(object):
    """Keyboard interface.

    Provides a simple keyboard interface for interaction. You may
    extend this interface with keyboard shortcuts for manipulating the
    molecule visualization.

    """

    def __init__(self):
        self.screenshot_counter = 0
        self.render_window = None
        self.window2image_filter = None
        self.png_writer = None
        # Add the extra attributes you need here...

    def keypress(self, obj, event):
        """This function captures keypress events and defines actions for
        keyboard shortcuts."""
        key = obj.GetKeySym()
        if key == "9":
            self.render_window.Render()
            self.window2image_filter.Modified()
            screenshot_filename = ("screenshot%02d.png" %
                                   (self.screenshot_counter))
            self.png_writer.SetFileName(screenshot_filename)
            self.png_writer.Write()
            print("Saved %s" % (screenshot_filename))
            self.screenshot_counter += 1
        # Add your keyboard shortcuts here. If you modify any of the
        # actors or change some other parts or properties of the
        # scene, don't forget to call the render window's Render()
        # function to update the rendering.
        # elif key == ...


# Read the data into a vtkPolyData object using the functions in
# molecules_io.py
data = vtk.vtkPolyData()
data.SetPoints(molecules_io.read_points("coordinates.txt"))
data.GetPointData().SetScalars(molecules_io.read_scalars("radii.txt"))
data.SetLines(molecules_io.read_connections("connections.txt"))

#
#
# Add your code here...
ball = vtk.vtkSphereSource()
ball.SetThetaResolution(12)
ball.SetPhiResolution(12)

ballGlyph = vtk.vtkGlyph3D()
ballGlyph.SetInputData(data)
ballGlyph.SetSourceConnection(ball.GetOutputPort())

# Mapper
ballMapper = vtk.vtkPolyDataMapper()
ballMapper.SetInputConnection(ballGlyph.GetOutputPort())

# Actor
ballActor = vtk.vtkActor()
ballActor.SetMapper(ballMapper)

#
tube = vtk.vtkTubeFilter()
tube.SetInputData(data)
tube.SetVaryRadiusToVaryRadiusOff()
tube.SetRadius(0.1)

mapper = vtk.vtkPolyDataMapper()
mapper.SetInputConnection(tube.GetOutputPort())


actor = vtk.vtkActor()
actor.SetMapper(mapper)

rad = [0.37, 0.68, 0.73, 0.74, 0.77, 2.0]

legend = vtk.vtkLegendBoxActor()
legend.SetNumberOfEntries(len(rad))

legendBox = vtk.vtkCubeSource()
legendBox.Update()
legend.SetEntry(0, legendBox.GetOutput(), "0.37", [0.0, 0.0, 1.0])
legend.SetEntry(1, legendBox.GetOutput(), "0.68", [0.0, 1.0, 1.0])
legend.SetEntry(2, legendBox.GetOutput(), "0.73", [0.0, 1.0, 0.0])
legend.SetEntry(3, legendBox.GetOutput(), "0.74", [1.0, 1.0, 0.0])
legend.SetEntry(4, legendBox.GetOutput(), "0.77", [1.0, 0.0, 0.0])
legend.SetEntry(5, legendBox.GetOutput(), "2.0", [1.0, 0.0, 1.0])

legend.GetPositionCoordinate().SetCoordinateSystemToDisplay()
legend.GetPositionCoordinate().SetValue(0, 0)

legend.GetPosition2Coordinate().SetCoordinateSystemToDisplay()
legend.GetPosition2Coordinate().SetValue(150, 150)
#

colorTransferFunction = vtk.vtkColorTransferFunction()
colorTransferFunction.AddRGBPoint(0.37, 0.0, 0.0, 1.0)
colorTransferFunction.AddRGBPoint(0.68, 0.0, 1.0, 1.0)
colorTransferFunction.AddRGBPoint(0.73, 0.0, 1.0, 0.0)
colorTransferFunction.AddRGBPoint(0.74, 1.0, 1.0, 0.0)
colorTransferFunction.AddRGBPoint(0.77, 1.0, 0.0, 0.0)
colorTransferFunction.AddRGBPoint(2.0, 1.0, 0.0, 1.0)

# Set colors depending on the color transfer functions
ballMapper.SetLookupTable(colorTransferFunction)

ballActor.SetMapper(ballMapper)

# Create a renderer and add the actors to it
renderer = vtk.vtkRenderer()
renderer.SetBackground(0.2, 0.2, 0.2)

## Add your actors to to the renderer
renderer.AddActor(ballActor)
renderer.AddActor(actor)
renderer.AddActor(legend)
##

# Create a render window
render_window = vtk.vtkRenderWindow()
render_window.SetWindowName("Molecular dynamics")
render_window.SetSize(500, 500)
render_window.AddRenderer(renderer)

# Create an interactor
interactor = vtk.vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Create a window-to-image filter and a PNG writer that can be used
# to take screenshots
window2image_filter = vtk.vtkWindowToImageFilter()
window2image_filter.SetInput(render_window)
png_writer = vtk.vtkPNGWriter()
png_writer.SetInputConnection(window2image_filter.GetOutputPort())

# Set up the keyboard interface
keyboard_interface = KeyboardInterface()
keyboard_interface.render_window = render_window
keyboard_interface.window2image_filter = window2image_filter
keyboard_interface.png_writer = png_writer

# Connect the keyboard interface to the interactor
interactor.AddObserver("KeyPressEvent", keyboard_interface.keypress)

# Initialize the interactor and start the rendering loop
interactor.Initialize()
render_window.Render()
interactor.Start()

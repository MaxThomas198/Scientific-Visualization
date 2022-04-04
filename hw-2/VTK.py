import vtk

# Define a class for the keyboard interface
class KeyboardInterface(object):
    """Keyboard interface.

    Provides a simple keyboard interface for interaction. You should
    extend this interface with keyboard shortcuts for changing the
    isovalue interactively.

    """

    def __init__(self):
        self.screenshot_counter = 0
        self.render_window = None
        self.window2image_filter = None
        self.png_writer = None
        # Add the extra attributes you need here...
        self.isoSurface = None

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
        # Add your keyboard shortcuts here. You can use, e.g., the
        # "Up" key to increase the isovalue and the "Down" key to
        # decrease it. Don't forget to call the render window's
        # Render() function to update the rendering after you have
        # changed the isovalue.
        # elif key == ...
        elif key=="Up":
            self.isoSurface.SetValue(0, self.isoSurface.GetValue(0)+0.1)
            render_window.Render()
        elif key=="Down":
            self.isoSurface.SetValue(0, self.isoSurface.GetValue(0)-0.1)
            render_window.Render()

# Read the volume dataset
filename = "hydrogen.vtk"
reader = vtk.vtkStructuredPointsReader()
reader.SetFileName(filename)
print("Reading volume dataset from " + filename + " ...")
reader.Update()  # executes the reader
print("Done!")

# Just for illustration, extract and print the dimensions of the
# volume. The string formatting used here is similar to the sprintf
# style in C.
width, height, depth = reader.GetOutput().GetDimensions()
print("Dimensions: %i %i %i" % (width, height, depth))

# Create an outline of the volume
# filter
outline = vtk.vtkOutlineFilter()
outline.SetInputConnection(reader.GetOutputPort())
# mapper
outline_mapper = vtk.vtkPolyDataMapper()
outline_mapper.SetInputConnection(outline.GetOutputPort())
# actor
outline_actor = vtk.vtkActor()
outline_actor.SetMapper(outline_mapper)
# Define actor properties (color, shading, line width, etc)
outline_actor.GetProperty().SetColor(0.8, 0.8, 0.8)
outline_actor.GetProperty().SetLineWidth(2.0)

# Create a renderer and add the actors to it
renderer = vtk.vtkRenderer()
renderer.SetBackground(0.2, 0.2, 0.2)
renderer.AddActor(outline_actor)

# Range of the data
data = reader.GetOutput()
a,b = data.GetScalarRange()
print("Range of image: %d--%d" %(a,b))

# Create transfer mapping scalar value to opacity.
opacityTransferFunction = vtk.vtkPiecewiseFunction()
opacityTransferFunction.AddPoint(0, 0.0)
opacityTransferFunction.AddPoint(1, 0.2)

# Create transfer mapping scalar value to color.
colorTransferFunction = vtk.vtkColorTransferFunction()
colorTransferFunction.AddRGBPoint(0.0, 0.0, 0.0, 0.0)
colorTransferFunction.AddRGBPoint(0.25, 1.0, 0.0, 0.0)
colorTransferFunction.AddRGBPoint(0.5, 0.0, 0.0, 1.0)
colorTransferFunction.AddRGBPoint(0.75, 0.0, 1.0, 0.0)
colorTransferFunction.AddRGBPoint(1.0, 0.0, 0.2, 0.0)

# The property describes how the data will look.
volumeProperty = vtk.vtkVolumeProperty()
volumeProperty.SetColor(colorTransferFunction)
volumeProperty.SetScalarOpacity(opacityTransferFunction)
volumeProperty.ShadeOn()
volumeProperty.SetInterpolationTypeToLinear()

# The mapper / ray cast function know how to render the data.
volumeMapper = vtk.vtkFixedPointVolumeRayCastMapper()
volumeMapper.SetInputConnection(reader.GetOutputPort())

# The volume holds the mapper and the property and
# can be used to position/orient the volume.
myvolume = vtk.vtkVolume()
myvolume.SetMapper(volumeMapper)
myvolume.SetProperty(volumeProperty)

renderer.AddVolume(myvolume)

# create the scalar_bar
scalar_bar = vtk.vtkScalarBarActor()
scalar_bar.SetOrientationToHorizontal()
scalar_bar.SetLookupTable(colorTransferFunction)

# Isosurface
isoSurface = vtk.vtkContourFilter()
isoSurface.SetInputConnection(reader.GetOutputPort())
isoSurface.SetValue(0, 0.5)
isoMapper = vtk.vtkPolyDataMapper()
isoMapper.SetInputConnection(isoSurface.GetOutputPort())
isoActor = vtk.vtkActor()
isoActor.SetMapper(isoMapper)
renderer.AddActor(isoActor)


# Create a render window
render_window = vtk.vtkRenderWindow()
render_window.SetWindowName("Isosurface extraction")
render_window.SetSize(800, 800)
render_window.AddRenderer(renderer)

# Create an interactor
interactor = vtk.vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# create the scalar_bar_widget
scalar_bar_widget = vtk.vtkScalarBarWidget()
scalar_bar_widget.SetScalarBarActor(scalar_bar)
scalar_bar_widget.SetInteractor(interactor)
scalar_bar_widget.On()

renderer.AddActor(scalar_bar)

# Create a window-to-image filter and a PNG writer that can be used
# for taking screenshots
window2image_filter = vtk.vtkWindowToImageFilter()
window2image_filter.SetInput(render_window)
png_writer = vtk.vtkPNGWriter()
png_writer.SetInputConnection(window2image_filter.GetOutputPort())

# Set up the keyboard interface
keyboard_interface = KeyboardInterface()
keyboard_interface.render_window = render_window
keyboard_interface.window2image_filter = window2image_filter
keyboard_interface.png_writer = png_writer
keyboard_interface.isoSurface = isoSurface

# Connect the keyboard interface to the interactor
interactor.AddObserver("KeyPressEvent", keyboard_interface.keypress)

# Initialize the interactor and start the rendering loop
interactor.Initialize()
render_window.Render()
interactor.Start()




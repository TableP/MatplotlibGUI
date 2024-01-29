from functools import partial

import customtkinter
import matplotlib.backends.backend_tkagg

from Controller import Controller
from Model import Model


class UserInterface(customtkinter.CTk):
    def __init__(self):

        #setting _controller as none initially
        self._controller = None
        customtkinter.set_appearance_mode("dark")
        super().__init__()
        print("initialising user interface")
        #initial configuration
        self.geometry("1000x750")
        self.propagate(False)
        self.protocol("WM_DELETE_WINDOW", lambda: (self.quit(), self.destroy()))
        #grid config
        self.grid_rowconfigure(0, weight=2)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        #instantiating frame objects from classes
        self.importPanel = ImportDataPanel(self, self)
        self.customizePanel = CustomiseGraphPanel(self, self)
        self.visualPanel = VisualiseGraphPanel(self)
        self.terminalPanel = TerminalDisplayPanel(self)
        #setting up the frames to be added
        self.importPanel.grid(row=0, column=0, padx=20, pady=20, sticky='nesw', rowspan=1)
        self.customizePanel.grid(row=0, column=1, padx=0, pady=20, sticky='nesw')
        self.visualPanel.grid(row=0, column=2, padx=20, pady=20, sticky='nesw')
        self.terminalPanel.grid(row=1, column=1, padx=30, pady=30, sticky='nesw', columnspan=2)

    def setController(self, controller):
        self._controller = controller

    def printTest(self, object, value):
        print("test success within viewer range")
        print(value)
        print(object.get())

    #handles button events
    def mainButtonHandler(self, function):
        if self._controller:
            self._controller.buttonEventHandler(function)
        else:
            print("no controller found")

    #handles combobox events
    def comboBoxToController(self, comboBoxSelection, function):
        if self._controller:
            self._controller.configEventHandler(function, comboBoxSelection)
        else:
            print("no controller found")

    #handles slider release events
    def sliderReleaseToController(self, function, slider, e):
        if self._controller:
            self._controller.configEventHandler(slider.get(), function)
        else:
            print("no controller found")

    #handles live slider events
    def liveSliderUpdater(self, newVal):
        self.customizePanel.setCTextParam1(newVal)






class CustomiseGraphPanel(customtkinter.CTkFrame):
    def __init__(self, master, mainViewer):
        super().__init__(master, width=200, height=400)
        self.mainViewer = mainViewer
        self.propagate(False)
        print("initialising user interface")
        #setting up grid weightings
        self.grid_rowconfigure(0, weight=5)
        self.grid_rowconfigure(1, weight=5)
        self.grid_rowconfigure(2, weight=5)
        self.grid_rowconfigure(3, weight=5)
        self.grid_rowconfigure(4, weight=8)
        self.grid_rowconfigure(5, weight=3)
        self.grid_rowconfigure(6, weight=3)
        self.grid_rowconfigure(7, weight=3)
        self.grid_rowconfigure(8, weight=3)
        self.grid_rowconfigure(9, weight=3)
        self.grid_rowconfigure(10, weight=3)
        self.grid_rowconfigure(11, weight=3)
        self.grid_rowconfigure(12, weight=3)
        self.grid_rowconfigure(13, weight=3)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        #setting up labels
        self.xLabel = customtkinter.CTkLabel(self, text="X Axis")
        self.yLabel = customtkinter.CTkLabel(self, text="Y Axis")
        self.cTextParamMain = customtkinter.CTkLabel(self, text="Adjust graph parameters")
        self.cTextParam1 = customtkinter.CTkLabel(self, text="Param 1")
        self.cTextParam2 = customtkinter.CTkLabel(self, text="Line Colour")
        self.cTextParam3 = customtkinter.CTkLabel(self, text="Line Style")
        self.cTextParam4 = customtkinter.CTkLabel(self, text="Marker")



        #setting up customisable options
        #axis configuration
        self.titleLabel = customtkinter.CTkLabel(self, text="Current title: NONE")
        self.titleButton = customtkinter.CTkButton(self, text="Add Title", command=partial(
            self.mainViewer.mainButtonHandler, "AddTitle"))
        self.xComboBox = customtkinter.CTkComboBox(self, command=partial(self.mainViewer.comboBoxToController, "x"), state="readonly")
        self.yComboBox = customtkinter.CTkComboBox(self, command=partial(self.mainViewer.comboBoxToController, "y"), state="readonly")
        self.xOverrideButton = customtkinter.CTkButton(self, text="Custom name", command=partial(
            self.mainViewer.mainButtonHandler, "xOverride"))
        self.yOverrideButton = customtkinter.CTkButton(self, text="Custom name", command=partial(
            self.mainViewer.mainButtonHandler, "yOverride"))

        #sliders
        self.cSliderParam1 = customtkinter.CTkSlider(self, from_=0, to=5, command=partial(self.mainViewer.liveSliderUpdater))
        self.cComboBoxParam2 = customtkinter.CTkComboBox(self, values=["red", "orange", "yellow", "green", "blue", "cyan", "violet"], state="readonly",
                                                         command=partial(self.mainViewer.comboBoxToController, "Line Colour"))
        self.cComboBoxParam3 = customtkinter.CTkComboBox(self, values=["-", "--", "-.", ":", ""], state="readonly",
                                                         command=partial(self.mainViewer.comboBoxToController, "Line Style"))
        self.cComboBoxParam4 = customtkinter.CTkComboBox(self, values=["o", "v", "^", "<", ">", ""], state="readonly",
                                                         command=partial(self.mainViewer.comboBoxToController, "Marker"))
        #slider binds
        self.cSliderParam1.bind("<ButtonRelease-1>", command=partial(self.mainViewer.sliderReleaseToController, "Line Width", self.cSliderParam1))

        # configuring labels and combobox
        self.cSliderParam1.set(1)
        self.cTextParam1.configure(text="Size of Line: " + str(self.cSliderParam1.get()))
        self.xComboBox.set("")
        self.yComboBox.set("")
        self.cComboBoxParam2.set("red")
        self.cComboBoxParam3.set("-")
        self.cComboBoxParam4.set("o")


        #placement of objects
        self.titleLabel.grid(row=0, column=0, padx=20, pady=10, sticky='s')
        self.titleButton.grid(row=0, column=1, padx=20, pady=10, sticky='s')
        self.xLabel.grid(row=1, column=0, padx=20, pady=5, sticky='n', columnspan=2)
        self.xComboBox.grid(row=2, column=0, padx=20, pady=0)
        self.xOverrideButton.grid(row=2, column=1, padx=20, pady=0)
        self.yLabel.grid(row=3, column=0, padx=20, pady=5, columnspan=2)
        self.yComboBox.grid(row=4, column=0, padx=20, pady=0)
        self.yOverrideButton.grid(row=4, column=1, padx=20, pady=0)
        self.cTextParamMain.grid(row=5, column=0, padx=20, pady=5, sticky='s', columnspan=2)
        self.cTextParam1.grid(row=6, column=0, padx=20, pady=5, sticky='n', columnspan=2)
        self.cSliderParam1.grid(row=7, column=0, padx=20, pady=5, sticky='nesw', columnspan=2)
        self.cTextParam2.grid(row=8, column=0, padx=20, pady=5, sticky='n', columnspan=2)
        self.cComboBoxParam2.grid(row=9, column=0, padx=20, pady=5, sticky='nesw', columnspan=2)
        self.cTextParam3.grid(row=10, column=0, padx=20, pady=5, sticky='n', columnspan=2)
        self.cComboBoxParam3.grid(row=11, column=0, padx=20, pady=5, sticky='nesw', columnspan=2)
        self.cTextParam4.grid(row=12, column=0, padx=20, pady=5, sticky='nesw', columnspan=2)
        self.cComboBoxParam4.grid(row=13, column=0, padx=20, pady=5, sticky='nesw', columnspan=2)

    def setXAxisComboBox(self, text):
        self.xComboBox.set(text)

    def setYAxisComboBox(self, text):
        self.yComboBox.set(text)

    def setGraphLabel(self, text):
        self.titleLabel.configure(text="Current title: " + text)

    def setCTextParam1(self, text):
        self.cTextParam1.configure(text="Size of Line: " + str(text))

class ImportDataPanel(customtkinter.CTkFrame):
    #have to pass two selfs to this method to gain access to parent class methods - enquire about this later
    def __init__(self, master, mainViewer):
        self.mainViewer = mainViewer
        super().__init__(master, width=200, height=200)
        print("initialising user interface")
        self.propagate(False)
        #grid config
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.grid_rowconfigure(3, weight=1)
        self.grid_rowconfigure(4, weight=1)
        self.grid_columnconfigure(0, weight=1)
        #button stuff - linking button to associated main viewer which is linked to main Controller
        self.button1 = customtkinter.CTkButton(self, width=200, height=100, border_width=5, text="import CSV", command=partial(
            self.mainViewer.mainButtonHandler, "impCSV"))
        self.button2 = customtkinter.CTkButton(self, width=200, height=100, text="Generate Figure", command=partial(
            self.mainViewer.mainButtonHandler, "GenGraph"))
        self.button3 = customtkinter.CTkButton(self, width=200, height=100, text="Add Graph", command=partial(
            self.mainViewer.mainButtonHandler, "AddGraph"))
        self.button4 = customtkinter.CTkButton(self, width=200, height=100, text="Save Figure", command=partial(
            self.mainViewer.mainButtonHandler, "SaveGraph"))
        self.button5 = customtkinter.CTkButton(self, width=200, height=100, text="Settings", command=partial(
            self.mainViewer.mainButtonHandler))
        #grid placement
        self.button1.grid(row=0, column=0, padx=10, pady=5)
        self.button2.grid(row=1, column=0, padx=10, pady=5)
        self.button3.grid(row=2, column=0, padx=10, pady=5)
        self.button4.grid(row=3, column=0, padx=10, pady=5)
        self.button5.grid(row=4, column=0, padx=10, pady=5)

    def returnData(self):
        importData = "" #this will draw from the csv file so expect arrays etc.
        return importData


class VisualiseGraphPanel(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master, width=500, height=200)
        print("initialising user interface")
        self.graphVisual = None

    #generates a graph onto a tk_widget that will pack itself onto the frame
    def drawGraph(self, graph):
        if self.graphVisual:
            self.graphVisual.get_tk_widget().destroy()
            self.graphVisual = matplotlib.backends.backend_tkagg.FigureCanvasTkAgg(graph, master=self)
            self.graphVisual.draw()
            self.graphVisual.get_tk_widget().pack()
        else:
            self.graphVisual = matplotlib.backends.backend_tkagg.FigureCanvasTkAgg(graph, master=self)
            self.graphVisual.draw()
            self.graphVisual.get_tk_widget().pack()

class TerminalDisplayPanel(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master, width=750, height=50, fg_color="white")
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.propagate(True)
        self.textDisplay = customtkinter.CTkTextbox(self, width=750, height=150, text_color="white", state="normal")
        self.textDisplay.configure(state= "disabled")
        self.textDisplay.grid(row=0, column=0, padx=20, pady=2)


import datetime
import customtkinter
import matplotlib.pyplot
import matplotlib.figure


class Controller:
    def __init__(self, viewer, model):
        print("initialising controller")
        #grabs the model and viewer
        self._viewer = viewer
        self._model = model
        self.updateTerminalText("Log initialised")

    #can use match and case but elifs basically accomplish the same objective
    #currently in testing phase
    def buttonEventHandler(self, function):
        if function == "impCSV":
            filepath = customtkinter.filedialog.askopenfilename()
            #this is a tryblock for the ability to catch an error with regards to the file path selected
            try:
                self._model.readCSVFile(filepath)
                sCSV = self._model.getCSVArray()
                self.updateTerminalText("Extracted CSV values are: " + str(sCSV))
                self._model.setCSVLoaded(True)
                self.generateGraphDetails(sCSV)
                self.updateComboBox()
            except:
                self.updateTerminalText("Error: CSV Loaded is in an incorrect format"
                                        "\n Please use row 1 as keys names and subsequent rows as values of key")

        elif function == "GenGraph":
            #if no CSV has been loaded yet then there is no data in the model to use for graph generation
            if self._model.getCSVLoaded():
                self.generateGraph()
            else:
                self.updateTerminalText("Error: CSV has not been loaded so no graph can be generated")

        elif function == "SaveGraph":
            self.saveFigure()

        elif function == "xOverride":
            self.overrideXVal()

        elif function == "yOverride":
            self.overrideYVal()

        elif function == "AddTitle":
            self.addTitle()


    #updates text in the viewer terminal panel - requires testing
    def updateTerminalText(self, textToDisplay):
        currentDateTime = datetime.datetime.now()
        formatedDateTime = currentDateTime.strftime("%H: %M: %S")
        self._viewer.terminalPanel.textDisplay.configure(state="normal")
        self._viewer.terminalPanel.textDisplay.insert("end", str(formatedDateTime) + "   ")
        self._viewer.terminalPanel.textDisplay.insert("end", textToDisplay + "\n")
        self._viewer.terminalPanel.textDisplay.see("end")
        self._viewer.terminalPanel.textDisplay.configure(state="disabled")

    #accesses the model variables to set them based on the config parameter and value
    def configEventHandler(self, selection, configParam):
        print(configParam)
        print(selection)
        if configParam == "x":
            print("x is the axis")
            self._model.setXLabels(selection)
            self.updateTerminalText("X axis has been adjusted to: " + selection)
        elif configParam == "y":
            self._model.setYLabels(selection)
            self.updateTerminalText("Y axis has been adjusted to: " + selection)
        elif configParam == "Line Width":
            self._model.setLineWidth(selection)
            self.updateTerminalText("Line Width has been adjusted to: " + str(selection))
        elif configParam == "Line Colour":
            self._model.setLineColour(selection)
            self.updateTerminalText("Line Colour has been adjusted to: " + selection)
        elif configParam == "Line Style":
            self._model.setLineStyle(selection)
            self.updateTerminalText("Line Style has been adjusted to: " + selection)
        elif configParam == "Marker":
            self._model.setMarker(selection)
            self.updateTerminalText("Marker type has been adjusted to: " + selection)

        #if a graph has already been generated then it will be updated
        if self._model.getGraphOnScreenBoolean():
            self.generateGraph()

    #grabs the x and y labels and appends to array
    def generateGraphDetails(self, incArray):
        self.axisLabels = []
        self.axisValues = []
        self.csvArray = incArray
        for key in self.csvArray:
            self.axisLabels.append(key)
            self.axisValues.append(self.csvArray[key])

        self._model.setXLabels(self.axisLabels[0])
        self._model.setYLabels(self.axisLabels[1])

        #i think this is redundant so look again later
        #self._model.setXVals(self.axisValues[0])
        #self._model.setYVals(self.axisValues[1])

    #multigraph figures not implemented yet. To be done as a future release
    #using the selected x and y label will grab appropriate values based on key:value pairings and then generates a graph
    #based on configuration values from the model
    def generateGraph(self):
        self.xLabel = self._model.getXLabels()
        self.yLabel = self._model.getYLabels()
        numberOfGraphs = self._model.getNumberOfActiveGraphs()

        values = self._model.getCSVArray()
        #utilises the fact that they x/y labels are the exact keys for the key:value pairs within the CSV
        xyVals = self.sortXAxis(values[self.xLabel], values[self.yLabel])

        xVal = []
        yVal = []
        for i in range(len(xyVals)):
            xVal.append(xyVals[i][0])
            yVal.append(xyVals[i][1])

        tempXLabel = self._model.getXLabelOverride()
        tempYLabel = self._model.getYLabelOverride()

        if tempXLabel is None:
            tempXLabel = self.xLabel

        if tempYLabel is None:
            tempYLabel = self.yLabel


        #figsize is literally the width and length of the figure not the inner subplot dimension
        self.newFigure = matplotlib.figure.Figure(figsize=(5, 5), dpi=100)


        #algorithm for generating graphs based on number of graph - not in use
        subplotDimensionVals = self.determineSubplotDimenions(numberOfGraphs)


        #this 111 is the reason why each new figure does not actually get drawn correctly
        #they are being placed on top of eachother
        newGraph = self.newFigure.add_subplot(111)
        newGraph.plot(xVal, yVal, linewidth=self._model.getLineWidthVal(), c=str(self._model.getLineColour()),
                           linestyle=str(self._model.getLineStyle()), marker=str(self._model.getLineMarker()))
        newGraph.set_xlabel(tempXLabel)
        newGraph.set_ylabel(tempYLabel)
        graphTitle = self._model.getGraphTitle()
        if graphTitle is None:
            newGraph.set_title("")
        else:
            newGraph.set_title(graphTitle)
        self._viewer.visualPanel.drawGraph(self.newFigure)
        #sets the graph on screen boolean to true as a graph is now on the screen
        self._model.setGraphOnScreenBoolean(True)
        self._model.setCurrentFigure(self.newFigure)
        self.updateTerminalText("Graph generation successful")

    #unused but will be in the future when support for multiple subplots is implemented
    def determineSubplotDimenions(self, numOfGraphs):
        if numOfGraphs == 1:
            return 1
        elif numOfGraphs < 5:
            return 2
        elif numOfGraphs < 10:
            return 3

    #sorts the pairs of coordinates based on the xVal
    def sortXAxis(self, valX, valY):
        #zip combines two lists together
        #sorted is a sorter
        combinedVals = sorted(zip(valX, valY))
        return combinedVals

    #when graph details have been generated this method is called afterwards
    #populates x/y combobox with all potential keys which act as axis names
    def updateComboBox(self):
        self.currentComboBoxValues = []
        for label in self.axisLabels:
            self.currentComboBoxValues.append(label)
        #print(self.currentComboBoxValues)
        #print(self._viewer.customizePanel.xComboBox.get())
        self._viewer.customizePanel.xComboBox.configure(values=self.currentComboBoxValues)
        self._viewer.customizePanel.yComboBox.configure(values=self.currentComboBoxValues)
        xLabel = self._model.getXLabelOverride()
        yLabel = self._model.getYLabelOverride()

        if xLabel is None:
            self._viewer.customizePanel.xComboBox.set(self.currentComboBoxValues[0])
        if yLabel is None:
            self._viewer.customizePanel.yComboBox.set(self.currentComboBoxValues[1])

    #saves figure on screen as "test.png" in local directory. If no figure is found an error is given
    def saveFigure(self):
        figure = self._model.getCurrentFigure()
        if figure is not None:
            #matplotlib.pyplot.savefig(self._model.getCurrentFigure, "test.png")
            figure.savefig("test.png")
            self.updateTerminalText("figure saved")
        else:
            self.updateTerminalText("no figure found")

    def overrideXVal(self):
        newLabelInput = customtkinter.CTkInputDialog(text="Input new label for X")
        newLabel = newLabelInput.get_input()
        self._model.setXLabelOverride(newLabel)
        self._viewer.customizePanel.setXAxisComboBox(newLabel)
        self.updateTerminalText("X axis has been set to: " + newLabel)
        if self._model.getGraphOnScreenBoolean():
            self.generateGraph()

    def overrideYVal(self):
        newLabelInput = customtkinter.CTkInputDialog(text="Input new label for Y")
        newLabel = newLabelInput.get_input()
        self._model.setYLabelOverride(newLabel)
        self._viewer.customizePanel.setYAxisComboBox(newLabel)
        self.updateTerminalText("Y axis has been set to: " + newLabel)
        if self._model.getGraphOnScreenBoolean():
            self.generateGraph()

    def addTitle(self):
        newLabelInput = customtkinter.CTkInputDialog(text="Input new label for Y")
        newLabel = newLabelInput.get_input()
        self._model.setGraphTitle(newLabel)
        self.updateTerminalText("Title has been set to: " + newLabel)
        self._viewer.customizePanel.setGraphLabel(newLabel)
        if self._model.getGraphOnScreenBoolean():
            self.generateGraph()






import csv
import matplotlib

class Model:

    def __init__(self):
        print("model online")
        self._controller = None
        self._graphOnScreenBoolean = False
        self._cCSVLoaded = False
        self._csvArray = {}
        #will be used for future feature of multi figure display
        self._graphSubPlots = []
        self._graphTitle = None
        self._xLabel = ""
        self._yLabel = ""
        self._xLabelOverride = None
        self._yLabelOverride = None
        self._xVals = []
        self._yVals = []
        self._numberOfActiveGraphs = 0
        self._currentFigure = None

        self._lineWidthVal = 1
        self._lineColour = "hotpink"
        self._lineStyle = "-"
        self._lineMarker = "o"

    def setController(self, controller):
        self._controller = controller
    #consider moving to controller as it is technically logic however it is logic directly related to data
    def readCSVFile(self, targetString: str):
        self._csvArray = {}
        #if there is no controller then an error will pop up as it uses a controller method
        if self._controller is not None:
            #encoding='utf-8-sig' is used to remove the Byte Order Mark
            with open(targetString, newline='', encoding='utf-8-sig') as targetCSVFile:
                #DictReader uses row 1 as key and the current row as value for key:value pairs
                csvReader = csv.DictReader(targetCSVFile)
                #iteration of elements in csvReader (csvReader is an object with rows)
                for row in csvReader:
                    print(row)
                    self.combineKeys(row)
        else:
            print("no controller found")


            #print(self.csvArray)

    #adds identical key values from the addDict to mainDict
    def combineKeys(self, addDict: dict):
        #iterates keys through addDict
        for key in addDict:
            #print(key)
            #checks if keys exist in the main dictionary
            #if key exists then the value list appends the key value of addDict
            if key in self._csvArray:
                self._csvArray[key].append(int(addDict[key]))
            #if the key does not exist then a new key:pair value is added
            else:
                self._csvArray[key] = [int(addDict[key])]



    def getCSVArray(self):
        return self._csvArray

    def getXLabels(self):
        return self._xLabel

    def getYLabels(self):
        return self._yLabel

    def getXVals(self):
        return self._xVals

    def getYVals(self):
        return self._yVals

    def getGraphSubPlots(self):
        return self._graphSubPlots

    def getNumberOfActiveGraphs(self):
        return self._numberOfActiveGraphs

    def getLineWidthVal(self):
        return self._lineWidthVal

    def getLineColour(self):
        return self._lineColour

    def getLineStyle(self):
        return self._lineStyle

    def getLineMarker(self):
        return self._lineMarker

    def getGraphOnScreenBoolean(self):
        return self._graphOnScreenBoolean

    def getCurrentFigure(self):
        return self._currentFigure

    def getXLabelOverride(self):
        return self._xLabelOverride

    def getYLabelOverride(self):
        return self._yLabelOverride

    def getGraphTitle(self):
        return self._graphTitle

    def getCSVLoaded(self):
        return self._cCSVLoaded

    def setXLabels(self, label):
        self._xLabel = label

    def setYLabels(self, label):
        self._yLabel = label

    def setXVals(self, vals):
        self._xVals = vals

    def setYVals(self, vals):
        self._yVals = vals

    def setGraphSubPlots(self, subPlot):
        self._graphSubPlots.append(subPlot)

    def setNumberOfActiveGraphs(self, numOfGraphs):
        self._numberOfActiveGraphs = numOfGraphs

    def setGraphOnScreenBoolean(self, state):
        self._graphOnScreenBoolean = state

    def setCurrentFigure(self, figure):
        self._currentFigure = figure

    def setXLabelOverride(self, label):
        self._xLabelOverride = label

    def setYLabelOverride(self, label):
        self._yLabelOverride = label

    def setGraphTitle(self, title):
        self._graphTitle = title

    def setCSVLoaded(self, boolean):
        self._cCSVLoaded = boolean

    def setLineWidth(self, val):
        self._lineWidthVal = val

    def setLineColour(self, val):
        self._lineColour = val

    def setLineStyle(self, val):
        self._lineStyle = val

    def setMarker(self, val):
        self._lineMarker = val


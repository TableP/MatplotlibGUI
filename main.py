# This is a sample Python script.
from Controller import Controller
from Model import Model
from UserInterface import UserInterface


# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.

def startProgram():
    viewer = UserInterface()
    model = Model()
    controller = Controller(viewer, model)
    model.setController(controller)
    viewer.setController(controller)
    viewer.mainloop()



# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    startProgram()
    print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/

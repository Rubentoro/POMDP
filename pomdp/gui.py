import sys
import tkinter
from tkinter import *
from app import App
from tkinter import scrolledtext

class RedirectText(object):
    def __init__(self, text_ctrl):
        self.output = text_ctrl
 
    def write(self, string):
        self.output.insert(tkinter.END, string)


# Window config

window = Tk()
window.title("POMDP")
window.geometry('1080x720')

L1 = Label(text="Welcome to POMDP GUI", fg="black")
L1.grid(column=1, row=1, columnspan=10, sticky=W)

L2 = Label(text="Select the problem to solve:", fg="black")
L21 = Label(text="    (Choices: tag, tiger, bridge, car)", fg="black")
L2.grid(column=5, row=3, columnspan=10, sticky=W)
L21.grid(column=5, row=4, columnspan=10, sticky=W)
problem = Entry(window, width=30)
problem.grid(column=5, row=5, columnspan=10, sticky=W)

L4 = Label(text="Select the algorithm to solve the problem:", fg="black")
L41 = Label(text="    (Choices: pomcp, pbvi)", fg="black")
L4.grid(column=5, row=7, columnspan=10, sticky=W)
L41.grid(column=5, row=8, columnspan=10, sticky=W)
algorithm = Entry(window, width=30)
algorithm.grid(column=5, row=9, columnspan=10, sticky=W)

L5 = Label(text="Select the parameters to run the algorithm", fg="black")
L5.grid(column=5, row=11, columnspan=10, sticky=W)

L6 = Label(text="Budget:", fg="black")
L6.grid(column=5, row=13, columnspan=10, sticky=W)
budget = Entry(window,width=30)
budget.grid(column=5, row=14, columnspan=10, sticky=W)

L7 = Label(text="Maximum play times:", fg="black")
L71 = Label(text="    (0 --> No limit)", fg="black")
L7.grid(column=5, row=16, sticky=W)
L71.grid(column=5, row=17, sticky=W)
max_play = Entry(window,width=30)
max_play.grid(column=5, row=18, columnspan=10, sticky=W)

L8 = Label(text="Mode:", fg="black")
L82 = Label(text="    (Choices: interactive, silent, benchmark)")
L8.grid(column=5, row=20, columnspan=10, sticky=W)
L82.grid(column=5, row=21, columnspan=10, sticky=W)
mode = Entry(window, width=30)
mode.grid(column=5, row=22, columnspan=10, sticky=W)

stdout_widget = scrolledtext.ScrolledText(height=20, width=130)
stdout_widget.grid(column=3, row=32, columnspan=10, sticky=W)

# Calling functions according to the selected choices
def main_app():
    if problem.get() == 'tag':
        App().run_tag(None, str(algorithm.get()), float(budget.get()), float(max_play.get()), None, None, str(mode.get()))
    elif problem.get() == 'tiger':
        App().run_tiger(None, str(algorithm.get()), float(budget.get()), float(max_play.get()), None, None, str(mode.get()))
    elif problem.get() == 'bridge':
        App().run_bridge_repair(None, str(algorithm.get()), float(budget.get()), float(max_play.get()), None, None, str(mode.get()))
    elif problem.get() == 'car':
        App().run_car(None, str(algorithm.get()), float(budget.get()), float(max_play.get()), None, None, str(mode.get()))

def main_app_redirect():
    # Redirect stdout
    stdout_widget.delete(1.0, END) # Clean stdout_widget
    redirection = RedirectText(stdout_widget)
    sys.stdout = redirection
    main_app()

def main_app_terminal():
    sys.stdout=sys.__stdout__
    main_app()


# Button
button_here = Button(window, text="Run here", command=main_app_redirect)
button_here.grid(column=5, row=27, columnspan=10, sticky=W)

# Button
button_terminal = Button(window, text="Run in terminal", command=main_app_terminal)
button_terminal.grid(column=6, row=27, columnspan=10, sticky=W)


# Keep the app running
window.mainloop()
import PySimpleGUI as sg

sg.theme('DarkAmber')   # Add a touch of color
# All the stuff inside your window.

# Layouts
board_layout = [[sg.Button(),
                sg.Button(),
                sg.Button(),
                sg.Button(),
                sg.Button(),
                sg.Button(),
                sg.Button(),
                sg.Button()]]

results_layout = [[sg.Text("FC"), sg.Text("HC")]]

guess_layout = [] + board_layout + results_layout

main_window_layout = [[sg.Text("Player Board")]]
main_window_layout += board_layout
main_window_layout += [[sg.Text("# Guesses")]‎]

# Create the Window
window = sg.Window('Window Title', main_window_layout)
# Event Loop to process "events" and get the "values" of the inputs
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Cancel': # if user closes window or clicks cancel
        break
    print('You entered ', values[0])

window.close()
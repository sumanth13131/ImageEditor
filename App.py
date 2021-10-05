import json
import os
import cv2
import PySimpleGUI as sg

# Theme config
sg.theme('BlueMono')


# DropDown
with open("convert.json") as f:
    data = json.load(f)["BGR_to"]

# Mapping
with open("lookup.json") as f:
    bgr_map = json.load(f)["BGR_to_map"]


def App():  # Main func
    layout = [  # Row0
                [sg.Text('IMAGE EDITOR', justification='center', size=(100, 2),
                         font=("Arial", 30))],

                # Row1
                [sg.Text("Choose an Image:", size=(13, 1), font=("Arial", 15)),
                 sg.Input(size=(40, 1)),
                 sg.FileBrowse(key="path", size=(10, 1), font=("Arial", 15)),
                 sg.Button("Open", size=(10, 1), font=("Arial", 15))],

                # Row2
                [sg.Text("")],

                # Row3
                [sg.Text("Convert To :", size=(13, 1), font=("Arial", 15)),
                 sg.Combo(data, default_value="--Select--",
                          key="convert_to", size=(25, 1)),
                 sg.Button("Convert", size=(10, 1), font=("Arial", 15)),
                 sg.Button("Save", size=(10, 1), font=("Arial", 15))
                 ],

                # Row4
                [sg.Image(key="image", pad=(100, 0))],

    ]

    # Building Window
    window = sg.Window('Image Editor', layout,
                       size=(800, 600), resizable=True, grab_anywhere=True)

    # Event Loop
    while True:
        event, values = window.read()  # Reading Window
        if event == sg.WIN_CLOSED:
            break

        # Open and Rendering Image In Window
        elif event == "Open":
            print(values["path"])
            try:
                img = cv2.imread(values["path"])
                img = cv2.resize(img, (550, 400))
                imgbytes = cv2.imencode('.png', img)[1].tobytes()
                window["image"].update(data=imgbytes)
            except:
                sg.popup_error('Supports Only Formats : *.png, *.jpg, *.jpeg')

        # Converting The image According To Dropdown Selection
        elif event == "Convert" and values["convert_to"] != "--Select--":
            to_c = values["convert_to"]
            img = cv2.imread(values["path"])
            img = cv2.cvtColor(img, bgr_map[to_c])
            img = cv2.resize(img, (550, 400))
            imgbytes = cv2.imencode('.png', img)[1].tobytes()
            window["image"].update(data=imgbytes)

        # Saving An Image
        elif event == "Save" and values["convert_to"] != "--Select--":
            text = sg.popup_get_folder(
                'Please enter a folder name to save image')
            to_c = values["convert_to"]
            img = cv2.imread(values["path"])
            img = cv2.cvtColor(img, bgr_map[to_c])
            filename = os.path.join(text, 'result.jpg')
            cv2.imwrite(filename, img)
            sg.popup_ok('Successfully saved ..!')

    # Destroying The window
    window.close()


if __name__ == '__main__':
    App()

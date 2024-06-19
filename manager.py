import PySimpleGUI as sg
from utils import create_config_if_not_exists, update_config, parse_folder, create_config_layout

config = create_config_if_not_exists()

if not config:
    setup_layout = [
        [sg.Text("Select the path to your EVE O Preview Installation...")], 
        [sg.Text("Install Folder"),sg.In(size=(25,1), enable_events=True, key="-FOLDER-"), sg.FolderBrowse()]
    ]
    setup_window = sg.Window("Setup", setup_layout)
    while True:
        event, values = setup_window.read()

        if event == "-FOLDER-":
            temp_folder=values["-FOLDER-"]
            if temp_folder:
                config["folder"]=temp_folder
                update_config(config)
            break
        elif event == sg.WIN_CLOSED:
            setup_window.close()
            exit()

    setup_window.close()


profiles = parse_folder(config)


treedata = sg.TreeData()
for index, profile in enumerate(profiles):
    treedata.Insert("", index, profile.get("file"), [profile.get("updated")])

tree = sg.Tree(
        treedata, 
        headings=["last updated"],
        enable_events=True,
        k="-TREE-",
        col0_width=30
    )

file_layout = [
    [tree]
]


main_layout = [
    [
    sg.Col(file_layout, vertical_alignment='top'),
    sg.VSeparator(),
    sg.Col([create_config_layout(config, profiles[0], 0)], k='-CONFIG SECTION-', vertical_alignment='top')
    ]
]

main_window = sg.Window("EVE-O-Preview Profiles", main_layout, relative_location=(250,230))

active_config = 0
activated_configs = []

while True:
    event, values = main_window.read()
    
    if event == "-TREE-":
        idx = values["-TREE-"][0]
        main_window[('-ROW-', active_config)].update(visible=False)
        profile = profiles[idx]
        active_config = idx
        if active_config in activated_configs:
            main_window[('-ROW-', active_config)].update(visible=True)
        else:
            main_window.extend_layout(main_window['-CONFIG SECTION-'], [create_config_layout(config, profile, active_config)])
            activated_configs.append(active_config)
    if event == sg.WIN_CLOSED:
        main_window.close()
        exit()
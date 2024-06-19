import json
import os
import PySimpleGUI as sg

def create_config_if_not_exists():
    if not os.path.exists('eve-o-profiles.config.json'):
       with open('eve-o-profiles.config.json', 'w') as f:
           json.dump({}, f)
           config = {}
    else:
        with open('eve-o-profiles.config.json', 'r') as f:
            config = json.load(f)
    return config
        

def update_config(config):
    with open('eve-o-profiles.config.json', 'w') as f:
        json.dump(config, f)

def parse_folder(config):
    folder = config["folder"]
    file_list = os.listdir(folder)

    profiles = []

    for f in file_list:
        if os.path.isfile(os.path.join(folder, f)) and f.lower().endswith("json"):
            profile = {}
            profile["file"] = f
            profile["updated"] = os.path.getmtime(os.path.join(folder, f))
            profiles.append(profile)

    return profiles

def parse_config(config, file):
    with open(os.path.join(config["folder"], file), "r") as f:
        eve_config = json.load(f)
    return eve_config

def create_config_layout(config, profile, active_config):
    eve_config = parse_config(config, profile["file"])

    row = [
        sg.pin(
            sg.Col([
                [
                    sg.Text(text="name"),
                    sg.Text(text=profile["file"])
                ],
                [
                    sg.Text(text="Group1")
                ],
                [
                    sg.Multiline(default_text=json.dumps(eve_config.get("CycleGroup1ClientsOrder"), indent=2), expand_x=True, size=(None, 8))
                ],
                [
                    sg.Text(text="Group2")
                ],
                [
                    sg.Multiline(default_text=json.dumps(eve_config.get("CycleGroup2ClientsOrder"), indent=2), expand_x=True, size=(None, 8))
                ],
                [
                    sg.Text(text="Window Layout")
                ],
                [
                    sg.Multiline(default_text=json.dumps(eve_config.get("FlatLayout"), indent=2), expand_x=True, size=(None, 8))
                ],
                [
                    sg.Button(button_text="Save Config"), sg.Button(button_text="Set Active")
                ],
                [
                    sg.Input(k="-PROFILE NAME-"), sg.Button(button_text="Create Duplicate")
                ]
            ], k=('-ROW-', active_config))
        )
    ]
    return row
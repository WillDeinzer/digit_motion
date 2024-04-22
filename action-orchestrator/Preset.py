import Action
import json 
import os 

class PresetLoader:

    def __init__(self, path): 
        self.path = path
        self.presets = {}

    def load(self):
        presets = os.listdir(self.path)
        for preset in presets:
            with open(os.path.join(self.path, preset)) as f:
                data = json.load(f)
                self.presets[preset.strip('.json')] = data
    
    def reload_preset(self, preset: str):
        with open(os.path.join(self.path, preset + ".json")) as f:
            data = json.load(f)
            self.presets[preset] = data
    
    def get(self, preset: str):
        return self.presets.get(preset, None)

presetLoader = PresetLoader('presets')


class Preset:

    def __init__(self, name):
        self.name = name
        self.actions = []

    
    def toJSON(self):
        return {'name':self.name, 'actions': [action.toJSON() for action in self.actions]}
    
    def fromJSON(self, json):
        self.name = json['name']
        self.actions = []
        for action in json['actions']:
            self.actions.append(Action.ACTIONS[action[0]](action[1]))
        return self
    
    def addAction(self, action):
        self.actions.append(action)
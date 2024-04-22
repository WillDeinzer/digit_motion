import json
import os
import imgui 
import guis



class Waypoint: 
    def __init__(self, x, y, z):
        self.x = x 
        self.y = y 
        self.z = z
    
    def toJSON(self):
        return [{'xyz':[self.x, self.y, self.z]}]


class ActionLoader:

    def __init__(self, path): 
        self.path = path
        self.actions = {}

    def load(self):
        actions = os.listdir(self.path)
        for action in actions:
            with open(os.path.join(self.path, action)) as f:
                data = json.load(f)
                self.actions[action.strip('.json')] = data
    
    def reload_action(self, action: str):
        with open(os.path.join(self.path, action + ".json")) as f:
            data = json.load(f)
            self.actions[action] = data
    
    def get(self, action: str):
        return self.actions.get(action, None)
    
    
actionLoader = ActionLoader('base-actions')

    


class Action:
    def __init__(self, name):
        self.name = name 
        self.data = {}
        self.opt_gui = {}
        self.render_funcs = {}


    def toJSON(self):
        return [self.name, self.data.copy()]
    
    def copy(self):
        return ACTIONS[self.name](self.data.copy())
    
    def render_opts(self):
        for key, val in self.data.items():
            func = self.opt_gui.get(key, None)
            if func:
                func()
            else: 
                if (type(val) == float or type(val) == int):
                    self.data[key] = imgui.input_float(key, val)

    def reload(self):
        actionLoader.reload_action(self.name)
        self.data = actionLoader.get(self.name)[1]

    def render(self):
        for key, value in self.data.items():
            func = self.render_funcs.get(key, None)
            if func:
                func()
            else:
                imgui.text(f"{key}: {value}")
            





class MoveEndEffector(Action):

    def __init__(self, data={}):
        super().__init__("action-move-end-effector")
        self.data = data
        if(len(data) == 0):
            self.data = actionLoader.get(self.name)[1]
        
        print(self.data)



        self.opt_gui = {
            'waypoints': guis.WaypointCreatorWidget(self.add_waypoint).render,
            'end-effector': guis.EndEffectorSelector(self.save_end_effector).render
        }

        self.render_funcs = {
            'waypoints': guis.WaypointWidget(None,self.data['waypoints']).render,}

    def add_waypoint(self, coords):
        x, y, z = coords
        waypoint = Waypoint(x, y, z)
        self.data['waypoints'].append(waypoint.toJSON())
    
    def save_end_effector(self, end_effector):
        self.data['end-effector'] = end_effector


class ConcurrentAction(Action):

    def __init__(self, data={}):
        super().__init__("action-concurrent")
        self.data = data
        if (len(data) != 0):
            actions = data['actions']
            for i, action in enumerate(actions):
                self.data['actions'][i] = ACTIONS[action[0]](action[1])
        if(len(data) == 0):
            self.data = actionLoader.get(self.name)[1]

        self.opt_gui = {'actions': guis.ActionCreatorWidget(self.add_action, actionLoader).render}


    def render(self):
        imgui.text("Concurrent Action")
        for action in self.data['actions']:
            imgui.indent(10)
            imgui.text(action.name)
            imgui.unindent(10)

    def add_action(self, action):
        self.data['actions'].append(action)

    def copy(self):
        data_copy = self.data.copy()
        data_copy['actions'] = [action.copy() for action in self.data['actions']]
        return ConcurrentAction(data_copy)

    def toJSON(self):
        json = super().toJSON()
        json[1]['actions'] = [action.toJSON() for action in self.data['actions']]
        return json


ACTIONS = {'action-move-end-effector': MoveEndEffector,
           'action-concurrent': ConcurrentAction}
        
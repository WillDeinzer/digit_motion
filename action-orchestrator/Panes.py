import imgui

class Pane:

    def __init__(self, name, width, height, pos):
        self.name = name
        self.width = width
        self.height = height
        self.pos = pos

    def render(self): 
        pass 



class MainPane(Pane):

    def __init__(self, tabs={}): 
        super().__init__("Main", 1280-600, 250, (300, 18))
        self.tabs = tabs

        


    def render(self): 
        imgui.set_next_window_size(self.width, self.height)
        imgui.set_next_window_position(self.pos[0], self.pos[1])
        
        with imgui.begin("Main", True):
            with imgui.begin_tab_bar("Main Bar") as tab_bar:
                if tab_bar.opened:
                    for name, tab in self.tabs.items():
                        with imgui.begin_tab_item(name) as item:
                            if item.selected:
                                tab()
                 
                            
                    
                        
                                
           


class ActionSelectorPane(Pane):

    def __init__(self, actionLoader, callback):
        super().__init__("Action Selector", 300, 720, (1280-300, 18))
        self.callback = callback
        self.actionLoader = actionLoader
        self.action = None 

    def unselect(self):
        self.action = None
        
    def render(self):
        imgui.set_next_window_size(self.width, self.height)
        imgui.set_next_window_position(self.pos[0], self.pos[1])
        
        with imgui.begin("Action Selector", True):
            for action in self.actionLoader.actions.keys():
                if imgui.selectable(action, self.action == action)[0]:
                    self.action = action 
                    self.callback(self.actionLoader.get(action))


class PresetSelectorPane(Pane):

    def __init__(self, presetLoader, callback):
        super().__init__("Preset Selector", 300, 720, (0, 18))
        self.presetLoader = presetLoader
        self.preset = None
        self.callback = callback
    def render(self):
        imgui.set_next_window_size(self.width, self.height)
        imgui.set_next_window_position(self.pos[0], self.pos[1])
        
        with imgui.begin("Preset Selector", True):
            for preset in self.presetLoader.presets.keys():
                if imgui.selectable(preset, self.preset == preset)[0]:
                    self.action = preset 
                    self.callback(self.presetLoader.get(preset))


class PresetPane(Pane):
    
        def __init__(self, render):
            super().__init__("Preset", 1280-600, 300, (300, 268))
            self.renderfunc = render
    
        def render(self):
            imgui.set_next_window_size(self.width, self.height)
            imgui.set_next_window_position(self.pos[0], self.pos[1])
            
            with imgui.begin("Preset", True):
                self.renderfunc()
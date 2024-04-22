from __future__ import absolute_import
from imgui.integrations.pygame import PygameRenderer
import OpenGL.GL as gl
import imgui
import pygame
import sys
import Action
import Panes
import Preset
import json

current_action = None 

"""
" Run pip install imgui[full] to install imgui
" The JSON in the base_action folder is incorrect, please replace with the correct JSON so the
" gui loads in the fields correctly
"""



class ActionOrchestrator:

    def __init__(self):
        self.current_action = None 
        self.current_preset = Preset.Preset("untitled") 
        self.editing = False
        pass 


    def update_action(self, action_type):
        if self.current_action != None:
            self.current_action.reload()
        self.editing = False
        self.current_action = Action.ACTIONS[action_type[0]]()

    def update_presets(self, preset_type):
        self.current_preset = Preset.Preset("untitled").fromJSON(preset_type)
        self.current_action = None


    def addAction(self):
        if self.current_action != None:            
            with imgui.begin_group():
                self.current_action.render()
            imgui.same_line(spacing = 20)
            with imgui.begin_group():
                imgui.set_next_window_bg_alpha(1)
                with imgui.begin_child("Options", 0, 0, border=True):
                    if self.editing:
                        imgui.text("Editing: " + self.current_action.name)
                        imgui.same_line(spacing = 10)
                        imgui.text("Index: " + str(self.current_preset.actions.index(self.current_action)))
                    self.current_action.render_opts()
                    if self.editing == False: 
                        if imgui.button("Save"):
                            print(self.current_action.toJSON())
                            self.current_preset.addAction(self.current_action.copy())
                            self.current_action.reload() 

                        imgui.same_line(spacing = 10)
                        if imgui.button("refresh"):
                            self.current_action.reload() 
                    else: 
                        imgui.text("Editing: Changes are committed automatically to preset")
                        imgui.text("         Press save below to save changes to disk")

    def editPreset(self):
        imgui.text("TODO: Implement edit action")
    
    def renderPreset(self):
        with imgui.begin_group():
            with imgui.begin_list_box(" ", 200, 100) as list_box:
                for i, action in enumerate(self.current_preset.actions):
                    if imgui.selectable(f"[{i}] {action.name}")[0]:
                        self.current_action = action
                        self.editing = True
        imgui.same_line(spacing = 20)
        with imgui.begin_group():
            with imgui.begin_child("Preset", 0, 0, border=True):
                _, self.current_preset.name = imgui.input_text("Name", self.current_preset.name)
                if self.editing:
                    if imgui.button("Move up"):
                        index = self.current_preset.actions.index(self.current_action)
                        if index > 0:
                            self.current_preset.actions[index], self.current_preset.actions[index-1] = self.current_preset.actions[index-1], self.current_preset.actions[index]
                    
                    if imgui.button("Move down"):
                        index = self.current_preset.actions.index(self.current_action)
                        if index < len(self.current_preset.actions) - 1:
                            self.current_preset.actions[index], self.current_preset.actions[index+1] = self.current_preset.actions[index+1], self.current_preset.actions[index]
                
                if imgui.button("Save"):
                    with open("presets/" + self.current_preset.name + ".json", 'w') as f:
                        json.dump(self.current_preset.toJSON(), f, indent=4)
                    Preset.presetLoader.load()
            

        



def main():
    pygame.init()
    size = 1280, 720

    pygame.display.set_mode(size, pygame.DOUBLEBUF | pygame.OPENGL | pygame.RESIZABLE)
    pygame.display.set_caption("Action Orchestrator")
    imgui.create_context()
    impl = PygameRenderer()

    io = imgui.get_io()
    io.display_size = size
    Action.actionLoader.load()
    Preset.presetLoader.load()
    actionOrchestrator = ActionOrchestrator()
    panes = []
    panes.append(Panes.ActionSelectorPane(Action.actionLoader, actionOrchestrator.update_action))
    panes.append(Panes.PresetSelectorPane(Preset.presetLoader, actionOrchestrator.update_presets))
    panes.append(Panes.PresetPane(actionOrchestrator.renderPreset))
    tabs = {'Add': actionOrchestrator.addAction}
    main = Panes.MainPane(tabs)
    panes.append(main)
    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)
            impl.process_event(event)
        impl.process_inputs()

        imgui.new_frame()

        if imgui.begin_main_menu_bar():
            if imgui.begin_menu("File", True):

                clicked_quit, selected_quit = imgui.menu_item(
                    "Quit", "Cmd+Q", False, True
                )

                if clicked_quit:
                    sys.exit(0)

                imgui.end_menu()
            imgui.end_main_menu_bar()
        for pane in panes:
            pane.render()
        
        # note: cannot use screen.fill((1, 1, 1)) because pygame's screen
        #       does not support fill() on OpenGL sufraces
        gl.glClearColor(1, 1, 1, 1)
        gl.glClear(gl.GL_COLOR_BUFFER_BIT)
        imgui.render()
        impl.render(imgui.get_draw_data())

        pygame.display.flip()


if __name__ == "__main__":
    main()

    

    pass 
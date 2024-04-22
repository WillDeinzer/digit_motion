import imgui
import Action 

def null_func():
    return

class Widget:
    def __init__(self, name, callback = null_func):
        self.name = name 
        self.callback = callback
    
    def render(self):
        pass 

class WaypointCreatorWidget(Widget):
    def __init__(self, callback):
        super().__init__("Waypoint Editor")
        self.x, self.y, self.z = 0, 0, 0
        self.callback = callback

    def render(self):
        
        if imgui.button("Add Waypoint"):
            imgui.open_popup(self.name)

        with imgui.begin_popup_modal(self.name) as popup:
            if not popup.opened:
                return
            
            _, self.x = imgui.input_float("X", self.x)
            _, self.y = imgui.input_float("Y", self.y)
            _, self.z = imgui.input_float("Z", self.z)

            if imgui.button("Save"):
                self.callback((self.x, self.y, self.z))
                imgui.close_current_popup()
            
            if imgui.button("Cancel"):
                imgui.close_current_popup()

class WaypointWidget(Widget):
    def __init__(self, callback, waypoints):
        super().__init__("Waypoints")
        self.callback = callback
        self.waypoints = waypoints
        self.coord = (0, 0, 0)

    def render(self):
        imgui.text(f"waypoints: [{len(self.waypoints)}]")
        for i, waypoint in enumerate(self.waypoints):
            imgui.indent(10)
            buf = f"xyz: {waypoint[0]['xyz'][0]}, {waypoint[0]['xyz'][1]}, {waypoint[0]['xyz'][2]}"
            if imgui.selectable(f"[{i}] {buf}")[0]:
                imgui.open_popup(f"waypoint-{i}")

            with imgui.begin_popup_modal(f"waypoint-{i}") as popup:
                if popup.opened:
                    

                    _, waypoint[0]['xyz'][0] = imgui.input_float("X", waypoint[0]['xyz'][0])
                    _, waypoint[0]['xyz'][1] = imgui.input_float("Y", waypoint[0]['xyz'][1])
                    _, waypoint[0]['xyz'][2] = imgui.input_float("Z", waypoint[0]['xyz'][2])

                    if imgui.button("Close"):
                        imgui.close_current_popup()
            imgui.unindent(10)
            
            
class EndEffectorSelector(Widget):

    def __init__(self, callback):
        super().__init__("End Effector Selector")
        self.end_effectors = ["left-foot", "right-foot", "left-hand", "right-hand"]
        self.end_effector = -1
        self.callback = callback

    def render(self):
        with imgui.begin_combo("end-effector", self.end_effectors[self.end_effector]) as combo:
            if combo.opened:
                for i, end_effector in enumerate(self.end_effectors):
                    is_selected = self.end_effector == i
                    if imgui.selectable(end_effector)[0]:
                        self.end_effector = i
                        self.callback(self.end_effectors[self.end_effector])
                    if is_selected:
                        imgui.set_item_default_focus()


class ActionCreatorWidget(Widget):

    def __init__(self, callback, actionLoader):
        super().__init__("Action Creator")
        self.callback = callback
        self.name = ""
        self.data = {}
        self.actionLoader = actionLoader
        self.action_type = None
        self.action = None
        self.block_list = ['action-concurrent']

    def render(self):
        if imgui.button("Create Action"):
            imgui.open_popup("Action Creator")
        
        with imgui.begin_popup_modal("Action Creator") as popup:
            if not popup.opened:
                return
            with imgui.begin_group():
                if (self.action != None):
                    with imgui.begin_group():
                        self.action.render()
                    imgui.same_line(spacing = 10)
                    with imgui.begin_group():
                        imgui.set_next_window_bg_alpha(1)
                        with imgui.begin_child("Options", 0, 300, border=True):
                            self.action.render_opts()
                            if imgui.button("Save"):
                                self.callback(self.action)
                                self.action.reload()
                                self.action = None

                                imgui.close_current_popup()

            imgui.same_line(spacing = 20)
            with imgui.begin_group():
                with imgui.begin_child("Action Creator", 0, 0, border=True):
                    for action in self.actionLoader.actions.keys():
                        if imgui.selectable(action, self.action_type == action)[0]:
                            self.action_type = action 
                            self.action = Action.ACTIONS[self.actionLoader.get(action)[0]]()
                            #self.callback(self.actionLoader.get(action))
            if imgui.button("Close"):
                imgui.close_current_popup()
                if self.action != None:
                    self.action.reload()

            
        


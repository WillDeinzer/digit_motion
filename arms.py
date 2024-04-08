import math
import asyncio
import contextvars
import functools
import json
import agility
import agility.messages as msgs


# Note - 127.0.0.1 for simulator, 10.10.1.1 for hardware

# Constant vars for easy edit
ADDRESS = '127.0.0.1'
PORT = 8080
CONNECT_TIMEOUT = 9999999.0

async def to_thread(func, /, *args, **kwargs):
    loop = asyncio.get_running_loop()
    ctx = contextvars.copy_context()
    func_call = functools.partial(ctx.run, func, *args, **kwargs)
    return await loop.run_in_executor(None, func_call)

async def main(address: str = ADDRESS, port: int = PORT, connect_timeout: float = CONNECT_TIMEOUT):
    async with agility.JsonApi(address) as api:
        info = await api.query(msgs.GetRobotInfo())
        print(f"Robot name: {info.robot_name}")

        await api.request_privilege("change-action-command")
        reach_action = json.loads('''[
        "action-end-effector-move",
        {
            "end-effector": "right-hand",
            "waypoints": [
            {
                "xyz": [
                0.4,
                -0.15,
                0.1
                ]
            }
            ],
            "reference-frame": {
            "command-frame": "base"
            },
            "stall-threshold": null,
            "cyclic": false,
            "max-speed": 0.8,
            "duration": 3,
            "transition-duration": null
        }
        ]''')

        retract_action = json.loads('''[
        "action-end-effector-move",
        {
            "end-effector": "right-hand",
            "waypoints": [
            {
                "xyz": [
                0.2,
                -0.15,
                0.3
                ]
            }
            ],
            "reference-frame": {
            "command-frame": "base"
            },
            "stall-threshold": null,
            "cyclic": false,
            "max-speed": 0.3,
            "duration": 3,
            "transition-duration": null
        }
        ]''')

        award_action = json.loads('''[
        "action-end-effector-move",
        {
            "end-effector": "right-hand",
            "waypoints": [
            {
                "xyz": [
                0.6,
                -0.2,
                0.2
                ]
            }
            ],
            "reference-frame": {
            "command-frame": "base"
            },
            "stall-threshold": null,
            "cyclic": false,
            "max-speed": 0.2,
            "duration": 5,
            "transition-duration": null
        }
        ]''')

        default_position = json.loads('''[
        "action-end-effector-move",
        {
            "end-effector": "right-hand",
            "waypoints": [
            {
                "xyz": [
                0.3,
                -0.3,
                -0.1
                ]
            }
            ],
            "reference-frame": {
            "command-frame": "base"
            },
            "stall-threshold": null,
            "cyclic": false,
            "max-speed": 0.3,
            "duration": 3,
            "transition-duration": null
        }
        ]''')

        rotate_90_counter = json.loads('''[
        "action-goto",
        {
            "target": {"rpyxy": [0, 0, 1.570796, 0, 0]},
            "heading-constraint": null,
            "reference-frame": {
            "special-frame": "world"
            },
            "position-tolerance": 0.2,
            "orientation-tolerance": 0.2,
            "mobility-parameters": {}
        }
        ]''')
        
        face_forward = json.loads('''[
        "action-goto",
        {
            "target": {"rpyxy": [0, 0, 0, 0, 0]},
            "heading-constraint": null,
            "reference-frame": {
            "special-frame": "world"
            },
            "position-tolerance": 0.2,
            "orientation-tolerance": 0.2,
            "mobility-parameters": {}
        }
        ]''')
        
        rotate_90_clock = json.loads('''[
        "action-goto",
        {
            "target": {"rpyxy": [0, 0, -1.570796, 0, 0]},
            "heading-constraint": null,
            "reference-frame": {
            "special-frame": "world"
            },
            "position-tolerance": 0.2,
            "orientation-tolerance": 0.2,
            "mobility-parameters": {}
        }
        ]''')
        
        action = ""
        while action != "quit":
            action = await to_thread(input, "Enter an action (reach_comm, retract_comm, award, rotate_90, face_forward) or type 'quit': ")
            action = str(action).split()
            if len(action) > 0:
                if action[0] == "quit":
                    break
                elif action[0].lower() == "reach_comm":
                    await api.wait_action(reach_action, remove_after=False)
                elif action[0].lower() == "retract_comm":
                    await api.wait_action(retract_action, remove_after=False)
                elif action[0].lower() == "award":
                    await api.wait_action(award_action, remove_after=False)
                elif action[0].lower() == "rotate_90":
                    await api.wait_action(rotate_90_counter, remove_after=False)
                elif action[0].lower() == "face_forward":
                    await api.wait_action(face_forward, remove_after=False)
                elif action[0].lower() == "rotate":
                    angle_in_deg = 0
                    if len(action) > 1:
                        angle_in_deg = int(action[1])
                    
                    angle_in_rad = angle_in_deg * math.pi / 180
                    
                    rotate = json.loads('''[
                    "action-goto",
                    {
                        "target": {"rpyxy": [0, 0, %angle, 0, 0]},
                        "heading-constraint": null,
                        "reference-frame": {
                        "special-frame": "world"
                        },
                        "position-tolerance": 0.2,
                        "orientation-tolerance": 0.2,
                        "mobility-parameters": {}
                    }
                    ]'''.replace("%angle", str(angle_in_rad)))
                        
                    await api.wait_action(rotate, remove_after=False)
                else:
                    await api.wait_action(default_position, remove_after=False)

asyncio.run(main())
    
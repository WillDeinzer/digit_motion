import asyncio
import contextvars
import functools
import json
import agility
import agility.messages as msgs

async def to_thread(func, /, *args, **kwargs):
    loop = asyncio.get_running_loop()
    ctx = contextvars.copy_context()
    func_call = functools.partial(ctx.run, func, *args, **kwargs)
    return await loop.run_in_executor(None, func_call)

async def main(address: str = '10.10.1.1', port: int = 8080, connect_timeout: float = 9999999.0):
    async with agility.JsonApi(address = '10.10.1.1') as api:
        info = await api.query(msgs.GetRobotInfo())
        print(f"Robot name: {info.robot_name}")

        await api.request_privilege("change-action-command")
        reach_action = json.loads('''[
        "action-concurrent",
        {
            "actions": [[
        "action-end-effector-move",
        {
            "end-effector": "left-hand",
            "waypoints": [
            {
                "xyz": [
                0.4,
                0.015,
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
        ], [
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
        ] ]
        }
        ]''')


        squeeze_action = json.loads('''[
        "action-concurrent",
        {
            "actions": [[
        "action-end-effector-move",
        {
            "end-effector": "left-hand",
            "waypoints": [
            {
                "xyz": [
                0.3,
                0.15,
                0.2
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
        ], [
        "action-end-effector-move",
        {
            "end-effector": "right-hand",
            "waypoints": [
            {
                "xyz": [
                0.3,
                -0.15,
                0.2
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
        ] ]
        }
        ]''')


        retract_action = json.loads('''[
        "action-concurrent",
        {
            "actions": [[
        "action-end-effector-move",
        {
            "end-effector": "left-hand",
            "waypoints": [
            {
                "xyz": [
                0.2,
                0.15,
                0.2
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
        ], [
        "action-end-effector-move",
        {
            "end-effector": "right-hand",
            "waypoints": [
            {
                "xyz": [
                0.2,
                -0.15,
                0.2
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
        ] ]
        }
        ]''')


        award_action = json.loads('''[
        "action-concurrent",
        {
            "actions": [[
        "action-end-effector-move",
        {
            "end-effector": "left-hand",
            "waypoints": [
            {
                "xyz": [
                0.2,
                0.15,
                0.2
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
        ], [
        "action-end-effector-move",
        {
            "end-effector": "right-hand",
            "waypoints": [
            {
                "xyz": [
                0.2,
                -0.15,
                0.2
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
        ] ]
        }
        ]''')


        unsqueeze_action = json.loads('''[
        "action-concurrent",
        {
            "actions": [[
        "action-end-effector-move",
        {
            "end-effector": "left-hand",
            "waypoints": [
            {
                "xyz": [
                0.2,
                0.3,
                0.2
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
        ], [
        "action-end-effector-move",
        {
            "end-effector": "right-hand",
            "waypoints": [
            {
                "xyz": [
                0.2,
                -0.3,
                0.2
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
        ] ]
        }
        ]''')

        default_position = json.loads('''[
        "action-concurrent",
        {
            "actions": [[
        "action-end-effector-move",
        {
            "end-effector": "left-hand",
            "waypoints": [
            {
                "xyz": [
                0.3,
                0.3,
                0.1
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
        ], [
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
        ] ]
        }
        ]''')

        rotate_90 = json.loads('''[
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
        action = ""
        while action != "quit":
            action = await to_thread(input, "Enter an action (reach_comm, squeeze, retract_comm, award, unsqueeze, rotate_90) or type 'quit': ")
            if action == "quit":
                break
            elif action == "reach_comm":
                await api.wait_action(reach_action, remove_after=False)
            elif action == "squeeze":
                await api.wait_action(squeeze_action, remove_after=False)
            elif action == "retract_comm":
                await api.wait_action(retract_action, remove_after=False)
            elif action == "award":
                await api.wait_action(award_action, remove_after=False)
            elif action == "unsqueeze":
                await api.wait_action(unsqueeze_action, remove_after=False)
            elif action == "rotate_90":
                await api.wait_action(rotate_90, remove_after=False)
            else:
                await api.wait_action(default_position, remove_after=False)

asyncio.run(main())
    
import asyncio
import contextvars
import functools
import json
import agility
import agility.messages as msgs


# Note - 127.0.0.1 for simulator, 10.10.1.1 for hardware

async def to_thread(func, /, *args, **kwargs):
    loop = asyncio.get_running_loop()
    ctx = contextvars.copy_context()
    func_call = functools.partial(ctx.run, func, *args, **kwargs)
    return await loop.run_in_executor(None, func_call)

async def main(address: str = '127.0.0.1', port: int = 8080, connect_timeout: float = 9999999.0):
    async with agility.JsonApi(address = '127.0.0.1') as api:
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
                0.5,
                -0.2,
                0.1
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
        move_forward = json.loads('''[
            "action-move",
            {
            "velocity": {"axy": [0, 0.5, 0]},
            "mobility-parameters": {}
            }
        ]''')
        turn_clockwise = json.loads('''[
            "action-move",
            {
            "velocity": {"axy": [-0.5, 0, 0]},
            "mobility-parameters": {}
            }
        ]''')
        turn_counterclockwise = json.loads('''[
            "action-move",
            {
            "velocity": {"axy": [0.5, 0, 0]},
            "mobility-parameters": {}
            }
        ]''')
        stop = json.loads('''[
            "action-move",
            {
            "velocity": {"axy": [0, 0, 0]},
            "mobility-parameters": {}
            }
        ]''')

        action = ""
        while action != "quit":
            action = await to_thread(input, "Enter an action (reach_comm, retract_comm, award, move_forward, turn_c, turn_cc, stop) or type 'quit': ")
            if action == "quit":
                break
            elif action == "reach_comm":
                await api.wait_action(reach_action, remove_after=False)
            elif action == "retract_comm":
                await api.wait_action(retract_action, remove_after=False)
            elif action == "award":
                await api.wait_action(award_action, remove_after=False)
            elif action == "move_forward":
                await api.send(move_forward)
            elif action == "turn_c":
                await api.wait_action(turn_clockwise, remove_after=False)
            elif action == "turn_cc":
                await api.wait_action(turn_counterclockwise, remove_after=False)
            elif action == "stop":
                await api.wait_action(stop, remove_after=False)
            else:
                await api.wait_action(default_position, remove_after=False)

asyncio.run(main())
    
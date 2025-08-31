from loader import Loader
from context import Context
from robot import Robot

if __name__ == "__main__":
    """this file is only available for testing purposes in the backend"""
    robot: Robot = Robot()
    loader: Loader = Loader("flaskr/compiler/from_server.json")
    context: Context = Context(loader.get_blocks(), robot)

    for block in loader.get_blocks():
        block._execute(context, robot)
            
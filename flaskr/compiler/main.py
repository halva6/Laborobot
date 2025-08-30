from loader import Loader
from context import Context
from robot import Robot

if __name__ == "__main__":
    robot = Robot()
    loader = Loader("flaskr/compiler/from_server.json")
    context = Context(loader.get_blocks(), robot)

    for block in loader.get_blocks():
        block._execute(context, robot)
            
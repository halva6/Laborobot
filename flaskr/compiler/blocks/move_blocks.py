"""A module that contains the classes representing the blocks responsible for the robot's movement."""

from flaskr.compiler.blocks.block import Block
from flaskr.compiler.context import Context

class MoveBlock(Block):
    """
    moves the robot on three axes around a specific point
    """
    def __init__(self, block_id:str, text:str, variables:list[str], children:list) -> None:
        super().__init__(block_id, text, variables, children, 1) # the last number defines the exact number of expected variables

    def execute(self, context:Context) -> None:
        if self._block_id.startswith("block-steps-x"):
            # since it is specified in advance that each block has an exact number of expected variables,
            # one can therefore directly access the respective variable from the list
            x = context.get_variable(self._variables[0]).to_int()
            context.robot.move_on_axis("X",x)

        if self._block_id.startswith("block-steps-y"):
            y = context.get_variable(self._variables[0]).to_int()
            context.robot.move_on_axis("Y",y)

        if self._block_id.startswith("block-steps-z"):
            z = context.get_variable(self._variables[0]).to_int()
            context.robot.move_on_axis("Z",z)


class ResetPositionBlock(Block):
    """
    resets the position to the predefined starting position
    """
    def __init__(self, block_id:str, text:str, variables:list[str], children:list) -> None:
        super().__init__(block_id, text, variables, children, 0)

    def execute(self, context:Context) -> None:
        context.robot.reset_pos()


class MoveToPositionBlock(Block):
    """
    allows you to move all three axes directly
    """
    def __init__(self, block_id:str, text:str, variables:list[str], children:list):
        super().__init__(block_id, text, variables, children, 3)
        # 3 variables are expected here, but there are actually 0, because the variables of the positions come from the position block.
        # This is because the block in the HTML code belongs to the class 'block-move'. With this class, however, when translating to JSON, all variables (and also all those below) are added.
        # That's why there are expected variables in block 3, although theoretically it shouldn't be like that.
        # It is only due to simplicity. But since the expected variables are constant anyway and are firmly defined in the code, this is not a problem, but only a formality
        self.__p_x:int = None
        self.__p_y:int = None
        self.__p_z:int = None

    def execute(self, context:Context):
        self._execute_children(context)
        context.robot.move_to_position(self.__p_x, self.__p_y, self.__p_z)

    def _execute_children(self, context:Context):
        child:PositionBlock = self._children[0] #this block only have one children
        child.execute(context)

        self.__p_x = child.p_x
        self.__p_y = child.p_y
        self.__p_z = child.p_z


class PositionBlock(Block):
    """
    includes the three values for the respective axes in one
    """
    def __init__(self, block_id:str, text:str, variables:list[str], children:list) -> None:
        super().__init__(block_id, text, variables, children, 3)
        self.__p_x:int = None
        self.__p_y:int = None
        self.__p_z:int = None

    def execute(self, context: Context) -> None:
        self.__p_x:int = context.get_variable(self._variables[0]).to_int()
        self.__p_y:int = context.get_variable(self._variables[1]).to_int()
        self.__p_z:int = context.get_variable(self._variables[2]).to_int()

    @property
    def p_x(self)-> int:
        return self.__p_x

    @property
    def p_y(self)-> int:
        return self.__p_y

    @property
    def p_z(self)-> int:
        return self.__p_z

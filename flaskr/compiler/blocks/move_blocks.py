from compiler.blocks.block import Block
from compiler.context import Context

class MoveBlock(Block):
    def __init__(self, id:str, text:str, variables:list[str], children:list) -> None:
        super().__init__(id, text, variables, children, 1) # the last number defines the exact number of expected variables
    
    def execute(self, context:Context) -> None:
        if self._id.startswith("block-steps-x"):
            # since it is specified in advance that each block has an exact number of expected variables, 
            # one can therefore directly access the respective variable from the list
            x = context.get_variable(self._variables[0]).to_int() 
            context.get_robot().move_x(x)
        
        if self._id.startswith("block-steps-y"):
            y = context.get_variable(self._variables[0]).to_int()
            context.get_robot().move_y(y)

        if self._id.startswith("block-steps-z"):
            z = context.get_variable(self._variables[0]).to_int()
            context.get_robot().move_z(z)

class ResetPositionBlock(Block):
    def __init__(self, id:str, text:str, variables:list[str], children:list) -> None:
        super().__init__(id, text, variables, children, 0)
    
    def execute(self, context:Context) -> None: #only for test purpose
        context.get_robot().reset_pos()

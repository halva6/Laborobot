"""Module representing all the blocks that deal with repeating other blocks"""

from flaskr.compiler.blocks.block import Block
from flaskr.compiler.context import Context

class BreakBlock(Block):
    """
    breaks the loop immediately
    If you encounter it during execution, it becomes active, so to speak.
    The loop checks at each step whether it has been interrupted,
    i.e. whether the BreakBlock is active, if so, then the loop is interrupted
    """
    def __init__(self, block_id: str, text: str, variables: list[str], children: list) -> None:
        super().__init__(block_id, text, variables, children, 0)
        self.__active: bool = False

    def execute(self, context: Context) -> None:
        self.__active = True

    @property
    def is_active(self) -> bool:
        return self.__active

class LoopBlock(Block):
    """
    parent class for the two types of loops, provides the cancellation functionality with break
    """
    def __init__(self, block_id: str, text: str, variables: list[str], children: list, expected_vars:int) -> None:
        super().__init__(block_id, text, variables, children, expected_vars)
        self.__break_blocks:list[BreakBlock] = self.__find_break_childs(children=children)
        self._break: bool = False

    def _execute_children(self, context: Context) -> None:
        for child in self._children:
            child.execute(context)
            if self.__break_blocks != []:
                self._break = self.__is_break_active(self.__break_blocks)


    def __is_break_active(self, break_blocks:list[BreakBlock]) -> True:
        """
        checks if one of the break blocks has been executed
        """
        for break_block in break_blocks:
            if break_block.is_active:
                return True
        return False

    def __find_break_childs(self, children: list[Block]) -> list[BreakBlock]:
        """
        recursively searches for all break blocks that can exist as children
        """
        break_block_lst = []
        for child in children:
            if child.children != []:
                break_block_lst.extend(self.__find_break_childs(child.children))

            if "break" in child.block_id:
                break_block_lst.append(child)
        return break_block_lst
    

class ForBlock(LoopBlock):
    """
    like a for-loop, The children blocks a certain number of times.
    """
    def __init__(self, block_id: str, text: str, variables: list[str], children: list):
        super().__init__(block_id, text, variables, children, 3)

    def execute(self, context: Context):
        for i in range(context.get_variable(self._variables[1]).to_int(), context.get_variable(self._variables[2]).to_int()):
            context.get_variable(self._variables[0]).value = str(i)
            self._execute_children(context)
            if self._break:
                break

class WhileBlock(LoopBlock):
    """
    repeats the children blocks until the loop is manually broken by a break block
    """
    def __init__(self, block_id: str, text: str, variables: list[str], children: list):
        super().__init__(block_id, text, variables, children, 0)
    
    def execute(self, context: Context):
        while not self._break:
            self._execute_children(context)
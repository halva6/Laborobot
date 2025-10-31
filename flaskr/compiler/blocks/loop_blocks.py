"""Module representing all the blocks that deal with repeating other blocks"""

from flaskr.compiler.blocks.block import Block
from flaskr.compiler.context import Context


class RepeatBlock(Block):
    """
    repeats other blocks (like a for-loop)
    """
    def __init__(self, block_id: str, text: str, variables: list[str], children: list) -> None:
        super().__init__(block_id, text, variables, children, 1)
        self.__break_child = self.__find_break_child(children=children)
        self.__break: bool = False

    def execute(self, context: Context) -> None:
        for _ in range(context.get_variable(self._variables[0]).to_int()):
            self._execute_children(context)
            if self.__break:
                break

    def _execute_children(self, context: Context) -> None:
        for child in self._children:
            child.execute(context)
            if (
                not self.__break_child is None
            ):  # checks if the BreakBlock has been executed
                if self.__break_child.is_active():
                    self.__break = True  # if so, this informs the actual loop, in execute() that it should be interrupted immediately
                    break

    def __find_break_child(self, children: list[Block]) -> Block:
        """
        recursively searches if there is a BreakBlock at all
        """
        for child in children:
            if not child.children == []:
                return self.__find_break_child(child.children)

            if "break" in child.block_id:
                return child
        return None


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

    def is_active(self) -> bool:
        """
        returns:
            bool: true if active, false otherwise
        """
        return self.__active

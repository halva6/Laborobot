"""A module containing the blocks that branch the program flow"""

from flaskr.compiler.blocks.block import Block
from flaskr.compiler.context import Context


class IfBlock(Block):
    """
    Block for controlling the program flow, classic if condition
    """

    def __init__(self, block_id: str, text: str, variables: list[str], children: list):
        super().__init__(block_id, text, variables, children, 2)

    def execute(self, context: Context) -> None:
        execute_bool: bool = self._get_execute_bool(context=context)

        if execute_bool:
            self._execute_children(context)

    def _get_execute_bool(self, context: Context) -> bool:
        """
        checks if condition between two variables is met
        args:
            context (Context): the context used to retrieve and compare variable values
        returns:
            bool: true if the condition is met, false otherwise
        """
        execute_bool: bool = False
        if "==" in self._text:
            execute_bool = (context.get_variable(self._variables[0]).to_int() == context.get_variable(self._variables[1]).to_int())
        elif "<=" in self._text:
            execute_bool = (context.get_variable(self._variables[0]).to_int() <= context.get_variable(self._variables[1]).to_int())
        elif ">=" in self._text:
            execute_bool = (context.get_variable(self._variables[0]).to_int() >= context.get_variable(self._variables[1]).to_int())
        elif "<" in self._text:
            execute_bool = (context.get_variable(self._variables[0]).to_int() < context.get_variable(self._variables[1]).to_int())
        elif ">" in self._text:
            execute_bool = (context.get_variable(self._variables[0]).to_int() > context.get_variable(self._variables[1]).to_int())

        return execute_bool


class IfElseBlock(IfBlock):
    """
    Block for controlling the program flow, but with branches,
    classic if-else condition, but not yet implemented in the frontend
    """

    def __init__(self, block_id: str, text: str, variables: list[str], children: list, children_else: list) -> None:
        super().__init__(block_id, text, variables, children)
        self.__children_else = children_else

    def execute(self, context: Context) -> None:
        execute_bool: bool = self._get_execute_bool(context=context)

        if execute_bool:
            self._execute_children(context)
        else:
            self._children = self.__children_else
            self._execute_children(context)

from compiler.blocks.block import Block
from compiler.context import Context

class RepeatBlock(Block):
    def __init__(self, id:str, text:str, variables:list[str], children:list) -> None:
        super().__init__(id, text, variables, children, 1)
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
            if not self.__break_child == None: # checks if the BreakBlock has been executed
                if self.__break_child.is_active():
                    self.__break = True # if so, this informs the actual loop, in execute() that it should be interrupted immediately
                    break

    def __find_break_child(self, children:list) -> Block:
        """recursively searches if there is a BreakBlock at all"""
        for child in children:
            if not child.get_children() == []:
                return self.__find_break_child(child.get_children())
            
            if "break" in child.get_id():
                return child
        return None
    
class BreakBlock(Block):
    def __init__(self, id:str, text:str, variables:list[str], children:list) -> None:
        """breaks the loop immediately
        If you encounter it during execution, it becomes active, so to speak. 
        The loop checks at each step whether it has been interrupted, 
        i.e. whether the BreakBlock is active, if so, then the loop is interrupted"""
        super().__init__(id, text, variables, children, 0)
        self.__active: bool = False

    def execute(self, context:Context) -> None:
        self.__active = True

    def is_active(self) -> bool:
        return self.__active
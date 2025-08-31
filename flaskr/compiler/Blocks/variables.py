from compiler.server_error import FalseTypeError

class Variable():
    def __init__(self, name:str, value:str) -> None:
        self.__name:str = name
        self.__value:int = self.__check_validation(value=value)

    def get_value(self) -> int:
        return self.__value
    
    def get_name(self) -> str:
        return self.__name
    
    def __check_validation(self, value:str) -> int:
        if not value == None:
            if value.isnumeric():
                return int(value)
            else:
                raise FalseTypeError("Variable has the false data type, needed 'int'", self.__name)
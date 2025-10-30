from server_error import FalseTypeError

class Variable():
    def __init__(self, name:str, value:str) -> None:
        self.__name:str = name
        self.__value:str = str(value)

    def get_value(self):
        return self.__value

    def set_value(self, value: str) -> None:
        self.__value = value
    
    def get_name(self) -> str:
        return self.__name
    
    def to_int(self) -> int:
        return self.__check_validation(self.__value)
    
    def __check_validation(self, value:str) -> int:
        if not value == None:
            if value.startswith("-") and value[1:].isnumeric():
                return int(value[1:]) *-1
            elif value.isnumeric():
                return int(value)
            else:
                raise FalseTypeError


                
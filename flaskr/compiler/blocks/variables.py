"""Module that provides the internal variables"""
from flaskr.server_error import FalseTypeError

class Variable():
    """
    This represents the variables
    The variables can be either a string or an integer; 
    other data types are not possible
    """

    def __init__(self, name:str, value:str) -> None:
        self.__name:str = name
        self.__value:str = str(value)

    @property
    def value(self) -> str:
        return self.__value

    @value.setter
    def value(self, value: str) -> None:
        self.__value = value

    @property
    def name(self) -> str:
        return self.__name

    def to_int(self) -> int:
        """
        returns:
            int: int-value of the variable 
                 (because the variable value is actually stored as a string)
        """
        return self.__check_validation(self.__value)

    def __check_validation(self, value:str) -> int:
        """
        checks whether a variable can be converted to an int at all, 
        and whether it is negative or positive
        args:
            value (str): the sting value of the variable
        raises:
            FalseTypeError: if the variable cant convert to a int
        returns:
            int: the final int value        
        """
        if not value is None:
            if value.startswith("-") and value[1:].isnumeric():
                return int(value[1:]) *-1
            elif value.isnumeric():
                return int(value)
            else:
                raise FalseTypeError

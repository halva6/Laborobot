class Variable():
    def __init__(self, name:str, value:str):
        self.__name = name
        self.__value = self.__check_validation(value=value)

    def get_value(self):
        return self.__value
    
    def get_name(self) -> str:
        return self.__name
    
    def __check_validation(self, value:str):
        if not value == None:
            if value.isnumeric():
                return int(value)
            elif value.isdigit():
                return float(value)
            else:
                return str(value)
        else:
            return "None"

import json
from compiler.Blocks.block import *
from compiler.Blocks.variables import Variable

class Loader():
    def __init__(self, file_path:str, soketio) -> None:
        raw_blocks = self.__get_dict_from_json(file_path)
        self.__blocks:list = []
        self.__socketio = soketio

        for raw_block in raw_blocks:
            self.__blocks.append(self.__factory(raw_block))

    
    def __get_dict_from_json(self, file_path:str) -> dict:
        with open(file_path, "r", encoding="utf-8") as json_file:
            return json.load(json_file)
        return {}

    def __factory(self, raw_block):
        block_type = raw_block["type"]

        children = []
        for child in raw_block.get("children", []):
            children.append(self.__factory(child))

        variables:list[Variable] = []
        if not raw_block["variables"] == []:
            for variable in raw_block["variables"]:
                variables.append(Variable(variable["text"],variable["value"]))        


        if block_type == "block-event" and "break" in raw_block["id"]:
            return BreakBlock(id=raw_block["id"], type=block_type, text=raw_block["text"], variables=variables, children=children)
        elif block_type == "block-controll" and "repeat" in raw_block["text"]:
            return RepeatBlock(id=raw_block["id"], type=block_type, text=raw_block["text"], variables=variables, children=children)
        elif block_type == "block-controll" and "if" in raw_block["text"]:
            return IfBlock(id=raw_block["id"], type=block_type, text=raw_block["text"], variables=variables, children=children)
        elif block_type.startswith("block-move") and "steps" in raw_block["id"]:
            return MoveBlock(id=raw_block["id"], type=block_type, text=raw_block["text"], variables=variables, children=children)
        elif block_type.startswith("block-move") and "reset" in raw_block["id"]:
            return ResetPositionBlock(id=raw_block["id"], type=block_type, text=raw_block["text"], variables=variables, children=children)
        elif block_type == "block-debug" and "print" in raw_block["id"]:
            return DebugPrintBlock(id=raw_block["id"], type=block_type, text=raw_block["text"], variables=variables, children=children, socketio=self.__socketio)
        else:
            return Block(id=raw_block["id"], type=block_type, text=raw_block["text"], variables=variables, children=children)
        
    def get_blocks(self)-> list:
        return self.__blocks
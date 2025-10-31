"""Module that offers block assignment"""
import json
from flaskr.compiler.blocks.block import Block, DebugPrintBlock, TimerBlock, CalculationBlock, MeasurementBlock
from flaskr.compiler.blocks.condition_blocks import IfBlock
from flaskr.compiler.blocks.loop_blocks import RepeatBlock, BreakBlock
from flaskr.compiler.blocks.move_blocks import MoveBlock, ResetPositionBlock, MoveToPositionBlock, PositionBlock
from flaskr.compiler.blocks.variables import Variable


class Loader:
    """
    it reads the JSON file coming from the server and assigns a block and the corresponding information to each relevant element
    """
    def __init__(self, file_path: str) -> None:
        """Loader class reads JSON, validates schema, creates concrete block objects"""
        raw_blocks: dict = self.__get_dict_from_json(file_path)
        self.__blocks: list = []

        self.__variable_list: list[Variable] = []

        # recursive approach, since a certain block can have any number of sub-blocks or also called children
        for raw_block in raw_blocks:
            self.__blocks.append(self.__factory(raw_block))

    def __get_dict_from_json(self, file_path: str) -> dict:
        """
        loads and returns a dictionary from a json file
        args:
            file_path (str): path to the json file
        returns:
            dict: dictionary loaded from the json file
        """
        with open(file_path, "r", encoding="utf-8") as json_file:
            return json.load(json_file)
        return {}

    def __factory(self, raw_block: dict) -> Block:
        """
        creates a block object from a raw json dictionary, including its children and variables
        args:
            raw_block (dict): dictionary representing the block data from json
        returns:
            Block: an instance of the appropriate block type based on the block data
        """
        block_type: str = raw_block["type"]

        children: list = []
        for child in raw_block.get("children", []):
            children.append(self.__factory(child))

        variable_name_list: list[str] = []
        if not raw_block["variables"] == []:
            for variable in raw_block["variables"]:
                variable_name_list.append(variable["text"])
                self.__variable_list.append(
                    Variable(variable["text"], variable["value"])
                )

        # gets the blocktype based on typical properties from the JSON dict
        if block_type == "block-event" and "break" in raw_block["id"]:
            return BreakBlock(
                block_id=raw_block["id"],
                text=raw_block["text"],
                variables=variable_name_list,
                children=children,
            )
        elif block_type == "block-controll" and "repeat" in raw_block["text"]:
            return RepeatBlock(
                block_id=raw_block["id"],
                text=raw_block["text"],
                variables=variable_name_list,
                children=children,
            )
        elif block_type == "block-controll" and "if" in raw_block["text"]:
            return IfBlock(
                block_id=raw_block["id"],
                text=raw_block["text"],
                variables=variable_name_list,
                children=children,
            )
        elif block_type.startswith("block-move") and "steps" in raw_block["id"]:
            return MoveBlock(
                block_id=raw_block["id"],
                text=raw_block["text"],
                variables=variable_name_list,
                children=children,
            )
        elif block_type.startswith("block-move") and "reset" in raw_block["id"]:
            return ResetPositionBlock(
                block_id=raw_block["id"],
                text=raw_block["text"],
                variables=variable_name_list,
                children=children,
            )
        elif block_type == "block-debug" and "print" in raw_block["id"]:
            return DebugPrintBlock(
                block_id=raw_block["id"],
                text=raw_block["text"],
                variables=variable_name_list,
                children=children,
            )
        elif block_type == "block-time" and "seconds" in raw_block["id"]:
            return TimerBlock(
                block_id=raw_block["id"],
                text=raw_block["text"],
                variables=variable_name_list,
                children=children,
                time_multiplier=1,
            )
        elif block_type == "block-time" and "minutes" in raw_block["id"]:
            return TimerBlock(
                block_id=raw_block["id"],
                text=raw_block["text"],
                variables=variable_name_list,
                children=children,
                time_multiplier=60,
            )
        elif block_type.startswith("block-move") and "to-pos" in raw_block["id"]:
            return MoveToPositionBlock(
                block_id=raw_block["id"],
                text=raw_block["text"],
                variables=variable_name_list,
                children=children,
            )
        elif block_type == "block-pos":
            return PositionBlock(
                block_id=raw_block["id"],
                text=raw_block["text"],
                variables=variable_name_list,
                children=children,
            )
        elif block_type == "block-calc":
            return CalculationBlock(
                block_id=raw_block["id"],
                text=raw_block["text"],
                variables=variable_name_list,
                children=children,
            )
        elif block_type == "block-measure":
            return MeasurementBlock(
                block_id=raw_block["id"],
                text=raw_block["text"],
                variables=variable_name_list,
                children=children,
            )
        else:
            return Block(
                block_id=raw_block["id"],
                text=raw_block["text"],
                variables=variable_name_list,
                children=children,
                expected_vars=0,
            )

    @property
    def blocks(self) -> list[Block]:
        return self.__blocks

    @property
    def variables(self) -> list[Variable]:
        return self.__variable_list

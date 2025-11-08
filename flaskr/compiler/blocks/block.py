"""Module which includes the parent block and all other blocks"""

import time
import threading
import asyncio
from flaskr.compiler.context import Context
from flaskr.compiler.blocks.variables import Variable
from flaskr.server_error import ExpectVariableError, BlockNotImpelentedError
from flaskr.measurement import GoDirectDataCollector

class Block:
    """
    Block class is the parent class of each block
    and provides the corresponding functionalities

    Functions and variables that start
    with _ are protected and functions and variables
    with __ are private,
    the rest is public
    """

    def __init__(self, block_id: str, text: str, variables: list[str], children: list, expected_vars: int) -> None:
        self._block_id: str = block_id
        self._text: str = text
        self._variables: list[str] = variables
        self._children: list[Block] = children
        self.__validate_vars(expected_vars)

    def __validate_vars(self, expected_vars: int) -> None:
        """
        validates if the number of variables matches the expected count
        args:
            expected_vars (int): the expected number of variables
        raises:
            ExpectVariableError: if the number of variables doesn't match the expected count
        """
        if not len(self._variables) == expected_vars:
            raise ExpectVariableError(
                "Expected variables but got none", block_id=self._block_id
            )

    def execute(self, context: Context) -> None:
        """
        raises a NotImplementedError, meant to be overridden by subclasses
        args:
            context (Context): the context to be passed when the method is implemented
        """
        raise BlockNotImpelentedError(message="block is defined (not as a standalone block)", block_id=self._block_id)

    def _execute_children(self, context: Context) -> None:
        """
        executes the execute method for each child in the _children list
        args:
            context (Context): the context to pass to each child's execute method
        """
        for child in self._children:
            child.execute(context)

    @property
    def variables_names(self) -> list[str]:
        return self._variables

    @property
    def children(self) -> list:
        return self._children

    @property
    def block_id(self) -> str:
        return self._block_id

    def __str__(self) -> str:
        return str(self._block_id)


class DebugPrintBlock(Block):
    """
    Block for outputting arbitrary values to the client's console
    """

    def execute(self, context: Context) -> None:
        """
        sends data to the frontend, which is to be output in the console there,
        with the corresponding variable values
        args:
            context (Context): the context used to retrieve variable values and interact with
                               the socket io
        """
        if not self._variables == []:
            send_str: str = "[DEBUG] "
            for var in self._variables:
                send_str += context.get_variable(var).value + " | "

            if len(self._variables) == 1:
                send_str = send_str.replace("|", "")
        
            context.socket_io.emit(
                "update",
                {
                    "data": send_str
                },
            )
            print(send_str)


class TimerBlock(Block):
    """
    block for stopping the program at a specific time;
    can be used to time experiments
    """

    def __init__(self, block_id: str, text: str, variables: list[str], children: list, time_multiplier: int) -> None:
        super().__init__(block_id, text, variables, children, 1)
        self.__time_multiplier = time_multiplier

    def execute(self, context: Context):
        """
        pauses the execution for a duration based on the first variable's value
        and a time multiplier
        args:
            context (Context): the context used to retrieve the variable value
        """
        time.sleep(
            context.get_variable(self._variables[0]).to_int() * self.__time_multiplier
        )


class CalculationBlock(Block):
    """
    Block for calculating with variables;
    Possible operations: +, -, *, /, mod,
    bitwise and, bitwise or, bitwise xor, bitwise not, left shift, right shift
    """

    def __init__(self, block_id: str, text: str, variables: list[str], children: list) -> None:
        super().__init__(block_id, text, variables, children, 3)

    def execute(self, context:Context) -> None:
        """
        performs a calculation based on the operator in _text and updates the first variable's value
        args:
            context (Context): the context used to retrieve and update variable values
        """
        calc_var: Variable = context.get_variable(self._variables[0])
        value: int = calc_var.to_int()

        arg1: int = context.get_variable(self._variables[1]).to_int()
        arg2: int = context.get_variable(self._variables[2]).to_int()

        # other characters, besides those shown, that can still be used in variable naming
        # + --> {
        # - --> }
        # * --> [

        if "{" in self._text:
            value = arg1 + arg2
        elif "}" in self._text:
            value = arg1 - arg2
        elif "[" in self._text:
            value = arg1 * arg2
        elif "/" in self._text:
            value = int(arg1 / arg2)
        elif "%" in self._text:
            value = arg1 % arg2
        elif "&" in self._text:
            value = arg1 & arg2
        elif "|" in self._text:
            value = arg1 | arg2
        elif "^" in self._text:
            value = arg1 ^ arg2
        elif "~" in self._text:
            # Yes, this is a special case,
            # because theoretically you have to specify two variable values here,
            # but you only need one
            # --> which makes it a little cumbersome,
            # because you can simply give it a random value, since arg1 doesn't matter
            value = ~arg2
        elif "<<" in self._text:
            value = arg1 << arg2
        elif "<<" in self._text:
            value = arg1 >> arg2

        calc_var.value = str(value)


class MeasurementBlock(Block):
    """
    block for recording measurement data
    runs on a different thread
    """
    def __init__(self, block_id: str, text: str, variables: list[str], children: list) -> None:
        super().__init__(block_id, text, variables, children, 0)
        self.__is_measurement_running: bool = False

    def execute(self, context:Context) -> None:
        """
        starts a new thread to run the measurement if it's not already running
        args:
            context (Context): not used
        """
        if not self.__is_measurement_running:
            measurement_thread = threading.Thread(target=self.__run_measurement)
            measurement_thread.start()

    def __run_measurement(self) -> None:
        """
        runs the measurement in a new asyncio event loop and collects data

        sets the measurement as running, starts the data collection, 
        and closes the event loop when finished
        """
        self.__is_measurement_running = True

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)  # Set the event loop for this thread

        collector = GoDirectDataCollector()
        collector.run()
        self.__is_measurement_running = False
        loop.close()  # Close the loop when done

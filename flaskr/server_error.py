"""A module that contains all errors that can occur when using the program, manages them, and makes them visible to the client"""
import traceback
from flask_socketio import SocketIO

class ServerError(Exception):
    """this is the basis for all errors that arise from user code."""
    def __init__(self, message:str, block_id:str=None, error_code=None):
        self.message:str = message
        self.block_id:str = block_id
        self.error_code = error_code or self.__class__.__name__
        super().__init__(message)


class FalseTypeError(ServerError):
    """
    if the specified type does not match the required type
    """

class BlockNotImpelentedError(ServerError):
    """
    This error occurs if the block has not been implemented. 
    This error occurs because you should only inherit from blocks.
    """

class ExpectVariableError(ServerError):
    """
    if too few variables were specified
    """

class VariableNoneTyeError(ServerError):
    """
    if the variable is undefined, or if it is nothing
    """

class RobotPositionError(ServerError):
    """
    if the specified value exceed the physical possibilities of the robot's movement
    """

class DiviceNotFoundError(ServerError):
    """
    if no device is found
    """

class NoDeviceConnected(ServerError):
    """
    when no device is connected
    """

class ExecutionStartedError(ServerError):
    """
    when the program is already running, but an attempt is made to run the program again even though it has not yet finished
    """

class ErrorManager:
    """
    manages the error and sends it to the client in the appropriate format
    """
    _instance = None

    def __init__(self, socketio:SocketIO) -> None:
        self.socketio:SocketIO = socketio

    @classmethod
    def init(cls, socketio:SocketIO) -> None:
        """Initialize the ErrorManager with a SocketIO instance."""
        cls._instance = cls(socketio)

    @classmethod
    def report(cls, error: Exception) -> None:
        """Report an error to the frontend via SocketIO."""
        print(traceback.print_exception(error))
        if cls._instance is None:
            raise RuntimeError("ErrorManager has not been initialized. Call ErrorManager.init(socketio).")

        if isinstance(error, ServerError):
            cls._instance.socketio.emit("execution_error", {
                "error": error.message,
                "block_id": getattr(error, "block_id", None),
                "error_code": error.error_code
            })
        else:
            # Fallback for unexpected errors
            cls._instance.socketio.emit("execution_error", {
                "error": f"Internal Server Error: {str(error)}",
                "error_code": "InternalError"
            })

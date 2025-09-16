from flask_socketio import SocketIO

import traceback

class ServerError(Exception):
    """Basis für alle Fehler, die durch User-Code entstehen."""
    def __init__(self, message:str, block_id:str=None, error_code=None):
        self.message:str = message
        self.block_id:str = block_id
        self.error_code = error_code or self.__class__.__name__
        super().__init__(message)


class FalseTypeError(ServerError):
    pass

class ExpectVariableError(ServerError):
    pass

class VariableNoneTyeError(ServerError):
    pass

class RobotPositionError(ServerError):
    pass

class ErrorManager:
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

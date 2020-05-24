

class TvdbClientException(Exception):
    def __init__(self, message: str, instructions: str = "") -> None:
        super().__init__(message, instructions)
        self.message = message
        self.instructions = instructions

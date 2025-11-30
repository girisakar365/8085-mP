
from abc import ABC, abstractmethod
from typing import Dict, Callable
from .logs import setup_logger, error
setup_logger()

class Instruction(ABC):
    def __getitem__(self, key: str) -> Callable | None:
        try:
            return self.get_inst()[key]
        except KeyError:
            error(f"Instruction '{key}' not found.")

    @abstractmethod
    def get_inst(self) -> Dict[str, Callable]:
        pass

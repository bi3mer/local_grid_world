from dataclasses import dataclass
from typing import Tuple, List

@dataclass
class Edge:
    src: Tuple[int, int]
    tgt: Tuple[int, int]
    probability: List[Tuple[Tuple[int, int], float]]
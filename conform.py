import random
# This is imported because this python version doesn't support OR operators for function parameter typing.
from typing import Union

from agent import ParentAgent

class ConformingAgent(ParentAgent):
    def __init__(self, group_str, threshold: Union[float, None] = 0.1, x: int = -1, y: int = -1):
        if(threshold is None):
            threshold = round(random.uniform(0.5, 0.7), 2)

        super().__init__(group_str, threshold, x, y)
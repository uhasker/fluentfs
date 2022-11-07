import re
from typing import List, Union


def compile_regex(regex: Union[str, List[str]]) -> List[re.Pattern]:
    if isinstance(regex, str):
        regex = [regex]

    return [re.compile(r) for r in regex]

import re
from typing import Any
from datetime import datetime

def parse_variable(variable: str, root_dict: dict[str, Any]) -> Any:
    if variable == "null":
        return None
    if variable == "true":
        return True
    if variable == "false":
        return False
    if variable == "[]":
        return []
    if variable == "{}":
        return {}
    if re.match(r"^\d+$", variable):
        return int(variable)
    if re.match(r"^\d+\.\d+$", variable):
        return float(variable)
    if r := re.match(r"^(['\"])(.*)\1$", variable):
        return r.group(2)
    if r := re.match(r"^new Date\((\d+)\)$", variable):
        return datetime.fromtimestamp(int(r.group(1)) / 1000.0)
    if re.match(r"^s\d+$", variable):
        return root_dict[variable]
    return {}


def parse_dwr(string: str) -> dict[str, Any]:
    output: dict[str, Any] = {}
    string = string.replace(";", "\n")
    lines = string.splitlines()
    for line in lines:
        line = line.strip()
        if not line or line.startswith("//") or line.startswith("dwr."):
            continue
        if r := re.search(r"^var (s\d+)=(.*)", line):
            output[r.group(1)] = parse_variable(r.group(2), output)
            continue
        key: int | str
        if r := re.search(r"^(s\d+)\[(\d+)]=(.*)", line):
            array = output[r.group(1)]
            key = int(r.group(2))
            value = parse_variable(r.group(3), output)
            assert key <= len(array)
            if key < len(array):
                array[key] = value
            else:
                array.append(value)
            continue
        if r := re.search(r"^(s\d+)\.([^=]+)=(.*)", line):
            array = output[r.group(1)]
            key = r.group(2)
            value = parse_variable(r.group(3), output)
            array[key] = value
            continue
    return output
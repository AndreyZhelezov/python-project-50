import os
import yaml
import json
from yaml.loader import SafeLoader


def parse_data(file_path):
    _, ext = os.path.splitext(file_path)
    if ext in ['.json']:
        return json.load(open(file_path))
    if ext in ['.yaml', '.yml']:
        return yaml.load(open(file_path), Loader=SafeLoader)

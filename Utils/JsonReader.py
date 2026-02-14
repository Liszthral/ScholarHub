"""
    CopyRight: Liszthral
    Email: 2239288228@qq.com
    Project: ScholarHub - Utils - JsonReader
    Version: Release 1.0.1
    UpdateTime: 2026-0213-2130
"""

import json

class JsonReader:
    """
    :param [logger]: Log objects shared with the main program.
    """
    config = {}

    def __init__(self, path, logger):
        try:
            self.logger = logger
            self.path = path
            with open(f"{self.path}", 'r', encoding='utf-8-sig') as f:
                self.config = json.load(f)
            self.logger.info('Reading config file successfully.')
        except FileNotFoundError:
            self.logger.error(f"Not found file -> path={self.path}")

    def get(self, kind, *args):
        result = self.config.get(kind)
        for arg in args:
            if (isinstance(result, dict)) and (arg in result):
                result = result[arg]
            else:
                return None
        return result

    def configuration(self, kind, aim, *args):
        if kind not in self.config:
            return None
        parent = self.config[kind]
        if len(args) == 0:
            self.config[kind] = aim
            return True
        for arg in args[:-1]:
            if (isinstance(parent, dict)) and (arg in parent):
                parent = parent[arg]
            else:
                return None
        target = args[-1]
        if isinstance(parent, dict):
            parent[target] = aim
            return True
        else:
            return None

    def save(self):
        with open(f"{self.path}", 'w', encoding='utf-8-sig') as f:
            json.dump(self.config, f, ensure_ascii=False, indent=4)

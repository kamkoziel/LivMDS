import json

CONFIG_PATH = 'res/config.json'
CACHE_PATH = 'res/.cache.json'


class Config:
    @staticmethod
    def get_all(config_path=CONFIG_PATH):
        with open(config_path) as config_file:
            config_data = json.load(config_file)

        return config_data

    @staticmethod
    def get(key, config_path=CONFIG_PATH):
        with open(config_path) as config_file:
            config_data = json.load(config_file)

        return config_data.get(key, '')

    @staticmethod
    def update(key: str, value, config_path=CONFIG_PATH):
        with open(config_path) as config_file:
            config_data = json.load(config_file)
        config_data.update({key: value})

        with open(config_path, 'w') as fp:
            json.dump(config_data, fp, indent=4)

class Cache:
    @staticmethod
    def get(key, cache_path=CACHE_PATH):
        with open(cache_path) as cache_file:
            cache_data = json.load(cache_file)
        return cache_data[key]



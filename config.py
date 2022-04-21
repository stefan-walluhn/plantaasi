import uio as io
import ujson as json


def load_config(config_file='config.json'):
    with io.open(config_file) as cf:
        return json.load(cf)


config = load_config()

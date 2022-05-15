import codecs
import json
import logging.config
import os


with codecs.open(
    f"{os.path.dirname(__file__)}/logging_config.json", "r", encoding="utf-8-sig"
) as fd:
    logging.config.dictConfig(json.load(fd))


LOGGING_LEVEL = os.environ.get("LOGGING_LEVEL", "DEBUG").upper()

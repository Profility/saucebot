import logging
from ruamel.yaml import YAML 

log = logging.getLogger()
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s:%(levelname)s:%(name)s: %(message)s'
)

with open("config.yml", "r") as conf:
    try:
        config = YAML().load(conf)
    except Exception as e:
        log.error(f"Failed to load configuration: {e}")
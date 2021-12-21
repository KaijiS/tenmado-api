import logging
import yaml

# loggerの設定
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def read_yaml(filepath: str):
    """
    Yamlファイル読み込み
    """
    with open(filepath) as file:
        yml = yaml.safe_load(file)
    return yml

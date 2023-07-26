from functools import cache
from python_clean_arch.infra.config import ENV, Configs, TestConfigs


@cache
def get_config():
    configs = Configs()
    if ENV == "test":
        configs = TestConfigs()
    return configs

from typing import Dict, List
from omegaconf import DictConfig, OmegaConf


class Configuration:
    config: DictConfig = None

    @classmethod
    def load_config(cls, file: str = None, profile: str = "defaults") -> DictConfig:
        if not cls.config:
            config_loader = OmegaConf.load(file)
            defaults_cfg = config_loader.get("defaults", {})
            profile_cfg = config_loader.get(profile, {})
            cls.config = OmegaConf.merge(defaults_cfg, profile_cfg)
        return cls.config

    @classmethod
    def property_value(cls, property_name: str):
        """
        Usage: decorate a given method with @property_value("property_name")
        Since variables cannot be decorated directly,
        it's preferable to set them through the setter methods. e.g.:

        @property
        def endpoint(self):
            return self.__endpoint

        @endpoint.setter:
        @property_value("vault.endpoint")
        def variable(self, data):
            self.__endpoint = data
        """

        def fn_call_wrapper(fn):
            def fn_args_wrapper(*args, **kwargs):
                value: str = cls.get_property(property_name)
                return fn(args[0], value=value)

            return fn_args_wrapper

        return fn_call_wrapper

    @classmethod
    def get_property(cls, property_name: str) -> str:
        properties: List[str] = property_name.split(".")
        return cls._lookup_property(properties, config={})

    @classmethod
    def _lookup_property(cls, properties: List[str], config=None) -> str:
        head, *tail = properties
        if tail:
            cfg = config.get(head, Configuration.config.get(head))
            return cls._lookup_property(properties=tail, config=cfg)
        else:
            return config.get(head)

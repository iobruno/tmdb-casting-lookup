from typing import Dict, List
from omegaconf import DictConfig, OmegaConf


class Configuration:
    config: DictConfig = None

    @classmethod
    def load_config(cls, file: str = None, profile: str = "default") -> DictConfig:
        if cls.config:
            return cls.config
        else:
            config_loader = OmegaConf.load(file)
            defaults_cfg = config_loader.get("defaults", {})
            profile_cfg = config_loader.get(profile)
            cls.config = OmegaConf.create(
                cls._merge(defaults=defaults_cfg, overwrite_with=profile_cfg)
            )
            return cls.config

    @classmethod
    def _merge(cls, defaults: Dict, overwrite_with: Dict) -> Dict:
        merged = dict(defaults)
        for key, value in overwrite_with.items():
            if key in defaults:
                merged[key] = cls._merge(defaults[key], overwrite_with[key])
            else:
                return {**defaults, **overwrite_with}

        return merged

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

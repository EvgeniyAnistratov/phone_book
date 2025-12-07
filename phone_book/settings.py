from enum import Enum

from envparse import env, ConfigurationError


class ImproperlyConfigured(Exception):
    pass


class ConfigVarType(Enum):
    BOOL = 'BOOL'
    INT = 'INT'
    STR = 'STR'
    LIST_STR = 'LIST_STR'


def read_variable(
    name, v_type: ConfigVarType = ConfigVarType.STR, default: str | int | list[str] = None, required: bool = True
) -> str | int | list[str] | bool:
    if v_type == ConfigVarType.STR:
        value = env.str(name, default=default)
    elif v_type == ConfigVarType.LIST_STR:
        value = env(name, cast=list, subcast=str, default=default)
    elif v_type == ConfigVarType.BOOL:
        value = env.bool(name, default=default)
    elif v_type == ConfigVarType.INT:
        try:
            value = env.int(name, default=default)
        except ConfigurationError as e:
            if 'invalid literal for int()' in str(e):
                raise ImproperlyConfigured(f'Environment variable "{name}" is wrong.')
            else:
                raise e
    else:
        raise ImproperlyConfigured(f'Unknown v_type "{v_type}" while reading {name} variable.')
    if (value is None or value == '') and required:
        raise ImproperlyConfigured(f'Environment variable "{name}" is required.')
    return value


REDIS_HOST = read_variable('REDIS_HOST', ConfigVarType.STR, default='redis', required=False)
REDIS_PORT = read_variable('REDIS_PORT', ConfigVarType.INT, default=6379, required=False)

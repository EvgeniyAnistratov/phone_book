from python_utils.settings import read_variable, ConfigVarType


REDIS_HOST = read_variable('REDIS_HOST', ConfigVarType.STR, default='redis', required=False)
REDIS_PORT = read_variable('REDIS_PORT', ConfigVarType.INT, default=6379, required=False)

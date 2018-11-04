from nameko.extensions import DependencyProvider
from redis import StrictRedis


REDIS_CONFIG = 'REDIS'


class Redis(DependencyProvider):
    """
    Provides a Redis connector to the Nameko service
    """

    def __init__(self):
        self._client = None
        self._config = None

    def setup(self):
        self._config = self.container.config[REDIS_CONFIG]

    def start(self):
        self._client = StrictRedis(**self._config)

    def get_dependency(self, worker_ctx):
        return self._client

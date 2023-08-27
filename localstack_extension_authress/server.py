import logging
from localstack import config
from typing import Optional

from localstack.utils.container_utils.container_client import (
    ContainerClient,
    ContainerConfiguration,
)
from localstack.utils.docker_utils import DOCKER_CLIENT
from localstack.utils.serving import Server
from localstack.utils.sync import poll_condition

LOG = logging.getLogger('Authress.ContainerServer')
if config.DEBUG:
    LOG.setLevel(level=logging.DEBUG)
else:
    LOG.setLevel(level=logging.INFO)

class ContainerServer(Server):
    client: ContainerClient
    config: ContainerConfiguration

    container_id: Optional[str]

    def __init__(
        self,
        port: int,
        config: ContainerConfiguration,
        host: str = "localhost",
        client: ContainerClient = None,
    ) -> None:
        super().__init__(port, host)
        self.config = config
        self.client = client if client else DOCKER_CLIENT
        self.container_id = None

    def is_up(self) -> bool:
        if not self.is_container_running():
            return False
        return super().is_up()

    def is_container_running(self) -> bool:
        if not self.config.name:
            return False
        return self.client.is_container_running(self.config.name)

    def wait_is_container_running(self, timeout=None) -> bool:
        return poll_condition(self.is_container_running, timeout)

    def do_run(self):
        if self.client.is_container_running(self.config.name):
            raise ValueError(f"Container named {self.config.name} already running")
        
        self.container_id = self.client.create_container_from_config(self.config)
        LOG.debug("Container '%s' created to run API.", self.container_id)
        self.client.start_container(self.container_id)
        # re-configure host now that the network ip is known
        self._host = self.get_network_ip()

    def get_network_ip(self) -> str:
        try:
            inspect = self.client.inspect_container(self.container_id)
            host = inspect["NetworkSettings"]["IPAddress"]
            self._host = host
            return host
        except:
            return None
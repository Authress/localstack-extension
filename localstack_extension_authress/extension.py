import logging
import threading
import time
from typing import Optional

from localstack import config, constants
from localstack.extensions.api import Extension, aws, http
from localstack.utils.container_utils.container_client import ContainerConfiguration
from localstack.utils.strings import short_uid

from localstack_extension_authress.server import ContainerServer

LOG = logging.getLogger(__name__)
LOG.setLevel(level=logging.INFO)


class AuthressExtension(Extension):
    name = "localstack-extension-authress"

    server: Optional[ContainerServer]
    proxy: Optional[http.ProxyHandler]

    def __init__(self):
        self.server = None
        self.proxy = None

    def on_extension_load(self):
        """
        Called when LocalStack loads the extension.
        """

        if config.DEBUG:
            LOG.setLevel(level=logging.DEBUG)
        
        LOG.debug("[Authress] ****************** on_extension_load ******************")

    def on_platform_start(self):
        """
        Called when LocalStack starts the main runtime.
        """
        
        LOG.debug("[Authress] ****************** on_platform_start ******************")

        # volumes = VolumeMappings()
        # if localstack_volume := get_default_volume_dir_mount():
        #     models_source = os.path.join(localstack_volume.source, "cache", "authress", "models")
        #     volumes.append(VolumeBind(models_source, "/build/models"))
        # else:
        #     LOG.warning("no volume mounted, will not be able to store access records")

        server = ContainerServer(
            8888,
            ContainerConfiguration(
                image_name="ghcr.io/authress/authress-local:latest",
                name=f"localstack-authress-{short_uid()}",
                # volumes=volumes,
                env_vars={
                    # "ENV_NAME": "VALUE",
                },
            ),
        )
        self.server = server
        LOG.info("starting up %s as %s", server.config.image_name, server.config.name)
        server.start()

        def _update_proxy_job():
            # wait until container becomes available and then update the proxy to point to that IP
            i = 1

            while True:
                if self.proxy:
                    if self.server.get_network_ip():
                        LOG.info("serving Authress API on http://authress.%s:%s",
                            constants.LOCALHOST_HOSTNAME,
                            config.get_edge_port_http(),
                        )
                        self.proxy.proxy.forward_base_url = self.server.url
                        break

                time.sleep(i ** 2)
                i += 1

        threading.Thread(target=_update_proxy_job, daemon=True).start()

    def on_platform_shutdown(self):
        """
        Called when LocalStack is shutting down. Can be used to close any resources (threads, processes, sockets, etc.).
        """
        
        LOG.debug("[Authress] ****************** on_platform_shutdown ******************")

        if self.server:
            self.server.shutdown()
            self.server.client.remove_container(self.server.config.name)

    def update_gateway_routes(self, router: http.Router[http.RouteHandler]):
        """
        Called with the Router attached to the LocalStack gateway. Overwrite this to add or update routes.
        :param router: the Router attached in the gateway
        """
        LOG.info("setting up proxy to %s", self.server.url)
        self.proxy = http.ProxyHandler(forward_base_url=self.server.url)

        # hostname aliases
        router.add(
            "/",
            host="authress.<host>",
            endpoint=self.proxy,
        )
        router.add(
            "/<path:path>",
            host="authress.<host>",
            endpoint=self.proxy,
        )

    def update_request_handlers(self, handlers: aws.CompositeHandler):
        """
        Called with the custom request handlers of the LocalStack gateway. Overwrite this to add or update handlers.
        :param handlers: custom request handlers of the gateway
        """
        
        LOG.debug("[Authress] ****************** update_request_handlers ******************")
        pass

    def update_response_handlers(self, handlers: aws.CompositeResponseHandler):
        """
        Called with the custom response handlers of the LocalStack gateway. Overwrite this to add or update handlers.
        :param handlers: custom response handlers of the gateway
        """
        
        LOG.debug("[Authress] ****************** update_response_handlers ******************")
        pass
    
    def on_platform_ready(self):
        """
        Called when LocalStack is ready and the Ready marker has been LOG.debuged.
        """
        
        LOG.debug("[Authress] ****************** on_platform_ready ******************")
        pass

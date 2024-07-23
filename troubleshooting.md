##

Try running the command directly to start docker:

```sh
docker run --rm --name localstack_main -v ~/.cache/localstack-cli/license.json:/etc/localstack/conf.d/license.json:ro -v ~/.cache/localstack-cli/machine.json:/var/lib/localstack/cache/machine.json:ro -v /tmp/localstack-2_2_1_dev20230812232603-entrypoint.sh:/usr/local/bin/docker-entrypoint-dev.sh:ro -v ~/.cache/localstack/volume:/var/lib/localstack -v /var/run/docker.sock:/var/run/docker.sock -p 127.0.0.1:443:443 -p 127.0.0.1:4566:4566 -p 127.0.0.1:4510-4559:4510-4559 -e LOCALSTACK_AUTH_TOKEN=LOCALSTACK_AUTH_TOKEN -e EXTENSION_DEV_MODE=1 -e ACTIVATE_PRO=1 -e LOCALSTACK_CLI=1 -e DEBUG=1 -e DOCKER_HOST=unix:///var/run/docker.sock -e SET_TERM_HANDLER=1 --expose 53 --expose 53/udp localstack/localstack-pro --entrypoint docker-entrypoint-dev.sh
```
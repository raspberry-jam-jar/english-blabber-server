# english-blabber-server

### Installation
1. Clone the repository.
    ```bash
    https://github.com/raspberry-jam-jar/english-blabber-server.git --depth 1
    ```
2. Enable default server configuration.
    ```bash
    cd english-blabber-server/docker
    cp .env.template .env
    ```
3. Run Docker containers.
    ```bash
    cd english-blabber-server/docker
    docker-compose up -d
    ```
    If you use default configuration server is now available at `https://0.0.0.0:8001`.

Use `docker-compose down` command to stop containers.

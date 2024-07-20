<div align="center">

<img height="120px" src="./resources/imgs/wn.png" alt="WebNav" />

A privacy-first, lightweight website navigation service developed based on the Python framework PyWebIO.

<a href="https://github.com/waisaa/web-nav">Home Page</a> •
<a href="https://blog.csdn.net/qq_42761569?type=blog">Blogs</a>

[![](https://img.shields.io/badge/webui-webnav-9cf.svg)](http://localhost:7777/) [![](https://img.shields.io/badge/document-pywebio-blue.svg)](https://pywebio.readthedocs.io/) [![](https://img.shields.io/badge/license-MIT-brightgreen.svg)](https://github.com/waisaa/web-nav/tree/main/LICENSE)

</div>

![demo](./resources/imgs/webnav.png)

## Key points

- **Open source and free to use**. Embrace a future where creativity knows no boundaries with our open-source solution. All features are free to use and will never be charged in any form or content.
- **Self-hosting with Docker in just seconds**. Enjoy the flexibility, scalability, and ease of setup that Docker provides, allowing you to have full control over your data and privacy.
- **Customize your preferences**. With our intuitive customizing features, you can easily personalize your favorite themes and wallpapers.
- **Usage with embedded MySQL.** I would recommend using a Docker `volume` or `bind` mount for persistent data like shown in the examples below.

## Quick installation

#### Prerequisites
- Git
- Docker
- Docker Compose

#### Deploy with Docker Compose in seconds
- Get the source code
```sh
git clone https://github.com/waisaa/web-nav.git
```
- Enter the directory
```sh
cd web-nav/
```
- Build images of all services and start all services in detached mode
```sh
docker-compose up --build -d
```

#### Remove installation
- Stop and remove containers, networks, volumes, and images associated with the Docker Compose.
```sh
docker-compose down
```

> [!NOTE]
> This command is only applicable for Unix/Linux systems.
>
> The `./mysql/data` directory should be used as the data directory on your local machine, while `/var/lib/mysql` is the directory of the volume in Docker and should not be modified.

## Contribution

Contributions are what make the open-source community such an amazing place to learn, inspire, and create. We greatly appreciate any contributions you make. Thank you for being a part of our community! 🥰

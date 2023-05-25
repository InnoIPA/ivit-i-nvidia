![COVER](assets/images/iVIT-I-Logo-B.png)

# iVIT-I-Nvidia
iVIT-I is an AI inference tool which could support multiple AI framework and this repository is just for Nvidia platform.

* [Requirements](#requirements)
* [Getting Start](#getting-start)

# Requirements
* [Docker 20.10 + ](https://docs.docker.com/engine/install/ubuntu/)
* [Docker-Compose v2.15.1 ](https://docs.docker.com/compose/install/linux/#install-using-the-repository)
    * you can check via `docker compose version`
* NVIDIA gpu driver ( 430+ )
* Install [nvidia-docker2](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/install-guide.html)
# Getting Start
1. Clone Repository
    
    * Donwload Newest Version
        ```bash
        git clone  https://github.com/InnoIPA/ivit-i-nvidia.git && cd ivit-i-nvidia
        ```

2. Run iVIT-I Docker Container

    * Run CLI container
        ```bash
        sudo ./docker/run.sh

        "USAGE: ./docker/run.sh -h" << EOF
        Run the iVIT-I environment.

        Syntax: scriptTemplate [-bqh]
        options:
        b               run in background
        q               Qucik launch iVIT-I
        h               help.
        >>p.
        ```
3. Run Samples

    * [Source Sample](samples/ivit_source_sample/README.md)
    * [Displayer Sample](samples/ivit_displayer_sample/README.md)
    * [Classification Sample](samples/classification_sample/README.md)
    * [Object Detection Sample](samples/object_detection_sample/README.md)
    * [iDevice Sample](samples/ivit_device_sample/README.md)

# Python Library Documentation

[iVIT-I-nvidia API Docs](https://innoipa.github.io/ivit-i-nvidia/)


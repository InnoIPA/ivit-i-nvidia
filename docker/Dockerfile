# ivit-i-nvidia

FROM nvcr.io/nvidia/tensorrt:21.03-py3

WORKDIR /workspace

COPY ["./utils.sh", "./requirements.sh", "./patch_pose.sh", "/workspace/" ]

ENV DEBIAN_FRONTEND noninteractive  

RUN chmod u+x ./*.sh \
&& ./requirements.sh \
&& ./patch_pose.sh \
&& rm ./*.sh

ENTRYPOINT [ "/bin/bash", "-c" ]

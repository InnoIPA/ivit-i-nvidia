# ivit-i-nvidia
FROM nvcr.io/nvidia/tensorrt:21.03-py3
ENV WS=/workspace
ENV DEBIAN_FRONTEND=noninteractive  

USER root
WORKDIR ${WS}
COPY ["./utils.sh", "./requirements.sh", "./patch_pose.sh", "./entrypoint", "${WS}/" ]

# Install requirement
RUN chmod u+x ./*.sh \
&& ./requirements.sh \
&& ./patch_pose.sh 

COPY [ "./inno_verify", "./entrypoint",  "/usr/bin/" ]

ENTRYPOINT [ "entrypoint" ]
FROM nvcr.io/nvidia/tensorrt:21.03-py3
# ------------------------------------------------------------------
WORKDIR /workspace
COPY ["./utils.sh", "./requirements.sh", "./patch_pose.sh", "/workspace/" ]
# ------------------------------------------------------------------
# 由於 安裝套件有互動界面會導致報錯 所以先行關閉
ENV DEBIAN_FRONTEND noninteractive  
RUN chmod +x ./requirements.sh \
&& ./requirements.sh \
&& chmod +x ./patch_pose.sh \
&& ./patch_pose.sh \
&& rm ./*.sh

# ------------------------------------------------------------------
ENTRYPOINT [ "/bin/bash", "-c" ]
ARG BASE_IMAGE=ubuntu:24.04

FROM $BASE_IMAGE

ARG MASTER=0
ARG CUDA=0
#ARG USER_ID
#ARG GROUP_ID

WORKDIR /tmp/

COPY buildInDocker.sh buildInDocker.sh
COPY libs libs

#RUN /tmp/buildInDocker.sh --cuda $CUDA --user_id $USER_ID --group_id $GROUP_ID --master $MASTER && rm /tmp/buildInDocker.sh
RUN ./buildInDocker.sh --cuda $CUDA --master $MASTER && rm buildInDocker.sh

#USER user

# Add binaries to path
ENV PATH /usr/local/bin/OpenMVS:$PATH

WORKDIR /app/
COPY run_openmvs.py run_openmvs.py
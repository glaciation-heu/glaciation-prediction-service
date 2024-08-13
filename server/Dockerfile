FROM ubuntu:22.04
ARG DEBIAN_FRONTEND=noninteractive

#
# Python3.10 install for Ubuntu
#
# ref: https://linuxize.com/post/how-to-install-python-3-8-on-ubuntu-18-04/
RUN apt-get update
RUN apt-get install -y software-properties-common
RUN add-apt-repository ppa:deadsnakes/ppa
RUN apt-get install -y python3.10 python3-pip

# Create a symlink for python3
RUN ln -sf /usr/bin/python3 /usr/bin/python
RUN ln -sf /usr/bin/pip3 /usr/bin/pip

# Verify Python installation
RUN python3 --version && python --version

# Update package lists and install packages
RUN apt-get update && \
    apt-get install -y \
    cron \
    gcc \
    g++ \
    gfortran \
    libffi-dev \
    libopenblas-dev \
    bash \
    cmake \
    meson \
    ninja-build && \
    # Clean up to reduce image size
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

COPY requirements.txt /usr/src/app/

# Upgrade pythran and gast
#RUN pip install --no-cache-dir --upgrade pythran gast
# Install required packages
RUN pip3 install --no-cache-dir -r requirements.txt --ignore-installed

COPY . /usr/src/app

### Set up cronjob
COPY ./cronjob/prediction-cron /etc/cron.d/prediction-cron
RUN chmod 0644 /etc/cron.d/prediction-cron
# Add log
RUN touch /var/log/cron.log
#CMD /usr/sbin/cron -f && tail -f /var/log/cron.log

#EXPOSE 8080

#ENTRYPOINT ["python3"]
#CMD ["-m", "openapi_server"]
CMD cron && tail -f /var/log/cron.log & python3 -m openapi_server
EXPOSE 8080

FROM debian:stable

RUN apt update \
  && apt install -y python3 python3-pip python3-numpy \
  	 python3-matplotlib python3-pyqt5 python3-pbr locales

RUN echo "LC_ALL=en_US.UTF-8" >> /etc/environment \
	&& echo "en_US.UTF-8 UTF-8" >> /etc/locale.gen \
	&& echo "LANG=en_US.UTF-8" > /etc/locale.conf \
  	&& locale-gen en_US.UTF-8
	
ENV LC_ALL en_US.UTF-8
ENV LANG en_US.UTF-8  
ENV LANGUAGE en_US:en  
ENV LC_ALL en_US.UTF-8 

# use same IDs as user on host --> first user is automatically UID/GID 1000
RUN adduser --disabled-password --gecos "" test

USER test

COPY testdata/ /home/test/testdata

# run without using cache
ARG CACHEBUST=1
RUN pip3 install -i https://test.pypi.org/simple/ --no-deps --user elkoa

CMD cd /home/test/testdata && $HOME/.local/bin/elkoa

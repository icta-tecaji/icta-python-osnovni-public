FROM ubuntu:18.04

RUN apt-get update && apt-get install -y \
    openssh-server

RUN mkdir /var/run/sshd
RUN echo 'root:blu8z3' | chpasswd
RUN sed -i 's/PermitRootLogin yes/PermitRootLogin yes/' /etc/ssh/sshd_config

# SSH login fix. Otherwise user is kicked off after login
RUN sed 's@session\s*required\s*pam_loginuid.so@session optional pam_loginuid.so@g' -i /etc/pam.d/sshd
ENV NOTVISIBLE "in users profile"
RUN echo "export VISIBLE=now" >> /etc/profile

# create new user plume
RUN useradd -m -s /bin/bash testuser
RUN echo 'testuser:test' | chpasswd
RUN usermod -aG sudo testuser

WORKDIR /home/testuser

# dodaj stvari ki jih želimo imeti nameščene na sistemu
RUN apt-get update && apt-get install -y \
    sudo \
    telnetd

EXPOSE 22
EXPOSE 23

ADD start.sh /
RUN chmod +x /start.sh

CMD ["/start.sh"]

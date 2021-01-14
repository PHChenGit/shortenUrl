#!/usr/bin/env bash

DEBIAN_FRONTEND=noninteractive apt-get update && \
DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends lsb-release gnupg && \
cd /tmp && wget https://dev.mysql.com/get/mysql-apt-config_0.8.15-1_all.deb && \
DEBIAN_FRONTEND=noninteractive dpkg -i mysql-apt-config_0.8.15-1_all.deb && \
DEBIAN_FRONTEND=noninteractive apt-get update && \
DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends mysql-shell

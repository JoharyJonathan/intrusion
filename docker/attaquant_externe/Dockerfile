FROM ubuntu:22.04

# Désactiver les prompts et configurer la timezone
ENV DEBIAN_FRONTEND=noninteractive
RUN ln -fs /usr/share/zoneinfo/Africa/Antananarivo /etc/localtime && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
        nmap \
        hydra \
        hping3 \
        net-tools \
        curl \
        python3 \
        python3-pip \
        wget \
        unzip && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Installer rockyou.txt
RUN mkdir -p /usr/share/wordlists && \
    wget https://github.com/brannondorsey/naive-hashcat/releases/download/data/rockyou.txt -P /usr/share/wordlists/ || \
    (wget https://gitlab.com/kalilinux/packages/wordlists/-/raw/kali/master/rockyou.txt.gz -P /usr/share/wordlists/ && \
     gunzip /usr/share/wordlists/rockyou.txt.gz)

# Copier le script
COPY ./docker/attaquant_externe/attack_script.sh /root/attack_script.sh
RUN chmod +x /root/attack_script.sh

CMD ["/root/attack_script.sh"]
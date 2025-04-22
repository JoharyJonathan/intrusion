FROM ubuntu:22.04

# Désactiver les interactions pendant l'installation
ENV DEBIAN_FRONTEND=noninteractive

# Installer les dépendances de base
RUN apt-get update && \
    apt-get install -y \
    tcpdump \
    python3 \
    python3-pip \
    net-tools \
    openssh-server \
    iptables \
    sqlite3 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Installer tshark dans la même couche
RUN apt-get update && \
    apt-get install -y tshark \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Créer les dossiers nécessaires
RUN mkdir -p /app/db /var/log

# Copier les fichiers nécessaires
COPY docker/host_principal/services.sh /root/
COPY api /app/api
COPY model /app/model
COPY docker/host_principal/network_monitor.py /app/network_monitor.py
COPY scripts/convert_pcap_to_csv.py /app/scripts/

# Installer les dépendances Python
RUN pip3 install -r /app/api/requirements.txt

# Rendre le script exécutable
RUN chmod +x /root/services.sh

# Démarrer les services
CMD ["/root/services.sh"]
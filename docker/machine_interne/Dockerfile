FROM ubuntu:22.04

# Installer les outils nécessaires
RUN apt-get update && \
    apt-get install -y \
        curl \
        wget \
        openssh-client \
        net-tools \
        python3 \
        python3-pip && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Configurer un utilisateur normal
RUN useradd -m -s /bin/bash user && \
    echo "user:password" | chpasswd

# Démarrer un shell interactif
CMD ["/bin/bash", "-c", "tail -f /dev/null"]
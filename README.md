# Intrusion Detection and Attack Simulation Lab

A Docker-based cybersecurity lab that simulates external network attacks and demonstrates machine-learning-based intrusion detection, malicious IP tracking, and real-time security monitoring.

## Overview

This project was developed as part of a cybersecurity practical assignment. It simulates a network environment in which an external attacker performs reconnaissance and attack attempts against a target host.

The environment consists of three Ubuntu Docker containers:

- **`attaquant_externe`** — simulates an external attacker performing network scans, SSH brute-force attempts, and TCP SYN flood activity against the primary target.
- **`host_principal`** — acts as the main attack target and hosts the network monitoring service, machine learning inference API, and IP blacklist mechanism.
- **`machine_interne`** — represents an internal machine within the simulated Docker network. In the current implementation, it remains active but is not explicitly targeted by the attack script.

The intrusion detection model is trained using the **KDDTrain+ dataset**. The monitoring system captures network traffic and sends extracted features to the prediction API. IP addresses identified as malicious can be recorded in a blacklist, while a dashboard provides a real-time view of security events, including detected attacks, blocked activity, and normal actions.

## Key Features

- **Docker-based network simulation:** Three Ubuntu containers represent the external attacker, primary target, and internal machine.
- **Network reconnaissance simulation:** Nmap is used to scan the primary target.
- **SSH brute-force simulation:** Hydra attempts SSH authentication using a password wordlist.
- **TCP SYN flood simulation:** Hping3 generates TCP SYN packets toward the target's HTTP port.
- **Machine learning-based intrusion detection:** A model trained on KDDTrain+ contributes to classifying network activity.
- **Malicious IP blacklist:** Records IP addresses identified as malicious by the detection system.
- **Network monitoring:** Captures and analyzes traffic on the primary target.
- **Attack response:** Supports blocking malicious activity through the implemented response mechanisms.
- **Real-time dashboard:** Displays normal activity, detected attacks, and blocked events.

## Architecture

```text
                     Docker Network
                           |
          +----------------+----------------+
          |                |                |
          v                v                v
 +----------------+ +----------------+ +----------------+
 | attaquant_     | | host_principal  | | machine_       |
 | externe        | |                 | | interne        |
 |                | | Network Monitor| |                |
 | Nmap           | | ML Inference API| | Internal       |
 | Hydra          | | IP Blacklist    | | Machine        |
 | Hping3         | | Firewall Rules  | |                |
 +----------------+ +----------------+ +----------------+
          |                ^
          |                |
          +----------------+
           Simulated attacks
           target host_principal

                           |
                           v
                 +--------------------+
                 | Real-Time Dashboard|
                 | Security Events    |
                 +--------------------+
```

*The diagram presents the conceptual architecture. In the current implementation, the attack script explicitly targets `host_principal`; `machine_interne` is present in the Docker network but is not directly targeted by that script.*

## How It Works

1. **Environment initialization:** Docker starts the three Ubuntu containers and connects them to the simulated network.
2. **Attack simulation:** The external attacker repeatedly performs network scans, SSH brute-force attempts, and TCP SYN flood activity against `host_principal`.
3. **Network monitoring:** The monitoring service on `host_principal` captures traffic and extracts information for analysis.
4. **Machine learning inference:** Extracted features are sent to the prediction API, which uses the trained model to classify network activity.
5. **Threat tracking:** IP addresses identified as malicious can be recorded in the blacklist.
6. **Attack response:** The configured response mechanisms can apply blocking rules to malicious sources.
7. **Real-time visualization:** The dashboard displays normal activity and security-related events.

## Attack Simulation

The external attacker container runs a Bash script that repeatedly performs three types of simulated attacks against `host_principal`.

### 1. Network Reconnaissance

Nmap is used to scan the target and gather information about exposed ports and services.

### 2. SSH Brute-Force Attempts

Hydra attempts SSH authentication using the `root` username and a password wordlist.

The effectiveness of this simulation depends on SSH availability, authentication configuration, and the target's security rules.

### 3. TCP SYN Flood Simulation

Hping3 generates TCP SYN packets toward port 80 of the target. The process runs for a limited period before being stopped, after which the script waits for a randomized interval before starting another cycle.

These activities are intended for an isolated, authorized laboratory environment.

## Machine Learning and Dataset

The project uses **KDDTrain+**, the training portion of the NSL-KDD intrusion detection dataset.

The dataset contains labeled network connection records used to train machine learning models to distinguish normal traffic from potentially malicious activity.

The trained model is integrated into the network monitoring workflow:

1. Network traffic is captured.
2. Relevant features are extracted.
3. Features are sent to the prediction API.
4. The model returns a classification.
5. The detection system uses the result to support threat tracking and response.

The exact model architecture, feature preprocessing, classification labels, and evaluation metrics should be documented according to the implementation. Performance figures should only be reported when supported by measured results.

## Network Monitoring

The monitoring service runs on `host_principal` and uses network capture tools to observe traffic on its `eth0` interface.

The `network_monitor.py` component processes captured traffic and communicates with the prediction API. The source IP address is also passed to the API to associate predictions with potential sources.

Because monitoring is configured on `host_principal`, traffic directed exclusively to another container is not necessarily visible to this monitor. Extending detection to `machine_interne` would require additional monitoring or an appropriate network traffic collection mechanism.

## Blacklist and Attack Response

The blacklist records IP addresses identified as malicious by the detection system.

It supports the response workflow by retaining addresses that may be used in subsequent security decisions. The project also includes firewall-related functionality through `iptables`.

It is important to distinguish between two operations:

- **Detection and recording:** identifying a potentially malicious IP address and storing it in the blacklist.
- **Blocking:** applying firewall rules or another enforcement mechanism to prevent traffic from that address.

The effectiveness of blocking depends on how these mechanisms are connected and configured. A blacklist entry alone does not automatically prevent network traffic.

## Real-Time Dashboard

The dashboard provides a centralized view of the simulated environment's activity.

It is intended to display:

- Detected attacks
- Blocked malicious activity
- Normal actions
- Security events and their evolution over time

The dashboard helps visualize the relationship between attack simulation, model-based detection, threat tracking, and response.

## Technologies

| Component | Technology |
|---|---|
| Containerization | Docker |
| Container operating system | Ubuntu 22.04 |
| Network reconnaissance | Nmap |
| SSH attack simulation | Hydra |
| TCP packet generation | Hping3 |
| Network capture | tcpdump, TShark |
| Firewall management | iptables |
| Programming and scripting | Python, Bash |
| Machine learning dataset | KDDTrain+ / NSL-KDD |
| Threat tracking | IP blacklist backed by SQLite |
| Monitoring | Network monitoring service |
| Visualization | Real-time dashboard |

*The dashboard framework, backend API framework, machine learning algorithm, and exact model evaluation results can be documented separately once confirmed from the source code.*

## Project Structure

The repository is organized around the simulated network actors and the detection system.

```text
intrusion/
├── docker/
│   ├── attaquant_externe/
│   │   ├── Dockerfile
│   │   └── attack_script.sh
│   └── host_principal/
│       ├── Dockerfile
│       ├── services.sh
│       └── network_monitor.py
├── api/
├── model/
├── scripts/
│   └── convert_pcap_to_csv.py
├── machine_interne/
├── docker-compose.yml
└── README.md
```

*This is an illustrative overview of the main components. Adjust the tree to match the repository's actual directory structure.*

## Getting Started

### Prerequisites

- Docker Engine or Docker Desktop
- Git
- Sufficient resources to run the containers and network monitoring services

### Installation

Clone the repository:

```bash
git clone https://github.com/JoharyJonathan/intrusion.git
cd intrusion
```

Build and start the environment using Docker Compose:

```bash
docker compose up --build
```

Check the status of the containers:

```bash
docker compose ps
```

View the container logs:

```bash
docker compose logs -f
```

The exact dashboard URL, exposed ports, and any additional initialization steps depend on the Docker Compose configuration.

### Stopping the Environment

To stop the running containers:

```bash
docker compose down
```

Use these commands only with the project's intended Docker Compose configuration. Before starting the attack simulation, confirm that the environment is isolated and that all targets are authorized.

## Limitations and Future Improvements

The current implementation provides a foundation for experimenting with machine-learning-based intrusion detection in a containerized environment. Several improvements could extend its capabilities.

- **Expand attack coverage:** Add explicitly defined and controlled scenarios targeting `machine_interne`.
- **Improve monitoring coverage:** Collect traffic for all relevant containers rather than relying exclusively on monitoring `host_principal`.
- **Evaluate model performance:** Report precision, recall, F1-score, and a confusion matrix on an appropriate test set.
- **Improve response validation:** Verify that blacklist entries trigger the intended firewall rules and that blocking behavior is observable.
- **Improve event traceability:** Record timestamps, source IPs, predicted classes, and response outcomes for analysis.
- **Document deployment configuration:** Describe service ports, environment variables, and dashboard access requirements.
- **Strengthen isolation:** Restrict the simulated network and avoid exposing attack tools or vulnerable services to untrusted networks.

## Security Notice

This project is intended for educational use in a controlled cybersecurity laboratory.

- Run attack simulations only against systems you own or are explicitly authorized to test.
- Keep the simulated environment isolated from untrusted networks.
- Treat machine learning predictions as estimates, not guarantees of detection.
- Verify that firewall rules enforce blocking rather than assuming that blacklist entries are sufficient.
- Do not use this prototype as a production-ready intrusion detection or prevention system without further testing and security review.

## Author

**Johary Jonathan**

GitHub: [@JoharyJonathan](https://github.com/JoharyJonathan)

Repository: [intrusion](https://github.com/JoharyJonathan/intrusion)
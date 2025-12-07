# 🛡️ Real-Time Fraud Detection with Apache Kafka & MLOps

This repository demonstrates a **Real-Time Anomaly Detection System** for banking transactions. It is designed to accompany the "Apache Kafka in MLOps" presentation, showcasing how to build scalable, event-driven machine learning pipelines.

The project illustrates core MLOps concepts such as **system decoupling**, **real-time monitoring**, and **stream processing**.

## 🏗️ Architecture

The system consists of three main decoupled components:

1.  **Stream Producer (Data Generator):**
    * Simulates high-frequency credit card transactions.
    * Injects random "Fraud" patterns (e.g., high amounts, suspicious locations) to test the system.
    * *Tech Stack:* Python, Kafka Producer API.

2.  **Message Broker (Infrastructure):**
    * Acts as the central nervous system, buffering data and ensuring low-latency delivery.
    * *Tech Stack:* Apache Kafka, Zookeeper (running via Docker).

3.  **Real-Time Consumer (Dashboard):**
    * Consumes the data stream in real-time.
    * Detects anomalies using a rule-based approach.
    * Visualizes live metrics and alerts.
    * *Tech Stack:* Streamlit, Pandas, Kafka Consumer API.

## 🚀 Quick Start

Follow these steps to run the demo on your local machine.

### Prerequisites
* **Docker** and **Docker Compose** installed.
* **Python 3.8+** installed.

### 1. Start the Infrastructure
We use Docker to spin up a single-node Kafka cluster and Zookeeper.

```bash
docker-compose up -d
````

*Wait for about 30-40 seconds for the containers to fully initialize.*

### 2\. Install Python Dependencies

It is recommended to use a virtual environment.

```bash
pip install -r requirements.txt
```

### 3\. Run the Demo

You will need **two separate terminal windows** to see the producer-consumer pattern in action.

**Terminal 1: Start the Data Generator**
This script will start pushing mock transactions to the `transactions` topic.

```bash
python producer.py
```

**Terminal 2: Start the Dashboard**
This will launch the Streamlit web application.

```bash
streamlit run dashboard.py
```

*The dashboard should open automatically in your browser (usually at http://localhost:8501).*


## 🛠️ Troubleshooting

  * **"NoBrokersAvailable" Error:** Kafka takes a while to start. If you see this error, wait a minute and try running the Python scripts again.
  * **Docker Issues:** Ensure your Docker Desktop is running and you have enough RAM allocated.

## 📜 License

This project is open-source and available under the MIT License.
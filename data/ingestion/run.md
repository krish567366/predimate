# Ingestion Pipeline PoC - Step 1.3

## Prerequisites

Make sure the following are installed and configured:

- **Minikube** and **Helm**: For running the Kubernetes cluster and installing Kafka.
- **Docker**: Required to run the Mosquitto container and simulator.
- **Python** with `kafka-python` library.
- **Simulator Code (Step 1.2)**: Ensure you have the simulator code available from step 1.2.

---

## Step-by-Step Execution

### 1. Start Minikube

```bash
minikube start
```

---

### 2. Install Kafka using Helm

```bash
helm repo add bitnami https://charts.bitnami.com/bitnami
helm repo update
helm install my-kafka bitnami/kafka --set replicaCount=3 --set zookeeper.replicaCount=3
```

---

### 3. Verify Kafka Pods

```bash
kubectl get pods
```

> Wait until **all Kafka and ZooKeeper pods** are in the "Running" state.

---

### 4. Create the Kafka Topic

```bash
kubectl exec -it my-kafka-kafka-0 -- /opt/bitnami/kafka/bin/kafka-topics.sh --create --topic predimate-data --bootstrap-server my-kafka-kafka-bootstrap.default.svc.cluster.local:9092
```

---

### 5. Run the Mosquitto Container and Build the Simulator Image

Navigate to the directory containing the simulator code from step 1.2, then run:

```bash
python simulator.py
```

> This will create the Mosquitto container and build the simulator Docker image.

---

### 6. Run the Simulator Container

In a **new terminal window**, run:

```bash
docker run predimate-simulator
```

---

### 7. Run the Python Consumer

In another **new terminal window**, navigate to the directory with the consumer script and run:

```bash
python consumer.py
```

> Assuming the consumer script is named `consumer.py`.

---

### 8. Observe the Output

You should now see **simulated sensor data** printed to the terminal running the consumer script.

✅ This confirms that data is flowing from the **simulator → MQTT → Kafka → Python consumer**.

---

## Optional: Inspect Kafka Cluster

Use Kafka tools or Kubernetes commands to inspect Kafka and verify data ingestion into the `predimate-data` topic.

---

## Troubleshooting

### Kafka Pods Not Running
- Check pod logs for errors:

```bash
kubectl logs <pod-name>
```

---

### Consumer Not Receiving Data
- Ensure the Kafka topic was created successfully.
- Verify the Kafka bootstrap server address in the Python consumer script.
- Confirm the simulator is publishing to the correct MQTT topic.
- Ensure the Mosquitto container is running.

---

### Network Issues
- Check your **Minikube network configuration** if facing connectivity problems.

---

By following these steps, you should be able to **successfully run the 1.3 Ingestion Pipeline PoC** and confirm the complete data flow.

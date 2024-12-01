# Winners Circle Live  

## Steps to Set Up and Run the Application  

### 1. Spin a Docker Container  
Run the following command to start a Docker container:  

```bash
docker run --rm -it --entrypoint bash -v /home/ubuntu/efs-mount-point/students/<pid>/root:/root -p 8080-8130:8080 -p 9092-9142:9092 --name <pid> pipeline:latest
```

Replace `<docker_image_name>` with the appropriate Docker image you are using.  

---

### 2. Add Necessary Files to Airflow DAGs Directory  
Place the files `dag_stream.py` and `stream_ingest.py` in the Airflow DAGs directory:  

```bash
nano <file-name>
cp dag_stream.py stream_ingest.py /root/airflow/dags/
```

---

### 3. Access the EC2 Instance and Execute Inside the Docker Container  
SSH into your EC2 instance and execute the following command to enter the Docker container:  

```bash
docker exec -it <container_id> bash
```

Replace `<container_id>` with the ID of your running Docker container.  

---

### 4. Navigate to Kafka Directory  
Move to the Kafka installation directory:  

```bash
cd /home/kafka_2.13-3.5.0/
```

---

### 5. Export Kafka Heap Options  
Set the required Kafka memory heap options:  

```bash
export KAFKA_HEAP_OPTS="-Xmx256M -Xms128M"
```

---

### 6. Edit Server Properties for Kafka  
Open the Kafka server properties file for editing:  

```bash
nano config/server.properties
```

Add the following line (replacing `<ip>` and `<port>` with your server's IP address and port):  

```properties
advertised.listeners=PLAINTEXT://<ip>:<port>
```

---

### 7. Start Zookeeper  
Run the following command to start Zookeeper:  

```bash
bin/zookeeper-server-start.sh config/zookeeper.properties
```

---

### 8. Start the Kafka Server  
Run the following command to start the Kafka server:  

```bash
bin/kafka-server-start.sh config/server.properties
```

---

### 9. Add a Kafka Topic  
Create a Kafka topic named `CricketData` with the following command:  

```bash
bin/kafka-topics.sh --create --topic CricketData --bootstrap-server <ip>:<port> --replication-factor 1 --partitions 1
```

Replace `<ip>` and `<port>` with your server's IP address and port.  

---

### 10. Start Airflow  
Run Airflow with the following command:  

```bash
airflow standalone
```

You can access Airflow using the URL `http://<ip>:<port>` where `<ip>` is your server IP and `<port>` is the configured port for Airflow.  

---

## User Interface  

### UI Overview  
The user interface is a **Streamlit** Python application used to visualize data streams.  

### Steps to Run the UI Application:  
1. Navigate to the `ui/` directory:  

   ```bash
   cd ui/
   ```

2. Start the Streamlit application using the following command:  

   ```bash
   streamlit run app.py
   ```

Access the UI in your browser using the displayed Streamlit local or network URL.  

---

## Features  

- **Kafka Integration**: Handles real-time data ingestion using Kafka.  
- **Airflow Workflow**: Automated pipeline management and scheduling.  
- **Streamlit Visualization**: Interactive UI for data analysis and visualization.  
- **Scalable Architecture**: Built for handling large-scale data streams.  

---

## Prerequisites  

- Docker  
- Kafka (2.13-3.5.0)  
- Airflow  
- Python (for Streamlit)  
- EC2 Instance  

---
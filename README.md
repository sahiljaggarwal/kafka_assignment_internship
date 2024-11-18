
# **Real-Time Order Processing Pipeline**

This project was an attempt to create a real-time data processing pipeline using Kafka, Kafka Connect, and PostgreSQL with Docker Compose. The goal was to fetch data from a mock REST API (using `json-server`), process it via Kafka, and store it in PostgreSQL.

---

## **Current Status**

- The **JSON Server** is running successfully and serving mock data.  
- **Kafka**, **Kafka Connect**, and **PostgreSQL** have been set up using Docker Compose.  
- The **HTTP Source Connector** for Kafka Connect was configured to fetch data from the REST API.  
- The **PostgreSQL Sink Connector** was configured to store processed data.  

However, the pipeline is currently **not functional** due to issues with the **Kafka Connect HTTP Source Connector**.

---

## **Project Objectives**

1. Simulate a REST API providing order data using `json-server`.  
2. Ingest the data into Kafka using the **HTTP Source Connector**.  
3. Process the data and store it in a PostgreSQL database using the **PostgreSQL Sink Connector**.

---

## **Setup and Steps**

### **1. Setting Up JSON Server**

- Install JSON Server:
  ```bash
  npm install -g json-server
  ```
- Create a `db.json` file with mock order data:
  ```json
  {
    "orders": [
      {
        "order_id": "1",
        "product_name": "Product A",
        "quantity": 2,
        "price": 100,
        "order_date": "2024-11-14T10:00:00Z"
      }
    ]
  }
  ```
- Run JSON Server:
  ```bash
  json-server --watch db.json --port 3000
  ```
- Verify the API is running at `http://localhost:3000/orders`.

---

### **2. Setting Up Docker Compose**

- Start Kafka, Kafka Connect, Zookeeper, and PostgreSQL:
  ```bash
  docker-compose up -d
  ```
- Check that the following services are running:
  - **Kafka** on `localhost:9092`.
  - **Kafka Connect** on `localhost:8083`.
  - **PostgreSQL** on `localhost:5432`.

---

### **3. Configuring Kafka Connect**

#### **HTTP Source Connector**

- Create a configuration file (`http-source-connector.json`) for the HTTP Source Connector:
  ```json
  {
    "name": "http-source-connector",
    "config": {
      "connector.class": "io.confluent.connect.http.HttpSourceConnector",
      "tasks.max": "1",
      "http.api.url": "http://localhost:3000/orders",
      "http.method": "GET",
      "topic": "orders",
      "value.converter": "org.apache.kafka.connect.json.JsonConverter",
      "value.converter.schemas.enable": "false"
    }
  }
  ```
- Post the configuration to Kafka Connect:
  ```bash
  curl -X POST -H "Content-Type: application/json" \
  --data @http-source-connector.json \
  http://localhost:8083/connectors
  ```

#### **PostgreSQL Sink Connector**

- Create a configuration file (`postgres-sink-connector.json`) for the PostgreSQL Sink Connector:
  ```json
  {
    "name": "postgres-sink-connector",
    "config": {
      "connector.class": "io.confluent.connect.jdbc.JdbcSinkConnector",
      "tasks.max": "1",
      "topics": "orders",
      "connection.url": "jdbc:postgresql://postgres:5432/mydatabase",
      "connection.user": "myuser",
      "connection.password": "mypassword",
      "insert.mode": "insert",
      "auto.create": "true",
      "auto.evolve": "true",
      "value.converter": "org.apache.kafka.connect.json.JsonConverter",
      "value.converter.schemas.enable": "false"
    }
  }
  ```
- Post the configuration to Kafka Connect:
  ```bash
  curl -X POST -H "Content-Type: application/json" \
  --data @postgres-sink-connector.json \
  http://localhost:8083/connectors
  ```

---




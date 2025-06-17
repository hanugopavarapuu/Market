# Backend Architecture Documentation

## 1. Overall Architecture

```mermaid
graph TB
    subgraph Frontend
        UI[React Frontend]
    end

    subgraph Backend
        API[FastAPI Layer]
        Kafka[Kafka Message Broker]
        DB[(Database)]
        YF[Yahoo Finance]
    end

    UI -->|HTTP Requests| API
    API -->|Publish| Kafka
    Kafka -->|Consume| API
    API -->|Query/Store| DB
    API -->|Fetch Data| YF

    classDef frontend fill:#e1f5fe,stroke:#01579b
    classDef backend fill:#f3e5f5,stroke:#4a148c
    classDef database fill:#e8f5e9,stroke:#1b5e20
    classDef external fill:#fff3e0,stroke:#e65100

    class UI frontend
    class API,Kafka backend
    class DB database
    class YF external
```

## 2. File Structure and Responsibilities

### Core Components

```mermaid
mindmap
  root((Backend))
    (API Layer)
      [main.py]
        FastAPI app initialization
        Route definitions
        Dependency injection
      [endpoints/]
        Price endpoints
        Polling endpoints
    (Data Models)
      [models.py]
        SQLAlchemy models
        Database schemas
    (Services)
      [services/]
        Price service
        Polling service
        Kafka service
    (Core)
      [core/]
        Config
        Security
        Kafka setup
    (Schemas)
      [schemas/]
        Pydantic models
        Request/Response models
```

## 3. Kafka Integration Flow

```mermaid
sequenceDiagram
    participant Client
    participant API
    participant Kafka
    participant Consumer
    participant DB

    Client->>API: Request Stock Price
    API->>Kafka: Publish to 'price-requests'
    Kafka->>Consumer: Consume message
    Consumer->>DB: Store request
    Consumer->>API: Process request
    API->>Client: Return price

    Note over Kafka: Topics:
    Note over Kafka: - price-requests
    Note over Kafka: - price-updates
    Note over Kafka: - polling-jobs
```

## 4. Detailed Component Explanation

### 4.1 API Layer (`api/main.py`)

- Entry point for all HTTP requests
- Defines API routes and endpoints
- Handles request validation
- Manages dependency injection
- Integrates with Kafka producers

### 4.2 Data Models (`models.py`)

```mermaid
classDiagram
    class PriceData {
        +int id
        +str symbol
        +float price
        +datetime timestamp
        +str provider
    }
    class PollingJob {
        +int id
        +str symbol
        +int interval
        +bool active
        +datetime created_at
    }
    PriceData "1" -- "many" PollingJob
```

### 4.3 Services Layer (`services/`)

- **Price Service**: Handles price fetching and updates
- **Polling Service**: Manages polling jobs and schedules
- **Kafka Service**: Manages message production and consumption

### 4.4 Kafka Topics and Partitions

```mermaid
graph LR
    subgraph Topics
        PR[price-requests]
        PU[price-updates]
        PJ[polling-jobs]
    end

    subgraph Partitions
        P1[Partition 1]
        P2[Partition 2]
        P3[Partition 3]
    end

    PR --> P1
    PU --> P2
    PJ --> P3

    classDef topic fill:#e1f5fe,stroke:#01579b
    classDef partition fill:#f3e5f5,stroke:#4a148c

    class PR,PU,PJ topic
    class P1,P2,P3 partition
```

## 5. Request Flow Example

```mermaid
sequenceDiagram
    participant C as Client
    participant A as API
    participant K as Kafka
    participant S as Service
    participant D as Database

    C->>A: GET /api/v1/prices/latest?symbol=AAPL
    A->>K: Publish to price-requests
    K->>S: Consumer processes message
    S->>D: Store request
    S->>A: Return price data
    A->>C: Return HTTP response
```

## 6. Error Handling Flow

```mermaid
graph TD
    A[Request] -->|Validation| B{Valid?}
    B -->|Yes| C[Process]
    B -->|No| D[400 Bad Request]
    C -->|Kafka Error| E[500 Internal Error]
    C -->|DB Error| F[500 Database Error]
    C -->|Success| G[200 OK]
```

## 7. Key Features for Interview Discussion

1. **Scalability**

   - Kafka partitions for parallel processing
   - Database indexing for fast queries
   - Caching layer for frequent requests

2. **Reliability**

   - Error handling at each layer
   - Retry mechanisms for failed requests
   - Data consistency checks

3. **Performance**

   - Asynchronous processing with Kafka
   - Efficient database queries
   - Connection pooling

4. **Security**
   - Input validation
   - Rate limiting
   - Error message sanitization

## 8. Monitoring and Logging

```mermaid
graph LR
    A[Application] -->|Logs| B[Log Aggregator]
    B -->|Metrics| C[Monitoring Dashboard]
    B -->|Alerts| D[Alert System]
    C -->|Visualization| E[Grafana]
    D -->|Notifications| F[Email/Slack]
```

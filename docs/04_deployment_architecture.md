# Deployment Architecture

This document describes the containerization and deployment architecture using Docker and docker-compose.

## Docker Multi-Stage Build Process

```mermaid
graph TB
    subgraph "Build Stage"
        B1["Stage 1: Builder"]
        B1A["FROM python:3.11-slim"]
        B1B["Install build-essential"]
        B1C["Create wheels<br/>from requirements"]
        B1D["Output: /wheels"]
    end
    
    subgraph "Runtime Stage"
        R1["Stage 2: Runtime"]
        R1A["FROM python:3.11-slim"]
        R1B["Copy wheels<br/>from builder"]
        R1C["Install wheels"]
        R1D["Copy app code"]
        R1E["Create non-root user"]
        R1F["Expose port 5000"]
        R1G["Health check"]
    end
    
    subgraph "Output"
        O1["Final Image<br/>~1.2GB optimized"]
    end
    
    B1 --> B1A
    B1A --> B1B
    B1B --> B1C
    B1C --> B1D
    
    R1 --> R1A
    B1D -->|Copy /wheels| R1B
    R1B --> R1C
    R1C --> R1D
    R1D --> R1E
    R1E --> R1F
    R1F --> R1G
    
    R1G --> O1
    
    style B1 fill:#fff9c4
    style B1A fill:#fff9c4
    style B1B fill:#fff9c4
    style B1C fill:#fff9c4
    style B1D fill:#fff9c4
    style R1 fill:#ffe0b2
    style R1A fill:#ffe0b2
    style R1B fill:#ffe0b2
    style R1C fill:#ffe0b2
    style R1D fill:#ffe0b2
    style R1E fill:#ffe0b2
    style R1F fill:#ffe0b2
    style R1G fill:#ffe0b2
    style O1 fill:#d1c4e9
```

## Docker Compose Services Architecture

```mermaid
graph TB
    subgraph "Docker Compose"
        DC["docker-compose.yml"]
    end
    
    subgraph "Service 1: Flask API"
        API["car-price-api<br/>Port: 5000"]
        API1["Image: car-price-prediction"]
        API2["Container: car-price-prediction-api"]
        API3["Volumes:<br/>artifacts/,<br/>logs/"]
        API4["Network:<br/>car-price-network"]
    end
    
    subgraph "Service 2: MLflow Server"
        ML["mlflow-server<br/>Port: 5001"]
        ML1["Image: ghcr.io/mlflow/mlflow"]
        ML2["Container: mlflow-server"]
        ML3["Volumes:<br/>mlflow-data/"]
        ML4["Network:<br/>car-price-network"]
    end
    
    subgraph "Shared Resources"
        NETWORK["Bridge Network<br/>car-price-network"]
        VOLUMES["Named Volumes<br/>mlflow-data"]
    end
    
    DC --> API
    DC --> ML
    
    API --> API1
    API --> API2
    API --> API3
    API --> API4
    
    ML --> ML1
    ML --> ML2
    ML --> ML3
    ML --> ML4
    
    API3 --> VOLUMES
    ML3 --> VOLUMES
    
    API4 --> NETWORK
    ML4 --> NETWORK
    
    style DC fill:#fff9c4
    style API fill:#ffe0b2
    style API1 fill:#ffe0b2
    style API2 fill:#ffe0b2
    style API3 fill:#ffe0b2
    style API4 fill:#ffe0b2
    style ML fill:#ffe0b2
    style ML1 fill:#ffe0b2
    style ML2 fill:#ffe0b2
    style ML3 fill:#ffe0b2
    style ML4 fill:#ffe0b2
    style NETWORK fill:#b3e5fc
    style VOLUMES fill:#b3e5fc
```

## Container Communication

```mermaid
graph TB
    subgraph "Host Machine"
        H1["Port 5000: Flask API"]
        H2["Port 5001: MLflow"]
    end
    
    subgraph "Docker Network"
        API["API Container"]
        ML["MLflow Container"]
        BRIDGE["Bridge Network<br/>car-price-network"]
    end
    
    subgraph "Shared Storage"
        ARTIFACTS["artifacts/<br/>models, data"]
        LOGS["logs/<br/>running_logs.log"]
        MLFLOW_DATA["mlflow-data/<br/>experiments"]
    end
    
    H1 --> API
    H2 --> ML
    
    API --> BRIDGE
    ML --> BRIDGE
    
    BRIDGE -->|Service Discovery| API
    BRIDGE -->|Service Discovery| ML
    
    API --> ARTIFACTS
    API --> LOGS
    
    ML --> MLFLOW_DATA
    
    style H1 fill:#c8e6c9
    style H2 fill:#c8e6c9
    style API fill:#ffe0b2
    style ML fill:#ffe0b2
    style BRIDGE fill:#b3e5fc
    style ARTIFACTS fill:#ffccbc
    style LOGS fill:#ffccbc
    style MLFLOW_DATA fill:#ffccbc
```

## Deployment Workflow

```mermaid
graph TD
    A["Code Ready"]
    -->|Build| B["docker-compose build"]
    
    B -->|Build Stage 1| C["Create wheels<br/>python:3.11-slim"]
    C -->|Build Stage 2| D["Runtime image<br/>~1.2GB"]
    
    D -->|Pull Base| E["MLflow Image<br/>ghcr.io/mlflow/mlflow"]
    
    E -->|Compose| F["docker-compose up -d"]
    
    F -->|Start Service 1| G["API Container<br/>Port 5000"]
    F -->|Start Service 2| H["MLflow Container<br/>Port 5001"]
    
    G -->|Mount| I["Artifacts Volume"]
    G -->|Mount| J["Logs Volume"]
    H -->|Mount| K["MLflow Volume"]
    
    G -->|Health Check| L["Verify API Ready"]
    H -->|Health Check| M["Verify MLflow Ready"]
    
    L -->|Pass| N["✓ Deployment Complete"]
    M -->|Pass| N
    
    N -->|Access| O["http://localhost:5000"]
    N -->|Access| P["http://localhost:5001"]
    
    style A fill:#c8e6c9
    style B fill:#fff9c4
    style C fill:#fff9c4
    style D fill:#fff9c4
    style E fill:#fff9c4
    style F fill:#ffe0b2
    style G fill:#ffccbc
    style H fill:#ffccbc
    style I fill:#f8bbd0
    style J fill:#f8bbd0
    style K fill:#f8bbd0
    style L fill:#d1c4e9
    style M fill:#d1c4e9
    style N fill:#d1c4e9
    style O fill:#a5d6a7
    style P fill:#a5d6a7
```

## Container Lifecycle

```mermaid
stateDiagram-v2
    [*] --> Stopped
    
    Stopped --> Starting: docker-compose up -d
    Starting --> HealthCheck: Container created
    HealthCheck --> Running: Health check passes
    HealthCheck --> CrashLoop: Health check fails
    
    Running --> Healthy: Serving requests
    Healthy --> Running: Continuous operation
    
    Running --> Stopping: docker-compose down
    Stopping --> Stopped: Container stopped
    
    CrashLoop --> Stopped: Manual intervention
    
    Healthy --> Logs: Check docker-compose logs
    Logs --> Healthy: Investigate issues
    
    note right of Running
        - Listening on port 5000 (API)
        - Listening on port 5001 (MLflow)
        - Volumes mounted
        - Logging active
    end note
    
    note right of Healthy
        - Health checks passing
        - All endpoints available
        - Ready for predictions
    end note
```

## Resource Management

```mermaid
graph TD
    subgraph "API Container"
        APICPU["CPU: 2 cores<br/>max"]
        APIMEM["Memory: 2GB<br/>max"]
        APISTOR["Storage:<br/>artifacts/,<br/>logs/"]
    end
    
    subgraph "MLflow Container"
        MLCPU["CPU: 1 core"]
        MLMEM["Memory: 1GB"]
        MLSTOR["Storage:<br/>mlflow-data/"]
    end
    
    subgraph "System"
        TOTAL["Total Resources<br/>Available"]
    end
    
    APICPU --> TOTAL
    APIMEM --> TOTAL
    APISTOR --> TOTAL
    MLCPU --> TOTAL
    MLMEM --> TOTAL
    MLSTOR --> TOTAL
    
    style APICPU fill:#fff9c4
    style APIMEM fill:#fff9c4
    style APISTOR fill:#fff9c4
    style MLCPU fill:#ffe0b2
    style MLMEM fill:#ffe0b2
    style MLSTOR fill:#ffe0b2
    style TOTAL fill:#d1c4e9
```

## Health Check Mechanism

```mermaid
graph TD
    A["Health Check<br/>Interval: 30s"]
    -->|Execute| B["curl http://localhost:5000<br/>/info/status"]
    
    B -->|Success<br/>200 OK| C["✓ Healthy"]
    B -->|Timeout| D["⚠ Timeout"]
    B -->|Error| E["✗ Unhealthy"]
    
    C -->|Repeat| A
    D -->|Retries: 3| F["Check Failed?"]
    E -->|Retries: 3| F
    
    F -->|Yes| G["Container<br/>Restart"]
    F -->|No| A
    
    G -->|Automatic| H["Restart Policy:<br/>unless-stopped"]
    
    style A fill:#fff9c4
    style B fill:#fff9c4
    style C fill:#a5d6a7
    style D fill:#ffb74d
    style E fill:#ef5350
    style F fill:#fff9c4
    style G fill:#ffb74d
    style H fill:#fff9c4
```

## Volume Mounting Strategy

```mermaid
graph TB
    subgraph "Host Filesystem"
        HF["Project Directory<br/>car_price_prediction/"]
        ART["artifacts/"]
        LOGS["logs/"]
        MLFDATA["mlflow-data/"]
    end
    
    subgraph "API Container"
        CA["/app/artifacts"]
        CL["/app/logs"]
    end
    
    subgraph "MLflow Container"
        CM["/mlflow"]
    end
    
    ART -->|Bind Mount| CA
    LOGS -->|Bind Mount| CL
    MLFDATA -->|Named Volume| CM
    
    CA -->|Read/Write| HF
    CL -->|Read/Write| HF
    CM -->|Persist Data| HF
    
    style HF fill:#c8e6c9
    style ART fill:#ffe0b2
    style LOGS fill:#ffe0b2
    style MLFDATA fill:#ffe0b2
    style CA fill:#ffccbc
    style CL fill:#ffccbc
    style CM fill:#ffccbc
```

## Scaling Strategy

```mermaid
graph TD
    A["Single Container<br/>Development"]
    -->|Scale Up| B["Multiple Containers<br/>Behind Load Balancer"]
    
    B -->|Add| C["API Container 1<br/>Port 5000"]
    B -->|Add| D["API Container 2<br/>Port 5001"]
    B -->|Add| E["API Container 3<br/>Port 5002"]
    
    B -->|Shared| F["Shared Volumes<br/>artifacts/"]
    B -->|Shared| G["Shared MLflow<br/>Port 5010"]
    
    C --> H["Load Balancer<br/>Port 8000"]
    D --> H
    E --> H
    
    H -->|Distribute| I["Client Requests"]
    
    style A fill:#fff9c4
    style B fill:#ffe0b2
    style C fill:#ffccbc
    style D fill:#ffccbc
    style E fill:#ffccbc
    style F fill:#f8bbd0
    style G fill:#f8bbd0
    style H fill:#d1c4e9
    style I fill:#a5d6a7
```

---

## Key Deployment Features

✅ **Multi-Stage Docker Build** - Optimized image size  
✅ **Non-Root User** - Security best practice  
✅ **Health Checks** - Automatic restart on failure  
✅ **Volume Persistence** - Data survives container restart  
✅ **Network Isolation** - Service communication via bridge network  
✅ **Restart Policy** - Automatic recovery  
✅ **Environment Variables** - Configuration management  


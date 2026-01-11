# Deployment Pipeline

This document details the complete build, deployment, and service startup process using Docker and docker-compose.

## Complete Build Process

```mermaid
graph TD
    A["Dockerfile"]
    -->|Stage 1: Builder| B["FROM python:3.11-slim<br/>as builder"]
    
    B -->|Install| B1["build-essential<br/>compilers"]
    
    B -->|Copy| B2["requirements.txt"]
    
    B -->|Build| B3["pip wheel --no-cache-dir<br/>--no-deps<br/>--wheel-dir /wheels"]
    
    B3 -->|Output| B4["/wheels/<br/>All packages<br/>as wheels"]
    
    B -->|Stage 2: Runtime| C["FROM python:3.11-slim"]
    
    C -->|Install| C1["Non-compiler deps<br/>only"]
    
    C -->|Copy| C2["/wheels from builder"]
    
    C -->|Install| C3["pip install<br/>from wheels"]
    
    C -->|Create| C4["Non-root user<br/>appuser"]
    
    C -->|Copy| C5["Application code"]
    
    C -->|Setup| C6["Working directory<br/>/app"]
    
    C -->|Expose| C7["Port 5000"]
    
    C -->|Health| C8["HEALTHCHECK CMD<br/>curl localhost:5000"]
    
    C -->|Start| C9["CMD python app.py"]
    
    B4 -->|Multi-stage<br/>benefit| D["Smaller image<br/>~1.2GB<br/>No build tools"]
    
    style A fill:#c8e6c9
    style B fill:#fff9c4
    style B1 fill:#fff9c4
    style B2 fill:#fff9c4
    style B3 fill:#fff9c4
    style B4 fill:#fff9c4
    style C fill:#ffe0b2
    style C1 fill:#ffe0b2
    style C2 fill:#ffe0b2
    style C3 fill:#ffe0b2
    style C4 fill:#ffe0b2
    style C5 fill:#ffe0b2
    style C6 fill:#ffe0b2
    style C7 fill:#ffe0b2
    style C8 fill:#ffe0b2
    style C9 fill:#ffe0b2
    style D fill:#ffccbc
```

## Docker Image Layers

```mermaid
graph TB
    subgraph "Builder Stage (Intermediate)"
        B1["Layer 1: FROM python:3.11<br/>450MB"]
        B2["Layer 2: apt-get install<br/>300MB"]
        B3["Layer 3: pip wheel<br/>800MB"]
    end
    
    subgraph "Runtime Stage (Final Image)"
        R1["Layer 1: FROM python:3.11<br/>450MB"]
        R2["Layer 2: apt-get install<br/>50MB (no build tools)"]
        R3["Layer 3: COPY wheels<br/>200MB (wheels only)"]
        R4["Layer 4: pip install wheels<br/>300MB (installed)"]
        R5["Layer 5: CREATE USER<br/><1MB"]
        R6["Layer 6: COPY app code<br/>5MB"]
    end
    
    subgraph "Result"
        T["Final Image:<br/>~1.2GB<br/>Optimized<br/>Production-ready"]
    end
    
    B1 --> R1
    B2 -.->|discarded| T
    B3 -->|wheels| R3
    R3 --> R4 --> R5 --> R6
    R6 --> T
    
    style B1 fill:#fff9c4
    style B2 fill:#fff9c4
    style B3 fill:#fff9c4
    style R1 fill:#ffe0b2
    style R2 fill:#ffe0b2
    style R3 fill:#ffe0b2
    style R4 fill:#ffe0b2
    style R5 fill:#ffe0b2
    style R6 fill:#ffe0b2
    style T fill:#ffccbc
```

## docker-compose Orchestration

```mermaid
graph TD
    A["docker-compose.yml"]
    -->|Define| B["Services"]
    
    B -->|Service 1| B1["car-price-api"]
    B1 -->|Image| B1A["car-price-prediction<br/>from Dockerfile"]
    B1 -->|Port| B1B["5000:5000<br/>Flask API"]
    B1 -->|Volumes| B1C["artifacts/:/app/artifacts<br/>logs/:/app/logs"]
    B1 -->|Network| B1D["car-price-network"]
    B1 -->|Restart| B1E["unless-stopped"]
    
    B -->|Service 2| B2["mlflow-server"]
    B2 -->|Image| B2A["ghcr.io/mlflow/mlflow<br/>Official MLflow image"]
    B2 -->|Port| B2B["5001:5000<br/>MLflow UI"]
    B2 -->|Volumes| B2C["mlflow-data:/mlflow<br/>Persistent storage"]
    B2 -->|Network| B2D["car-price-network"]
    B2 -->|Command| B2E["mlflow server<br/>--host 0.0.0.0"]
    
    A -->|Define| C["Networks"]
    C -->|Bridge| C1["car-price-network<br/>Internal communication"]
    
    A -->|Define| D["Volumes"]
    D -->|Named| D1["mlflow-data<br/>Persistent"]
    D -->|Bind| D2["artifacts/<br/>Host directory"]
    
    style A fill:#c8e6c9
    style B fill:#fff9c4
    style B1 fill:#ffe0b2
    style B1A fill:#ffe0b2
    style B1B fill:#ffe0b2
    style B1C fill:#ffe0b2
    style B1D fill:#ffe0b2
    style B1E fill:#ffe0b2
    style B2 fill:#ffccbc
    style B2A fill:#ffccbc
    style B2B fill:#ffccbc
    style B2C fill:#ffccbc
    style B2D fill:#ffccbc
    style B2E fill:#ffccbc
    style C fill:#ffb74d
    style C1 fill:#ffb74d
    style D fill:#b3e5fc
    style D1 fill:#b3e5fc
    style D2 fill:#b3e5fc
```

## Deployment Command Sequence

```mermaid
graph TD
    A["Start Deployment"]
    -->|Step 1| B["docker-compose build"]
    
    B -->|Build Stage 1| B1["Builder image<br/>Create wheels"]
    B1 -->|Build Stage 2| B2["Runtime image<br/>Multi-stage optimization"]
    B2 -->|Tag| B3["car-price-prediction:latest"]
    
    A -->|Step 2| C["docker-compose up -d"]
    
    C -->|Create| C1["car-price-api<br/>Container"]
    C -->|Create| C2["mlflow-server<br/>Container"]
    
    C -->|Start| C1
    C -->|Start| C2
    
    C1 -->|Mount| C1A["artifacts/"]
    C1 -->|Mount| C1B["logs/"]
    C1 -->|Join| C1C["car-price-network"]
    
    C2 -->|Mount| C2A["mlflow-data/"]
    C2 -->|Join| C2C["car-price-network"]
    
    C1 -->|Health Check| C1D["GET /info/status<br/>Every 30s"]
    C1D -->|Pass| H1["Healthy"]
    C1D -->|Fail| H2["Restart"]
    
    C2 -->|Ready| C2D["MLflow listening<br/>port 5001"]
    
    H1 -->|Success| I["Deployment Complete"]
    C2D -->|Success| I
    
    style A fill:#c8e6c9
    style B fill:#fff9c4
    style B1 fill:#fff9c4
    style B2 fill:#fff9c4
    style B3 fill:#fff9c4
    style C fill:#ffe0b2
    style C1 fill:#ffe0b2
    style C2 fill:#ffe0b2
    style C1A fill:#ffccbc
    style C1B fill:#ffccbc
    style C1C fill:#ffccbc
    style C2A fill:#ffccbc
    style C2C fill:#ffccbc
    style C1D fill:#ffb74d
    style H1 fill:#a5d6a7
    style H2 fill:#ef5350
    style C2D fill:#ffb74d
    style I fill:#a5d6a7
```

## Container Startup Sequence

```mermaid
sequenceDiagram
    participant Docker as Docker Daemon
    participant API as API Container
    participant Flask as Flask App
    participant MLflow as MLflow Container
    
    Docker->>API: Start car-price-api<br/>Run python app.py
    Docker->>MLflow: Start mlflow-server<br/>Run mlflow server
    
    API->>Flask: Initialize Flask
    Flask->>Flask: Load model.pkl
    Flask->>Flask: Load scaler.pkl
    Flask->>Flask: Load encoders.pkl
    Flask-->>API: Models loaded
    
    API->>API: Listen on port 5000
    API-->>Docker: Ready for requests
    
    MLflow->>MLflow: Start server
    MLflow->>MLflow: Listen on port 5000<br/>(internal port)
    MLflow->>MLflow: Expose as 5001<br/>(external port)
    MLflow-->>Docker: Ready for tracking
    
    Docker->>API: Health check<br/>curl localhost:5000
    API-->>Docker: 200 OK
    
    Docker->>Docker: Mark containers<br/>healthy
    
    Note over API,MLflow: Both services ready<br/>API: http://localhost:5000<br/>MLflow: http://localhost:5001
```

## Network Communication

```mermaid
graph TB
    subgraph "Host Machine"
        H1["Port 5000"]
        H2["Port 5001"]
    end
    
    subgraph "Docker Network<br/>car-price-network"
        API["API Container<br/>car-price-api:5000"]
        MLFLOW["MLflow Container<br/>mlflow-server:5000"]
        BRIDGE["Bridge Network<br/>Internal DNS"]
    end
    
    subgraph "External Access"
        CLIENT["Client<br/>Browser/API Client"]
    end
    
    H1 -->|Port mapping| API
    H2 -->|Port mapping| MLFLOW
    
    API ---|Service DNS| BRIDGE
    MLFLOW ---|Service DNS| BRIDGE
    BRIDGE -->|Hostname resolve| API
    BRIDGE -->|Hostname resolve| MLFLOW
    
    CLIENT -->|HTTP| H1
    CLIENT -->|HTTP| H2
    
    API -->|Can reach<br/>mlflow-server:5000| MLFLOW
    
    style H1 fill:#c8e6c9
    style H2 fill:#c8e6c9
    style API fill:#fff9c4
    style MLFLOW fill:#ffe0b2
    style BRIDGE fill:#ffccbc
    style CLIENT fill:#ffb74d
```

## Health Check Mechanism

```mermaid
graph TD
    A["HEALTHCHECK in Dockerfile"]
    -->|Check every| B["30 seconds"]
    
    B -->|Execute| C["curl http://localhost:5000"]
    
    C -->|Success| D["HTTP 200 status"]
    D -->|Healthy| E["Container status:<br/>HEALTHY"]
    
    C -->|Timeout| F["No response<br/>after 10s"]
    F -->|Retries| F1["Retry count: 3"]
    F1 -->|Still failing| G["Container status:<br/>UNHEALTHY"]
    
    C -->|Error| H["HTTP != 200"]
    H -->|Retries| H1["Retry count: 3"]
    H1 -->|Still failing| G
    
    E -->|Action| I["Container lives<br/>No restart"]
    
    G -->|Action| J["Docker restarts<br/>container<br/>unless-stopped<br/>policy"]
    
    J -->|Result| K["New container<br/>starts"]
    K -->|Check| L["Health check<br/>again"]
    
    style A fill:#c8e6c9
    style B fill:#fff9c4
    style C fill:#ffe0b2
    style D fill:#a5d6a7
    style E fill:#a5d6a7
    style F fill:#ffb74d
    style F1 fill:#ffb74d
    style G fill:#ef5350
    style H fill:#ffb74d
    style H1 fill:#ffb74d
    style I fill:#a5d6a7
    style J fill:#ffb74d
    style K fill:#c8e6c9
    style L fill:#ffe0b2
```

## Deployment Troubleshooting

```mermaid
graph TD
    A["Deployment Issue"]
    
    A -->|Problem 1| B["Container won't start<br/>docker-compose up fails"]
    B -->|Check| B1["docker-compose logs"]
    B1 -->|Look for| B2["import errors<br/>file not found<br/>syntax errors"]
    B2 -->|Fix| B3["Update code<br/>Rebuild image"]
    
    A -->|Problem 2| C["Health check fails<br/>Container keeps restarting"]
    C -->|Check| C1["docker-compose logs<br/>API errors"]
    C1 -->|Look for| C2["Model loading errors<br/>Port conflicts<br/>Permission issues"]
    C2 -->|Fix| C3["Check model files<br/>Free port<br/>File permissions"]
    
    A -->|Problem 3| D["API returns 500 errors<br/>Predictions fail"]
    D -->|Check| D1["Model.pkl exists<br/>Scaler.pkl exists<br/>Encoders.pkl exists"]
    D1 -->|Look for| D2["Missing artifacts<br/>Invalid format<br/>Data mismatch"]
    D2 -->|Fix| D3["Retrain model<br/>Verify compatibility"]
    
    A -->|Problem 4| E["Can't connect to API<br/>Connection refused"]
    E -->|Check| E1["Port 5000 accessible<br/>Container running<br/>Network created"]
    E1 -->|Look for| E2["Firewall blocks<br/>Container stopped<br/>Network issues"]
    E2 -->|Fix| E4["Open port<br/>Restart containers<br/>Check network"]
    
    style A fill:#c8e6c9
    style B fill:#fff9c4
    style B1 fill:#ffb74d
    style B2 fill:#ffb74d
    style B3 fill:#a5d6a7
    style C fill:#fff9c4
    style C1 fill:#ffb74d
    style C2 fill:#ffb74d
    style C3 fill:#a5d6a7
    style D fill:#fff9c4
    style D1 fill:#ffb74d
    style D2 fill:#ffb74d
    style D3 fill:#a5d6a7
    style E fill:#fff9c4
    style E1 fill:#ffb74d
    style E2 fill:#ffb74d
    style E4 fill:#a5d6a7
```

## Deployment Lifecycle

```mermaid
stateDiagram-v2
    [*] --> Building: docker-compose build
    
    Building --> Built: Build successful
    Building --> BuildFailed: Build error<br/>Fix code, rebuild
    
    BuildFailed --> Building: Retry build
    
    Built --> Starting: docker-compose up -d
    
    Starting --> HealthCheck: Containers created
    HealthCheck --> Running: Health check passes
    HealthCheck --> CrashLoop: Health check fails<br/>Container restarts
    
    CrashLoop --> Running: Model loads OK<br/>Issue resolved
    CrashLoop --> Stopped: Max retries<br/>Manual intervention
    
    Running --> Serving: Ready for requests
    Serving --> Monitoring: Continuous operation
    
    Monitoring --> Running: Normal operation
    Monitoring --> Crashed: Container crashes<br/>Auto-restart
    
    Crashed --> Running: Restart successful
    
    Running --> Stopping: docker-compose down
    Serving --> Stopping: docker-compose down
    Monitoring --> Stopping: docker-compose down
    
    Stopping --> Stopped: Containers stopped<br/>Volumes preserved
    
    Stopped --> [*]
    
    note right of Running
        - Listening on ports 5000, 5001
        - Health checks passing
        - All models loaded
        - Ready for predictions
    end note
    
    note right of Serving
        - Accepting requests
        - Processing predictions
        - Logging activity
        - Tracking experiments
    end note
```

## Rollout Strategy

```mermaid
graph TD
    A["Current Deployment"]
    -->|Run in parallel| B["docker-compose up"]
    
    B -->|Health checks| C["New containers<br/>become healthy"]
    
    C -->|Warmup| D["Pre-load models<br/>30 seconds"]
    
    D -->|Test| E["Test endpoints<br/>verify working"]
    
    E -->|Success| F["Traffic to new<br/>containers"]
    E -->|Failure| G["Keep old<br/>containers<br/>Investigate issue"]
    
    F -->|After stable| H["Stop old<br/>containers<br/>docker-compose down<br/>old"]
    
    H -->|Cleanup| I["Deployment complete<br/>New version live"]
    
    style A fill:#c8e6c9
    style B fill:#fff9c4
    style C fill:#ffe0b2
    style D fill:#ffccbc
    style E fill:#ffb74d
    style F fill:#a5d6a7
    style G fill:#ef5350
    style H fill:#a5d6a7
    style I fill:#a5d6a7
```

---

## Deployment Commands Reference

**Build image:**
```bash
docker-compose build
```

**Start services:**
```bash
docker-compose up -d
```

**View logs:**
```bash
docker-compose logs -f car-price-api
docker-compose logs -f mlflow-server
```

**Check status:**
```bash
docker-compose ps
```

**Stop services:**
```bash
docker-compose down
```

**Restart services:**
```bash
docker-compose restart
```

**Remove volumes:**
```bash
docker-compose down -v
```


# API Architecture

This document describes the REST API structure, endpoints, and request/response flows.

## API Architecture Overview

```mermaid
graph TB
    subgraph "Client Layer"
        WEB["Web Browser<br/>localhost:5000"]
        CURL["cURL/HTTP<br/>Requests"]
        SDK["Python/JS<br/>SDK"]
    end
    
    subgraph "Flask Application"
        FLASK["Flask App<br/>Port 5000"]
        CORS["CORS<br/>Middleware"]
        AUTH["Error<br/>Handling"]
    end
    
    subgraph "API Namespaces"
        PRED_NS["Predict<br/>Namespace"]
        INFO_NS["Info<br/>Namespace"]
        WEB_NS["Web<br/>Namespace"]
    end
    
    subgraph "Endpoints"
        PE1["POST /predict/price<br/>Single Prediction"]
        PE2["POST /predict/batch<br/>Batch Prediction"]
        IE1["GET /info/status<br/>API Status"]
        IE2["GET /info/features<br/>Features List"]
        WE["GET /<br/>Web UI"]
        DOCS["GET /api/docs<br/>Swagger"]
    end
    
    subgraph "Processing"
        VAL["Validation<br/>Pydantic"]
        PREP["Preprocessing<br/>Feature Scaling"]
        PRED["Prediction<br/>ML Model"]
    end
    
    subgraph "Response"
        JSON["JSON<br/>Response"]
        HTML["HTML<br/>Response"]
        DOCS_UI["Swagger<br/>UI"]
    end
    
    WEB --> FLASK
    CURL --> FLASK
    SDK --> FLASK
    
    FLASK --> CORS
    CORS --> AUTH
    
    AUTH --> PRED_NS
    AUTH --> INFO_NS
    AUTH --> WEB_NS
    
    PRED_NS --> PE1
    PRED_NS --> PE2
    INFO_NS --> IE1
    INFO_NS --> IE2
    WEB_NS --> WE
    WEB_NS --> DOCS
    
    PE1 --> VAL
    PE2 --> VAL
    VAL --> PREP
    PREP --> PRED
    PRED --> JSON
    
    IE1 --> JSON
    IE2 --> JSON
    WE --> HTML
    DOCS --> DOCS_UI
    
    style WEB fill:#c8e6c9
    style CURL fill:#c8e6c9
    style SDK fill:#c8e6c9
    style FLASK fill:#fff9c4
    style CORS fill:#fff9c4
    style AUTH fill:#fff9c4
    style PRED_NS fill:#ffe0b2
    style INFO_NS fill:#ffe0b2
    style WEB_NS fill:#ffe0b2
    style PE1 fill:#ffccbc
    style PE2 fill:#ffccbc
    style IE1 fill:#ffccbc
    style IE2 fill:#ffccbc
    style WE fill:#ffccbc
    style DOCS fill:#ffccbc
    style VAL fill:#f8bbd0
    style PREP fill:#f8bbd0
    style PRED fill:#f8bbd0
    style JSON fill:#d1c4e9
    style HTML fill:#d1c4e9
    style DOCS_UI fill:#d1c4e9
```

## Request/Response Flow

```mermaid
sequenceDiagram
    participant Client
    participant API as Flask API
    participant Validation as Validation
    participant Model as ML Model
    participant Response as Response Builder

    Client->>API: POST /predict/price<br/>{car data}
    API->>Validation: Validate Input
    
    alt Valid Input
        Validation-->>API: ✓ Valid
        API->>API: Preprocess Data
        API->>Model: Get Prediction
        Model-->>API: Price + Confidence
        API->>Response: Build Success
        Response-->>API: {price, confidence}
        API-->>Client: 200 OK<br/>{price, confidence}
    else Invalid Input
        Validation-->>API: ✗ Errors
        API->>Response: Build Error
        Response-->>API: {error, details}
        API-->>Client: 400 Bad Request<br/>{error, details}
    end
```

## API Endpoints Structure

```mermaid
graph TD
    subgraph "Prediction Endpoints"
        P1["/predict/price"]
        P1 -->|POST| P1R["Request: CarFeatures<br/>Response: Price + Confidence"]
        
        P2["/predict/batch"]
        P2 -->|POST| P2R["Request: List[CarFeatures]<br/>Response: List[Price]"]
    end
    
    subgraph "Information Endpoints"
        I1["/info/status"]
        I1 -->|GET| I1R["Model Loaded: bool<br/>Scaler Loaded: bool<br/>Timestamp: str"]
        
        I2["/info/features"]
        I2 -->|GET| I2R["Features: List[str]<br/>Count: int"]
    end
    
    subgraph "Web Endpoints"
        W1["/"]
        W1 -->|GET| W1R["HTML Web UI<br/>Prediction Form"]
        
        W2["/api/docs"]
        W2 -->|GET| W2R["Swagger UI<br/>Interactive API Docs"]
    end
    
    subgraph "System"
        H1["/health"]
        H1 -->|GET| H1R["Status: 200 OK"]
    end
    
    style P1 fill:#ffccbc
    style P1R fill:#ffe0b2
    style P2 fill:#ffccbc
    style P2R fill:#ffe0b2
    style I1 fill:#ffccbc
    style I1R fill:#ffe0b2
    style I2 fill:#ffccbc
    style I2R fill:#ffe0b2
    style W1 fill:#ffccbc
    style W1R fill:#ffe0b2
    style W2 fill:#ffccbc
    style W2R fill:#ffe0b2
    style H1 fill:#ffccbc
    style H1R fill:#ffe0b2
```

## Data Validation Pipeline

```mermaid
graph TD
    A["Incoming Request<br/>JSON Data"]
    -->|Check| B["Required Fields<br/>Present?"]
    
    B -->|No| C["Return 400<br/>Missing Fields"]
    B -->|Yes| D["Type Check<br/>Numbers, Strings"]
    
    D -->|Fail| E["Return 400<br/>Type Error"]
    D -->|Pass| F["Range Check<br/>Year, Mileage, etc"]
    
    F -->|Fail| G["Return 400<br/>Range Error"]
    F -->|Pass| H["String Validation<br/>Non-empty"]
    
    H -->|Fail| I["Return 400<br/>String Error"]
    H -->|Pass| J["✓ Validation Success"]
    
    J -->|Proceed| K["Preprocessing<br/>Feature Scaling"]
    K -->|Return| L["Model Prediction"]
    
    style A fill:#c8e6c9
    style B fill:#fff9c4
    style D fill:#fff9c4
    style F fill:#fff9c4
    style H fill:#fff9c4
    style C fill:#ffcdd2
    style E fill:#ffcdd2
    style G fill:#ffcdd2
    style I fill:#ffcdd2
    style J fill:#d1c4e9
    style K fill:#f8bbd0
    style L fill:#d1c4e9
```

## Endpoint Details

### Prediction Endpoint: /predict/price

```mermaid
graph LR
    A["POST /predict/price<br/>Body: CarFeatures"] 
    -->|Validate| B["PredictionSchema"]
    -->|Preprocess| C["LabelEncode<br/>StandardScale"]
    -->|Predict| D["ML Model<br/>XGBoost"]
    -->|Format| E["Response<br/>JSON"]
    -->|Return| F["200 OK<br/>price, confidence"]
    
    style A fill:#c8e6c9
    style B fill:#fff9c4
    style C fill:#ffe0b2
    style D fill:#ffccbc
    style E fill:#f8bbd0
    style F fill:#d1c4e9
```

### Information Endpoints

```mermaid
graph LR
    A["GET /info/status"] 
    -->|Check| B["Model Loaded?<br/>Scaler Loaded?"]
    -->|Collect| C["System Info"]
    -->|Return| D["200 OK<br/>Status Object"]
    
    E["GET /info/features"]
    -->|Retrieve| F["Feature List<br/>16 Fields"]
    -->|Count| G["Feature Count"]
    -->|Return| H["200 OK<br/>Features Array"]
    
    style A fill:#c8e6c9
    style B fill:#fff9c4
    style C fill:#fff9c4
    style D fill:#d1c4e9
    
    style E fill:#c8e6c9
    style F fill:#fff9c4
    style G fill:#fff9c4
    style H fill:#d1c4e9
```

## Error Handling Flow

```mermaid
graph TD
    A["Request Received"]
    -->|Try| B["Process Request"]
    
    B -->|Validation Error| C["400 Bad Request<br/>Validation Details"]
    B -->|Model Error| D["500 Server Error<br/>Check Logs"]
    B -->|Success| E["200 OK<br/>Response Data"]
    
    C -->|Log| F["Error Logger"]
    D -->|Log| F
    E -->|Log| G["Info Logger"]
    
    C -->|Return| H["JSON Error"]
    D -->|Return| I["JSON Error"]
    E -->|Return| J["JSON Response"]
    
    F --> K["logs/running_logs.log"]
    G --> K
    
    style A fill:#fff9c4
    style B fill:#fff9c4
    style C fill:#ffcdd2
    style D fill:#ffcdd2
    style E fill:#d1c4e9
    style F fill:#b3e5fc
    style G fill:#b3e5fc
    style H fill:#ffcdd2
    style I fill:#ffcdd2
    style J fill:#d1c4e9
    style K fill:#c8e6c9
```

## API Namespace Organization

```mermaid
graph TB
    API["Flask-RESTX API"]
    
    API -->|Namespace| PRED_NS["Predict Namespace<br/>/predict"]
    API -->|Namespace| INFO_NS["Info Namespace<br/>/info"]
    API -->|Blueprint| WEB["Web Routes<br/>/ and /api/docs"]
    
    PRED_NS -->|Resource| PE1["PredictPrice<br/>POST /price"]
    PRED_NS -->|Resource| PE2["PredictBatch<br/>POST /batch"]
    
    INFO_NS -->|Resource| IE1["ModelStatus<br/>GET /status"]
    INFO_NS -->|Resource| IE2["FeatureInfo<br/>GET /features"]
    
    WEB -->|Route| WR1["GET /"]
    WEB -->|Route| WR2["GET /api/docs"]
    
    style API fill:#fff9c4
    style PRED_NS fill:#ffe0b2
    style INFO_NS fill:#ffe0b2
    style WEB fill:#ffe0b2
    style PE1 fill:#ffccbc
    style PE2 fill:#ffccbc
    style IE1 fill:#ffccbc
    style IE2 fill:#ffccbc
    style WR1 fill:#ffccbc
    style WR2 fill:#ffccbc
```

## API Security & Middleware

```mermaid
graph TD
    A["Incoming Request"]
    -->|1. CORS Check| B["CORS Middleware"]
    
    B -->|Pass| C["2. Request Parsing"]
    B -->|Fail| D["403 Forbidden"]
    
    C -->|3. Validation| E["Pydantic Schema"]
    E -->|Pass| F["4. Authentication<br/>Check"]
    E -->|Fail| G["400 Bad Request"]
    
    F -->|5. Rate Limit<br/>Optional| H["Process"]
    F -->|6. Execute| H
    
    H -->|7. Response| I["200/201/Error"]
    
    I -->|8. Logging| J["Log Entry"]
    J -->|Save| K["logs/running_logs.log"]
    
    style A fill:#c8e6c9
    style B fill:#fff9c4
    style C fill:#fff9c4
    style E fill:#fff9c4
    style F fill:#fff9c4
    style H fill:#ffe0b2
    style I fill:#d1c4e9
    style J fill:#b3e5fc
    style K fill:#c8e6c9
    style D fill:#ffcdd2
    style G fill:#ffcdd2
```

---

## Response Format Examples

### Success Response (200 OK)
```json
{
  "price": 15234.50,
  "confidence": 0.85,
  "features_received": 16
}
```

### Error Response (400 Bad Request)
```json
{
  "error": "Validation failed",
  "details": [
    {
      "field": "Prod. year",
      "message": "Value must be between 1900 and 2030"
    }
  ]
}
```

### Status Response (200 OK)
```json
{
  "model_loaded": true,
  "scaler_loaded": true,
  "model_path": "artifacts/training/model.pkl",
  "scaler_path": "artifacts/training/scaler.pkl",
  "timestamp": "2024-01-15T10:30:00"
}
```


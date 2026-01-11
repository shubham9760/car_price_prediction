# System Architecture

This document describes the overall system architecture of the Car Price Prediction project.

## High-Level System Architecture

```mermaid
graph TB
    subgraph "Data Layer"
        D1[Car Dataset]
        D2[Artifacts Storage]
    end
    
    subgraph "ML Pipeline"
        P1[Data Ingestion]
        P2[Base Model Prep]
        P3[Training]
        P4[Evaluation]
        P5[Prediction]
    end
    
    subgraph "API Layer"
        A1[Flask REST API]
        A2[Web Interface]
        A3[Swagger Docs]
    end
    
    subgraph "Analysis & Tracking"
        T1[Feature Importance]
        T2[Model Versioning]
        T3[MLflow Tracking]
    end
    
    subgraph "Deployment"
        DEP1[Docker Container]
        DEP2[docker-compose]
        DEP3[Services]
    end
    
    D1 --> P1
    P1 --> P2
    P2 --> P3
    P3 --> P4
    P4 --> P5
    
    P3 --> T1
    P3 --> T2
    P4 --> T3
    
    P5 --> A1
    A1 --> A2
    A1 --> A3
    
    D2 --> A1
    T1 --> A3
    T2 --> A3
    
    A1 --> DEP1
    DEP1 --> DEP2
    DEP2 --> DEP3
    
    style D1 fill:#e1f5e1
    style D2 fill:#e1f5e1
    style A1 fill:#e3f2fd
    style A2 fill:#e3f2fd
    style A3 fill:#e3f2fd
    style P1 fill:#fff3e0
    style P2 fill:#fff3e0
    style P3 fill:#fff3e0
    style P4 fill:#fff3e0
    style P5 fill:#fff3e0
    style T1 fill:#f3e5f5
    style T2 fill:#f3e5f5
    style T3 fill:#f3e5f5
    style DEP1 fill:#ffe0b2
    style DEP2 fill:#ffe0b2
    style DEP3 fill:#ffe0b2
```

## Component Relationships

```mermaid
graph LR
    subgraph "Configuration"
        CFG[ConfigurationManager]
        YAML[config.yaml]
        PARAMS[params.yaml]
    end
    
    subgraph "ML Components"
        DI[DataIngestion]
        PBM[PrepareBaseModel]
        TRN[Training]
        EVL[Evaluation]
        MC[ModelComparison]
        FI[FeatureImportance]
    end
    
    subgraph "API Components"
        API[Flask App]
        SCHEMA[PredictionSchema]
        TRACK[ModelTracking]
    end
    
    subgraph "Storage"
        MODELS[Model Artifacts]
        LOGS[Logs]
        VERSIONS[Version History]
    end
    
    CFG --> DI
    CFG --> PBM
    CFG --> TRN
    CFG --> EVL
    
    YAML --> CFG
    PARAMS --> CFG
    
    DI --> PBM
    PBM --> TRN
    TRN --> MC
    TRN --> FI
    TRN --> TRACK
    EVL --> MODELS
    
    API --> SCHEMA
    API --> TRACK
    API --> MODELS
    
    TRACK --> VERSIONS
    MC --> MODELS
    FI --> MODELS
    
    TRN --> LOGS
    EVL --> LOGS
    API --> LOGS
    
    style CFG fill:#bbdefb
    style DI fill:#fff9c4
    style PBM fill:#fff9c4
    style TRN fill:#fff9c4
    style EVL fill:#fff9c4
    style MC fill:#f8bbd0
    style FI fill:#f8bbd0
    style API fill:#c8e6c9
    style SCHEMA fill:#c8e6c9
    style TRACK fill:#d1c4e9
    style MODELS fill:#ffccbc
    style LOGS fill:#ffccbc
    style VERSIONS fill:#ffccbc
```

## Module Organization

```mermaid
classDiagram
    class ConfigurationManager {
        +get_data_ingestion_config()
        +get_prepare_base_model_config()
        +get_training_config()
        +get_evaluation_config()
    }
    
    class DataIngestion {
        +download_file()
        +extract_zip_file()
        +save_data()
    }
    
    class Training {
        +get_base_model()
        +train_full_model()
        +save_model()
        +save_scaler()
    }
    
    class ModelComparison {
        +run_comparison()
        +get_best_model()
        +save_comparison()
    }
    
    class FeatureImportance {
        +calculate_importance()
        +plot_features()
        +save_importance()
    }
    
    class PredictionSchema {
        +validate_features()
        +validate_dataframe()
    }
    
    class ModelTracking {
        +log_model()
        +log_metrics()
        +start_run()
        +end_run()
    }
    
    ConfigurationManager --> DataIngestion: configures
    ConfigurationManager --> Training: configures
    Training --> ModelComparison: uses
    Training --> FeatureImportance: uses
    Training --> ModelTracking: uses
    PredictionSchema --> ModelComparison: validates
    ModelTracking --|> ModelComparison: tracks
```

## Data Flow Overview

```mermaid
graph TD
    A[Raw Dataset] -->|Download & Extract| B[CSV File]
    B -->|Load| C[Pandas DataFrame]
    C -->|Cleaning & Preprocessing| D[Clean Data]
    D -->|Train/Test Split| E[Training Set]
    D -->|Train/Test Split| F[Test Set]
    E -->|Feature Scaling| G[Scaled Training Data]
    F -->|Feature Scaling| H[Scaled Test Data]
    G -->|Train Multiple Models| I[Model Selection]
    H -->|Evaluate| J[Metrics Calculation]
    I -->|Best Model| K[Production Model]
    J -->|Save Results| L[Artifacts Storage]
    K -->|Inference| M[Predictions]
    M -->|Return| N[API Response]
    
    style A fill:#c8e6c9
    style B fill:#c8e6c9
    style C fill:#fff9c4
    style D fill:#fff9c4
    style E fill:#ffe0b2
    style F fill:#ffe0b2
    style G fill:#ffccbc
    style H fill:#ffccbc
    style I fill:#f8bbd0
    style K fill:#d1c4e9
    style L fill:#b3e5fc
    style M fill:#d1c4e9
    style N fill:#a5d6a7
    style J fill:#fff3e0
```

## System Integration Points

```mermaid
graph TB
    subgraph "Input"
        UI["Web Form / API Request"]
        CSV["CSV Dataset"]
    end
    
    subgraph "Processing"
        LOAD["Data Loading"]
        PREP["Preprocessing"]
        TRAIN["Model Training"]
        EVAL["Evaluation"]
    end
    
    subgraph "Output"
        PRED["Predictions"]
        METRICS["Metrics"]
        VER["Version History"]
        LOGS["Application Logs"]
    end
    
    subgraph "Storage"
        ARTIFACTS["artifacts/"]
        MODELS["Models (.pkl)"]
        SCALERS["Scalers (.pkl)"]
    end
    
    subgraph "Monitoring"
        MLFLOW["MLflow Server"]
        LOGS_DIR["logs/"]
    end
    
    UI --> LOAD
    CSV --> LOAD
    LOAD --> PREP
    PREP --> TRAIN
    TRAIN --> EVAL
    EVAL --> PRED
    EVAL --> METRICS
    
    METRICS --> VER
    MODELS --> PRED
    SCALERS --> PRED
    
    TRAIN --> ARTIFACTS
    EVAL --> ARTIFACTS
    
    PRED --> UI
    METRICS --> LOGS
    VER --> MLFLOW
    LOGS --> LOGS_DIR
    
    style UI fill:#c8e6c9
    style CSV fill:#c8e6c9
    style LOAD fill:#fff9c4
    style PREP fill:#fff9c4
    style TRAIN fill:#ffe0b2
    style EVAL fill:#ffe0b2
    style PRED fill:#d1c4e9
    style METRICS fill:#f8bbd0
    style VER fill:#f8bbd0
    style LOGS fill:#f8bbd0
    style ARTIFACTS fill:#ffccbc
    style MODELS fill:#ffccbc
    style SCALERS fill:#ffccbc
    style MLFLOW fill:#b3e5fc
    style LOGS_DIR fill:#b3e5fc
```

---

## Key Integration Points

1. **Configuration Management** - Centralized config via ConfigurationManager
2. **Data Pipeline** - Sequential processing through stages
3. **Model Persistence** - Artifacts storage and versioning
4. **API Integration** - REST endpoints consume trained models
5. **Monitoring** - MLflow tracks experiments and metrics
6. **Logging** - Comprehensive logging throughout pipeline

---

## Scalability Considerations

- **Horizontal Scaling** - docker-compose allows multiple API instances
- **Data Scaling** - Batch processing for large datasets
- **Model Scaling** - Parallel training and evaluation
- **Storage Scaling** - Artifacts organized in versioned directories


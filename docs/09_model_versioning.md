# Model Versioning

This document explains how models are versioned, tracked, and managed using MLflow and local versioning systems.

## Model Versioning Architecture

```mermaid
graph TB
    A["Trained Models"]
    
    subgraph "Local Versioning"
        B["artifacts/training/"]
        B1["model.pkl - Current model"]
        B2["model_v1.pkl - Archived"]
        B3["model_v2.pkl - Archived"]
    end
    
    subgraph "MLflow Tracking"
        C["MLflow Server<br/>Port 5001"]
        C1["Experiment: car_price<br/>Run_id_1, Run_id_2, ..."]
        C2["Metrics: R², MSE, RMSE, MAE"]
        C3["Parameters: n_estimators,<br/>max_depth, learning_rate"]
        C4["Artifacts: model files,<br/>scaler, encoders"]
    end
    
    subgraph "Model Registry"
        D["Production Models"]
        D1["Stage: Staging"]
        D2["Stage: Production"]
        D3["Version: 1, 2, 3, ..."]
    end
    
    A --> B & C & D
    B --> B1 & B2 & B3
    C --> C1 & C2 & C3 & C4
    D --> D1 & D2 & D3
    
    style A fill:#c8e6c9
    style B fill:#fff9c4
    style B1 fill:#fff9c4
    style B2 fill:#fff9c4
    style B3 fill:#fff9c4
    style C fill:#ffe0b2
    style C1 fill:#ffe0b2
    style C2 fill:#ffe0b2
    style C3 fill:#ffe0b2
    style C4 fill:#ffe0b2
    style D fill:#ffccbc
    style D1 fill:#ffccbc
    style D2 fill:#ffccbc
    style D3 fill:#ffccbc
```

## MLflow Experiment Tracking

```mermaid
graph TD
    A["Training Job Started"]
    -->|Log| B["mlflow.start_run()"]
    
    B -->|Track| C["Experiment: car_price"]
    C -->|Set| C1["experiment_id"]
    C -->|Set| C2["run_id<br/>Unique identifier"]
    
    B -->|Log| D["Parameters"]
    D -->|Log| D1["n_estimators: 100"]
    D -->|Log| D2["max_depth: 5"]
    D -->|Log| D3["learning_rate: 0.1"]
    
    B -->|Log| E["Metrics<br/>After each fold"]
    E -->|Log| E1["train_r2_score"]
    E -->|Log| E2["val_r2_score"]
    E -->|Log| E3["train_mse"]
    E -->|Log| E4["val_mse"]
    
    B -->|Log| F["Artifacts"]
    F -->|Log| F1["model.pkl"]
    F -->|Log| F2["scaler.pkl"]
    F -->|Log| F3["encoders.pkl"]
    
    B -->|Log| G["Tags"]
    G -->|Log| G1["model_type: xgboost"]
    G -->|Log| G2["algorithm: gradient_boost"]
    
    C -->|Save| H["MLflow Backend<br/>Artifacts stored"]
    D -->|Save| H
    E -->|Save| H
    F -->|Save| H
    
    H -->|Persist| I["MLflow Server<br/>Port 5001"]
    
    style A fill:#c8e6c9
    style B fill:#fff9c4
    style C fill:#fff9c4
    style C1 fill:#fff9c4
    style C2 fill:#fff9c4
    style D fill:#ffe0b2
    style D1 fill:#ffe0b2
    style D2 fill:#ffe0b2
    style D3 fill:#ffe0b2
    style E fill:#ffe0b2
    style E1 fill:#ffe0b2
    style E2 fill:#ffe0b2
    style E3 fill:#ffe0b2
    style E4 fill:#ffe0b2
    style F fill:#ffccbc
    style F1 fill:#ffccbc
    style F2 fill:#ffccbc
    style F3 fill:#ffccbc
    style G fill:#ffccbc
    style G1 fill:#ffccbc
    style G2 fill:#ffccbc
    style H fill:#ffb74d
    style I fill:#a5d6a7
```

## Version Comparison Workflow

```mermaid
graph TD
    A["MLflow UI<br/>http://localhost:5001"]
    -->|Browse| B["Experiments List"]
    
    B -->|Select| C["car_price Experiment"]
    C -->|View| C1["Run 1: XGBoost<br/>R² = 0.88"]
    C -->|View| C2["Run 2: RF<br/>R² = 0.85"]
    C -->|View| C3["Run 3: XGBoost v2<br/>R² = 0.89"]
    
    C1 -->|Compare| D["Metrics Comparison"]
    C2 -->|Compare| D
    C3 -->|Compare| D
    
    D -->|Show| D1["XGBoost v2 Best<br/>+0.01 vs previous"]
    
    C1 -->|Compare| E["Parameters Comparison"]
    C2 -->|Compare| E
    C3 -->|Compare| E
    
    E -->|Show| E1["Parameter differences<br/>help identify<br/>winning settings"]
    
    D1 -->|Decision| F["Select Model<br/>for Production"]
    
    style A fill:#c8e6c9
    style B fill:#fff9c4
    style C fill:#fff9c4
    style C1 fill:#fff9c4
    style C2 fill:#fff9c4
    style C3 fill:#fff9c4
    style D fill:#ffe0b2
    style D1 fill:#ffe0b2
    style E fill:#ffe0b2
    style E1 fill:#ffe0b2
    style F fill:#ffccbc
```

## Model Promotion Pipeline

```mermaid
graph TD
    A["Model Ready for<br/>Production"]
    
    subgraph "Stage 1: Staging"
        B["Register Model<br/>in MLflow"]
        B1["Model Name: car_price_model"]
        B2["Version: 1"]
        B3["Stage: Staging"]
    end
    
    subgraph "Stage 2: Testing"
        C["A/B Testing<br/>on subset"]
        C1["Test with 10%<br/>of requests"]
        C2["Monitor metrics"]
        C3["Collect feedback"]
    end
    
    subgraph "Stage 3: Approval"
        D["Review Results"]
        D1["Compare with<br/>production model"]
        D2["Validate performance<br/>improvement"]
        D3["Get approval"]
    end
    
    subgraph "Stage 4: Production"
        E["Promote to<br/>Production"]
        E1["Update stage<br/>to Production"]
        E2["Route traffic<br/>to new model"]
        E3["Monitor in live<br/>environment"]
    end
    
    subgraph "Stage 5: Archive"
        F["Old Model<br/>Archived"]
        F1["Keep for<br/>rollback"]
        F2["Version history<br/>maintained"]
    end
    
    A --> B
    B --> B1 & B2 & B3
    B3 --> C
    C --> C1 & C2 & C3
    C3 --> D
    D --> D1 & D2 & D3
    D3 --> E
    E --> E1 & E2 & E3
    E3 --> F
    F --> F1 & F2
    
    style A fill:#c8e6c9
    style B fill:#fff9c4
    style B1 fill:#fff9c4
    style B2 fill:#fff9c4
    style B3 fill:#fff9c4
    style C fill:#ffe0b2
    style C1 fill:#ffe0b2
    style C2 fill:#ffe0b2
    style C3 fill:#ffe0b2
    style D fill:#ffccbc
    style D1 fill:#ffccbc
    style D2 fill:#ffccbc
    style D3 fill:#ffccbc
    style E fill:#ffb74d
    style E1 fill:#ffb74d
    style E2 fill:#ffb74d
    style E3 fill:#ffb74d
    style F fill:#b3e5fc
    style F1 fill:#b3e5fc
    style F2 fill:#b3e5fc
```

## Local Model Versioning System

```mermaid
graph TD
    A["Training Complete<br/>New Model"]
    -->|Save| B["model.pkl"]
    
    B -->|Check| C["Is this better?<br/>Compare R² scores"]
    
    C -->|Better| D["Version Up"]
    D -->|Rename| D1["model.pkl → model_v1.pkl"]
    D -->|Create| D2["new model.pkl"]
    D -->|Increment| D3["version = 2"]
    
    C -->|Worse| E["Keep Old<br/>Version"]
    E -->|Keep| E1["model.pkl unchanged"]
    E -->|Don't increment<br/>version"]
    
    D2 -->|Copy to| F["artifacts/training/"]
    D2 -->|Save| F1["model_v2.pkl"]
    
    F -->|Archive| F1
    F -->|Current| B
    
    subgraph "Local Version File"
        G["version.txt"]
        G1["Current version: 2"]
        G2["Best score: 0.88"]
        G3["Date created: 2024-01-15"]
    end
    
    D3 -->|Update| G
    G1 -.-> G
    
    style A fill:#c8e6c9
    style B fill:#fff9c4
    style C fill:#ffe0b2
    style D fill:#ffe0b2
    style D1 fill:#ffe0b2
    style D2 fill:#ffe0b2
    style D3 fill:#ffe0b2
    style E fill:#ffccbc
    style E1 fill:#ffccbc
    style F fill:#ffb74d
    style F1 fill:#ffb74d
    style G fill:#b3e5fc
    style G1 fill:#b3e5fc
    style G2 fill:#b3e5fc
    style G3 fill:#b3e5fc
```

## Model Metadata Tracking

```mermaid
graph TD
    subgraph "Model Information"
        A["Model Metadata"]
        A1["Name: car_price_model"]
        A2["Type: XGBoost Regressor"]
        A3["Created: 2024-01-15"]
        A4["Version: 2.0"]
    end
    
    subgraph "Training Data"
        B["Data Details"]
        B1["Samples: 384"]
        B2["Features: 11"]
        B3["Target: price"]
        B4["Date ingested: 2024-01-14"]
    end
    
    subgraph "Performance Metrics"
        C["Evaluation"]
        C1["R² Score: 0.88"]
        C2["MSE: 320M"]
        C3["RMSE: 17.9K"]
        C4["MAE: 11K"]
    end
    
    subgraph "Hyperparameters"
        D["Configuration"]
        D1["n_estimators: 100"]
        D2["max_depth: 5"]
        D3["learning_rate: 0.1"]
    end
    
    subgraph "Dependencies"
        E["Requirements"]
        E1["scikit-learn: 1.3.0"]
        E2["xgboost: latest"]
        E3["joblib: 1.3.1"]
    end
    
    A -->|Records| A1 & A2 & A3 & A4
    B -->|Records| B1 & B2 & B3 & B4
    C -->|Records| C1 & C2 & C3 & C4
    D -->|Records| D1 & D2 & D3
    E -->|Records| E1 & E2 & E3
    
    A1 -->|Stored in| F["MLflow<br/>model registry"]
    C1 -->|Stored in| F
    D1 -->|Stored in| F
    
    style A fill:#fff9c4
    style A1 fill:#fff9c4
    style A2 fill:#fff9c4
    style A3 fill:#fff9c4
    style A4 fill:#fff9c4
    style B fill:#ffe0b2
    style B1 fill:#ffe0b2
    style B2 fill:#ffe0b2
    style B3 fill:#ffe0b2
    style B4 fill:#ffe0b2
    style C fill:#ffccbc
    style C1 fill:#ffccbc
    style C2 fill:#ffccbc
    style C3 fill:#ffccbc
    style C4 fill:#ffccbc
    style D fill:#ffb74d
    style D1 fill:#ffb74d
    style D2 fill:#ffb74d
    style D3 fill:#ffb74d
    style E fill:#b3e5fc
    style E1 fill:#b3e5fc
    style E2 fill:#b3e5fc
    style E3 fill:#b3e5fc
    style F fill:#d1c4e9
```

## Version Management Sequence

```mermaid
sequenceDiagram
    participant Training as Training Code
    participant Local as Local Storage
    participant MLflow as MLflow Server
    participant Registry as Model Registry
    
    Training->>Local: Save model.pkl
    Training->>Local: Check existing version
    Local-->>Training: version = 1
    
    Training->>Local: Compare R² scores
    Local-->>Training: New > Old
    
    Training->>Local: Rename old model
    Local->>Local: model.pkl → model_v1.pkl
    
    Training->>Local: Save new model
    Local->>Local: New model.pkl created
    
    Training->>Local: Increment version
    Local->>Local: version.txt = 2
    
    Training->>MLflow: Log experiment run
    MLflow->>MLflow: Create run entry
    MLflow-->>Training: run_id
    
    Training->>MLflow: Log model artifact
    MLflow->>MLflow: Store model file
    
    Training->>Registry: Register model version
    Registry->>Registry: Create version 2
    Registry->>Registry: Set stage: Staging
    Registry-->>Training: Version registered
    
    Training-->>Training: Training complete
```

## Version History Example

```mermaid
graph TD
    A["Version History"]
    
    subgraph "Version 1"
        B["Date: 2024-01-14"]
        B1["Algorithm: Linear Regression"]
        B2["R² Score: 0.82"]
        B3["Status: Archived"]
    end
    
    subgraph "Version 2"
        C["Date: 2024-01-14 14:30"]
        C1["Algorithm: Random Forest"]
        C2["R² Score: 0.85"]
        C3["Status: Archived"]
    end
    
    subgraph "Version 3"
        D["Date: 2024-01-14 15:45"]
        D1["Algorithm: XGBoost"]
        D2["R² Score: 0.88"]
        D3["Status: Staging"]
    end
    
    subgraph "Version 4"
        E["Date: 2024-01-15 10:20"]
        E1["Algorithm: XGBoost (tuned)"]
        E2["R² Score: 0.89"]
        E3["Status: Production"]
    end
    
    A --> B & C & D & E
    B --> B1 & B2 & B3
    C --> C1 & C2 & C3
    D --> D1 & D2 & D3
    E --> E1 & E2 & E3
    
    B3 -->|Previous| C3
    C3 -->|Previous| D3
    D3 -->|Promoted| E3
    
    style A fill:#c8e6c9
    style B fill:#fff9c4
    style B1 fill:#fff9c4
    style B2 fill:#fff9c4
    style B3 fill:#fff9c4
    style C fill:#ffe0b2
    style C1 fill:#ffe0b2
    style C2 fill:#ffe0b2
    style C3 fill:#ffe0b2
    style D fill:#ffccbc
    style D1 fill:#ffccbc
    style D2 fill:#ffccbc
    style D3 fill:#ffccbc
    style E fill:#ffb74d
    style E1 fill:#ffb74d
    style E2 fill:#ffb74d
    style E3 fill:#ffb74d
```

## Rollback Mechanism

```mermaid
graph TD
    A["Problem Detected<br/>in Production"]
    -->|Alert| B["Latest Model<br/>Has issues"]
    
    B -->|Check| C["Version History"]
    C -->|Find| D["Previous Stable<br/>Version 3"]
    
    D -->|Load| E["model_v3.pkl<br/>from artifacts/"]
    E -->|Deploy| F["Switch to v3<br/>in API"]
    
    F -->|Update| G["model.pkl ← v3"]
    G -->|Restart| H["Flask API<br/>Reloads model"]
    
    H -->|Traffic| I["Requests now use<br/>v3 model"]
    I -->|Monitor| J["Check metrics"]
    
    J -->|Stable| K["✓ Rollback Complete<br/>Service restored"]
    
    B -->|Create| L["Incident Report<br/>Debug v4"]
    
    style A fill:#ef5350
    style B fill:#ef5350
    style C fill:#ffb74d
    style D fill:#fff9c4
    style E fill:#fff9c4
    style F fill:#ffe0b2
    style G fill:#ffe0b2
    style H fill:#ffccbc
    style I fill:#ffb74d
    style J fill:#ffb74d
    style K fill:#a5d6a7
    style L fill:#ffb74d
```

---

## Model Versioning Summary

**Versioning Strategy:**
- **Local Storage:** model.pkl, model_v1.pkl, model_v2.pkl
- **MLflow Registry:** Experiment tracking and version management
- **Metadata:** Stored with each version for full reproducibility

**Version Stages:**
- **Staging:** New model being tested
- **Production:** Current model serving requests
- **Archived:** Previous versions kept for rollback

**Key Artifacts Per Version:**
- model.pkl (trained model)
- scaler.pkl (feature scaling)
- encoders.pkl (categorical encoding)


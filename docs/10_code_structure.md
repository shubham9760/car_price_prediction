# Code Structure

This document outlines the project's module organization, class hierarchies, and component dependencies.

## Project Directory Structure

```mermaid
graph TD
    A["car_price_prediction/<br/>root"]
    
    A -->|Main Files| A1["main.py"]
    A -->|Main Files| A2["app.py<br/>Flask API"]
    A -->|Config| A3["config.yaml"]
    A -->|Config| A4["params.yaml"]
    A -->|Setup| A5["setup.py"]
    
    A -->|Source Code| B["src/"]
    B -->|Package| B1["car_price_prediction/"]
    B1 -->|Components| B2["components/"]
    B1 -->|Config| B3["config/"]
    B1 -->|Constants| B4["constants/"]
    B1 -->|Entities| B5["entity/"]
    B1 -->|Pipeline| B6["pipeline/"]
    B1 -->|Utils| B7["utils/"]
    
    A -->|Data| C["artifacts/"]
    C -->|Ingestion| C1["data_ingestion/"]
    C -->|Model| C2["prepare_base_model/"]
    C -->|Training| C3["training/"]
    
    A -->|Research| D["research/"]
    D -->|Notebooks| D1["stage_01_*.ipynb"]
    
    A -->|Documentation| E["docs/"]
    E -->|Diagrams| E1["*.md<br/>with Mermaid"]
    
    A -->|Deployment| F["Dockerfile<br/>docker-compose.yml"]
    
    style A fill:#c8e6c9
    style A1 fill:#fff9c4
    style A2 fill:#fff9c4
    style A3 fill:#fff9c4
    style A4 fill:#fff9c4
    style A5 fill:#fff9c4
    style B fill:#ffe0b2
    style B1 fill:#ffe0b2
    style B2 fill:#ffe0b2
    style B3 fill:#ffe0b2
    style B4 fill:#ffe0b2
    style B5 fill:#ffe0b2
    style B6 fill:#ffe0b2
    style B7 fill:#ffe0b2
    style C fill:#ffccbc
    style C1 fill:#ffccbc
    style C2 fill:#ffccbc
    style C3 fill:#ffccbc
    style D fill:#ffb74d
    style D1 fill:#ffb74d
    style E fill:#b3e5fc
    style E1 fill:#b3e5fc
    style F fill:#d1c4e9
```

## Components Organization

```mermaid
graph TD
    A["components/"]
    
    A -->|Stage 1| B["data_ingestion.py<br/>DataIngestion class"]
    B -->|Reads| B1["CSV files"]
    B -->|Outputs| B2["DataFrames"]
    
    A -->|Stage 2| C["prepare_base_model.py<br/>PrepareBaseModel class"]
    C -->|Creates| C1["Base model<br/>with preprocessing"]
    
    A -->|Stage 3| D["training.py<br/>Training class"]
    D -->|Trains| D1["ML models"]
    D -->|Saves| D2["model.pkl"]
    
    A -->|Stage 4| E["evaluation.py<br/>Evaluation class"]
    E -->|Calculates| E1["Metrics"]
    
    A -->|Stage 5| F["prepare_callbacks.py<br/>Callbacks class"]
    F -->|Manages| F1["Training callbacks<br/>Logging, saving"]
    
    A -->|Advanced| G["model_comparison.py<br/>ModelComparison"]
    G -->|Compares| G1["4 algorithms"]
    
    A -->|Advanced| H["feature_importance.py<br/>FeatureImportance"]
    H -->|Calculates| H1["Importance scores"]
    
    A -->|Validation| I["prediction_schema.py<br/>PredictionRequest"]
    I -->|Validates| I1["16 fields"]
    
    A -->|Tracking| J["model_tracking.py<br/>ModelTracking"]
    J -->|Tracks| J1["Versions<br/>Experiments"]
    
    style A fill:#c8e6c9
    style B fill:#fff9c4
    style B1 fill:#fff9c4
    style B2 fill:#fff9c4
    style C fill:#ffe0b2
    style C1 fill:#ffe0b2
    style D fill:#ffe0b2
    style D1 fill:#ffe0b2
    style D2 fill:#ffe0b2
    style E fill:#ffccbc
    style E1 fill:#ffccbc
    style F fill:#ffccbc
    style F1 fill:#ffccbc
    style G fill:#ffb74d
    style G1 fill:#ffb74d
    style H fill:#ffb74d
    style H1 fill:#ffb74d
    style I fill:#b3e5fc
    style I1 fill:#b3e5fc
    style J fill:#d1c4e9
    style J1 fill:#d1c4e9
```

## Pipeline Stages Structure

```mermaid
graph TD
    A["pipeline/"]
    
    A -->|Stage 1| B["stage_01_data_ingestion.py"]
    B -->|Implements| B1["DataIngestionPipeline<br/>class"]
    B1 -->|Calls| B2["DataIngestion component"]
    B2 -->|Output| B3["train/test data<br/>in artifacts/"]
    
    A -->|Stage 2| C["stage_02_prepare_base_model.py"]
    C -->|Implements| C1["PrepareBaseModelPipeline<br/>class"]
    C1 -->|Calls| C2["PrepareBaseModel"]
    C2 -->|Output| C3["base model<br/>in artifacts/"]
    
    A -->|Stage 3| D["stage_03_training.py"]
    D -->|Implements| D1["TrainingPipeline<br/>class"]
    D1 -->|Calls| D2["Training component"]
    D2 -->|Output| D3["model.pkl<br/>in artifacts/"]
    
    A -->|Stage 3 Advanced| D4["stage_03_advanced_training.py"]
    D4 -->|Implements| D5["AdvancedTrainingPipeline<br/>with CV"]
    D5 -->|Compares| D6["4 models<br/>5-fold CV"]
    
    A -->|Stage 4| E["stage_04_evaluation.py"]
    E -->|Implements| E1["EvaluationPipeline<br/>class"]
    E1 -->|Calls| E2["Evaluation component"]
    E2 -->|Output| E3["metrics<br/>in artifacts/"]
    
    A -->|Stage 5| F["stage_05_predict.py"]
    F -->|Implements| F1["PredictionPipeline<br/>class"]
    F1 -->|Loads| F2["model.pkl"]
    F2 -->|Output| F3["predictions"]
    
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
    style D4 fill:#ffccbc
    style D5 fill:#ffccbc
    style D6 fill:#ffccbc
    style E fill:#ffb74d
    style E1 fill:#ffb74d
    style E2 fill:#ffb74d
    style E3 fill:#ffb74d
    style F fill:#b3e5fc
    style F1 fill:#b3e5fc
    style F2 fill:#b3e5fc
    style F3 fill:#b3e5fc
```

## Configuration Architecture

```mermaid
graph TD
    A["config/"]
    
    A -->|Main| B["configuration.py"]
    B -->|Reads| B1["config.yaml"]
    B1 -->|Defines| B2["Artifact paths<br/>data, models, etc."]
    
    B -->|Creates| C["ConfigurationManager<br/>class"]
    C -->|Returns| C1["DataIngestionConfig"]
    C -->|Returns| C2["PrepareBaseModelConfig"]
    C -->|Returns| C3["TrainingConfig"]
    C -->|Returns| C4["EvaluationConfig"]
    
    B -->|Reads| D["params.yaml"]
    D -->|Defines| D1["EPOCHS<br/>BATCH_SIZE<br/>LEARNING_RATE<br/>etc."]
    
    A -->|Entity| E["entity/"]
    E -->|Dataclass| E1["ConfigEntity<br/>All config classes"]
    
    style A fill:#c8e6c9
    style B fill:#fff9c4
    style B1 fill:#fff9c4
    style B2 fill:#fff9c4
    style C fill:#ffe0b2
    style C1 fill:#ffe0b2
    style C2 fill:#ffe0b2
    style C3 fill:#ffe0b2
    style C4 fill:#ffe0b2
    style D fill:#ffccbc
    style D1 fill:#ffccbc
    style E fill:#ffb74d
    style E1 fill:#ffb74d
```

## Class Hierarchy and Relationships

```mermaid
graph TD
    A["DataIngestion"]
    B["PrepareBaseModel"]
    C["Training"]
    D["Evaluation"]
    E["PredictionPipeline"]
    
    A -->|Outputs| O1["X_train, X_test<br/>y_train, y_test"]
    O1 -->|Input| B
    
    B -->|Outputs| O2["base_model<br/>preprocessing"]
    O2 -->|Input| C
    
    C -->|Uses| F["ModelComparison<br/>ModelFactory"]
    F -->|Trains| F1["4 models"]
    F1 -->|Selects| O3["best_model"]
    O3 -->|Input| D
    
    C -->|Uses| G["FeatureImportance"]
    G -->|Calculates| O4["feature scores"]
    
    C -->|Uses| H["ModelTracking"]
    H -->|Logs| O5["MLflow experiments"]
    
    D -->|Outputs| O6["metrics<br/>R², MSE, RMSE, MAE"]
    O6 -->|Input| E
    
    E -->|Loads| O7["model.pkl<br/>scaler.pkl<br/>encoders.pkl"]
    O7 -->|Uses| I["PredictionSchema<br/>Pydantic"]
    I -->|Validates| O8["Input data"]
    O8 -->|Predicts| O9["price"]
    
    style A fill:#fff9c4
    style B fill:#ffe0b2
    style C fill:#ffccbc
    style D fill:#ffb74d
    style E fill:#b3e5fc
    style F fill:#ffccbc
    style G fill:#ffccbc
    style H fill:#ffccbc
    style I fill:#ffb74d
    style O1 fill:#fff9c4
    style O2 fill:#ffe0b2
    style O3 fill:#ffccbc
    style O4 fill:#ffccbc
    style O5 fill:#ffccbc
    style O6 fill:#ffb74d
    style O7 fill:#b3e5fc
    style O8 fill:#b3e5fc
    style O9 fill:#a5d6a7
```

## Data Flow Through Modules

```mermaid
sequenceDiagram
    participant Main as main.py
    participant P01 as Stage 1<br/>Ingestion
    participant P02 as Stage 2<br/>Base Model
    participant P03 as Stage 3<br/>Training
    participant P04 as Stage 4<br/>Evaluation
    participant P05 as Stage 5<br/>Prediction
    
    Main->>P01: Run pipeline
    P01->>P01: Load CSV
    P01-->>P01: Return X_train, y_train
    
    P01->>P02: Pass training data
    P02->>P02: Create preprocessing
    P02-->>P02: Return base model
    
    P02->>P03: Pass base model + data
    P03->>P03: Train 4 models
    P03->>P03: Select best (XGBoost)
    P03-->>P03: Return trained model
    
    P03->>P04: Pass model + test data
    P04->>P04: Calculate metrics
    P04-->>P04: Return R² = 0.88
    
    P04->>P05: Model ready
    P05->>P05: Load in API
    P05-->>P05: Ready for predictions
    
    Main-->>Main: All stages complete
```

## Utils Module Organization

```mermaid
graph TD
    A["utils/"]
    
    A -->|Common| B["common.py"]
    B -->|Functions| B1["read_yaml()"]
    B -->|Functions| B2["create_directories()"]
    B -->|Functions| B3["get_size()"]
    B -->|Functions| B4["save_json()"]
    B -->|Functions| B5["load_json()"]
    B -->|Functions| B6["save_binary()"]
    B -->|Functions| B7["load_binary()"]
    
    B -->|Utilities| C1["Logger setup"]
    B -->|Utilities| C2["Path handling"]
    B -->|Utilities| C3["File I/O"]
    
    style A fill:#c8e6c9
    style B fill:#fff9c4
    style B1 fill:#fff9c4
    style B2 fill:#fff9c4
    style B3 fill:#fff9c4
    style B4 fill:#fff9c4
    style B5 fill:#fff9c4
    style B6 fill:#fff9c4
    style B7 fill:#fff9c4
    style C1 fill:#ffe0b2
    style C2 fill:#ffe0b2
    style C3 fill:#ffe0b2
```

## Dependencies Between Modules

```mermaid
graph TB
    A["main.py"]
    -->|Imports| B["Pipeline Stages<br/>stage_01-05"]
    
    B -->|Depends| C["Components<br/>data_ingestion,<br/>training, etc."]
    
    C -->|Depends| D["Config<br/>configuration.py"]
    C -->|Depends| E["Entity<br/>config_entity.py"]
    C -->|Depends| F["Utils<br/>common.py"]
    
    D -->|Reads| G["config.yaml"]
    D -->|Reads| H["params.yaml"]
    
    C -->|Uses| I["External Libraries<br/>pandas, sklearn,<br/>joblib, MLflow"]
    
    A -->|Saves artifacts| J["artifacts/"]
    
    B -->|Also called by| K["app.py<br/>Flask API"]
    
    style A fill:#c8e6c9
    style B fill:#fff9c4
    style C fill:#ffe0b2
    style D fill:#ffccbc
    style E fill:#ffccbc
    style F fill:#ffccbc
    style G fill:#ffb74d
    style H fill:#ffb74d
    style I fill:#b3e5fc
    style J fill:#d1c4e9
    style K fill:#a5d6a7
```

## Module Import Structure

```mermaid
graph TD
    A["src/car_price_prediction/"]
    
    A -->|__init__.py| A1["Package initialization<br/>Version, author"]
    
    A -->|components/__init__.py| B["Export classes"]
    B -->|Exports| B1["DataIngestion"]
    B -->|Exports| B2["Training"]
    B -->|Exports| B3["Evaluation"]
    
    A -->|config/__init__.py| C["Export config"]
    C -->|Exports| C1["ConfigurationManager"]
    
    A -->|entity/__init__.py| D["Export entities"]
    D -->|Exports| D1["Config dataclasses"]
    
    A -->|pipeline/__init__.py| E["Export pipelines"]
    E -->|Exports| E1["All pipeline stages"]
    
    A -->|utils/__init__.py| F["Export utilities"]
    F -->|Exports| F1["Common functions"]
    
    style A fill:#c8e6c9
    style A1 fill:#fff9c4
    style B fill:#ffe0b2
    style B1 fill:#ffe0b2
    style B2 fill:#ffe0b2
    style B3 fill:#ffe0b2
    style C fill:#ffccbc
    style C1 fill:#ffccbc
    style D fill:#ffccbc
    style D1 fill:#ffccbc
    style E fill:#ffb74d
    style E1 fill:#ffb74d
    style F fill:#b3e5fc
    style F1 fill:#b3e5fc
```

## API Module Structure

```mermaid
graph TD
    A["app.py<br/>Flask API"]
    
    A -->|Define| B["Flask app<br/>create_app()"]
    
    A -->|Namespace 1| C["@app.route<br/>/ - Home"]
    A -->|Namespace 2| D["/api - API routes"]
    D -->|Endpoint| D1["POST /api/predict<br/>Single prediction"]
    D -->|Endpoint| D2["POST /api/predict/batch<br/>Batch prediction"]
    
    A -->|Namespace 3| E["/info - Info routes"]
    E -->|Endpoint| E1["GET /info/status<br/>API health"]
    E -->|Endpoint| E2["GET /info/features<br/>Feature importance"]
    
    A -->|Middleware| F["CORS<br/>Flask-CORS"]
    
    A -->|Documentation| G["Swagger UI<br/>Flask-RESTX"]
    G -->|Auto-docs| G1["/api/docs<br/>Interactive docs"]
    
    A -->|Dependencies| H["Components"]
    H -->|Uses| H1["PredictionSchema"]
    H -->|Uses| H2["Model loading<br/>joblib"]
    
    style A fill:#c8e6c9
    style B fill:#fff9c4
    style C fill:#ffe0b2
    style D fill:#ffe0b2
    style D1 fill:#ffe0b2
    style D2 fill:#ffe0b2
    style E fill:#ffccbc
    style E1 fill:#ffccbc
    style E2 fill:#ffccbc
    style F fill:#ffb74d
    style G fill:#ffb74d
    style G1 fill:#ffb74d
    style H fill:#b3e5fc
    style H1 fill:#b3e5fc
    style H2 fill:#b3e5fc
```

---

## Code Organization Summary

**Total Modules:** 20+ Python files  
**Main Components:** 8 core classes  
**Pipeline Stages:** 5 sequential stages  
**Configuration:** Centralized via YAML files  

**Key Organization Principles:**
- ✅ Modular design (each stage independent)
- ✅ Configuration-driven (params in YAML)
- ✅ Reusable components (classes for each function)
- ✅ Clear dependency flow (stage → component → util)
- ✅ API integration (Flask endpoints)
- ✅ Type safety (dataclasses and Pydantic)


# ML Pipeline Architecture

This document describes the machine learning pipeline with all 5 stages and their interactions.

## Complete ML Pipeline Flow

```mermaid
graph TD
    Start([Start Training Pipeline])
    
    subgraph "Stage 1: Data Ingestion"
        DI1["Download Dataset"]
        DI2["Extract ZIP"]
        DI3["Save CSV"]
    end
    
    subgraph "Stage 2: Base Model Preparation"
        PBM1["Load Data"]
        PBM2["Handle Missing Values"]
        PBM3["Encode Categories"]
        PBM4["Create Base Model"]
    end
    
    subgraph "Stage 3: Advanced Training"
        T1["Load Training Data"]
        T2["Preprocess Features"]
        T3["Train/Test Split"]
        T4["Apply Feature Scaling"]
        T5["Compare Models"]
        T6["Select Best Model"]
        T7["Track with MLflow"]
        T8["Version Model"]
    end
    
    subgraph "Stage 4: Evaluation"
        E1["Load Test Data"]
        E2["Make Predictions"]
        E3["Calculate Metrics"]
        E4["Save Results"]
    end
    
    subgraph "Stage 5: Prediction"
        P1["Load Trained Model"]
        P2["Validate Input"]
        P3["Preprocess Input"]
        P4["Generate Prediction"]
    end
    
    subgraph "Output"
        OUT1["Metrics JSON"]
        OUT2["Model Artifacts"]
        OUT3["Version History"]
        OUT4["Feature Importance"]
    end
    
    Start --> DI1
    DI1 --> DI2
    DI2 --> DI3
    DI3 --> PBM1
    PBM1 --> PBM2
    PBM2 --> PBM3
    PBM3 --> PBM4
    PBM4 --> T1
    T1 --> T2
    T2 --> T3
    T3 --> T4
    T4 --> T5
    T5 --> T6
    T6 --> T7
    T7 --> T8
    T8 --> E1
    E1 --> E2
    E2 --> E3
    E3 --> E4
    E4 --> OUT1
    T8 --> OUT2
    T8 --> OUT3
    E3 --> OUT4
    
    style Start fill:#4caf50
    style DI1 fill:#fff9c4
    style DI2 fill:#fff9c4
    style DI3 fill:#fff9c4
    style PBM1 fill:#ffe0b2
    style PBM2 fill:#ffe0b2
    style PBM3 fill:#ffe0b2
    style PBM4 fill:#ffe0b2
    style T1 fill:#ffccbc
    style T2 fill:#ffccbc
    style T3 fill:#ffccbc
    style T4 fill:#ffccbc
    style T5 fill:#f8bbd0
    style T6 fill:#f8bbd0
    style T7 fill:#d1c4e9
    style T8 fill:#d1c4e9
    style E1 fill:#b3e5fc
    style E2 fill:#b3e5fc
    style E3 fill:#b3e5fc
    style E4 fill:#b3e5fc
    style OUT1 fill:#c8e6c9
    style OUT2 fill:#c8e6c9
    style OUT3 fill:#c8e6c9
    style OUT4 fill:#c8e6c9
```

## Data Transformation Pipeline

```mermaid
graph LR
    A["Raw CSV<br/>429 KB"] 
    -->|Load| B["Pandas DataFrame<br/>429 rows × 16 cols"]
    -->|Replace '-'| C["Handle Missing<br/>Replace NaN"]
    -->|Label Encode| D["Categorical<br/>to Numeric"]
    -->|Median Fill| E["Numeric NaN<br/>Filled"]
    -->|Split 80/20| F["Train Set<br/>343 rows"]
    
    E -->|Split 80/20| G["Test Set<br/>86 rows"]
    
    F -->|StandardScaler| H["Scaled Features<br/>X_train"]
    G -->|StandardScaler| I["Scaled Features<br/>X_test"]
    
    H -->|Train| J["Model 1: LR"]
    H -->|Train| K["Model 2: RF"]
    H -->|Train| L["Model 3: XGB"]
    H -->|Train| M["Model 4: GB"]
    
    J -->|Evaluate| N["Best Model<br/>Selection"]
    K -->|Evaluate| N
    L -->|Evaluate| N
    M -->|Evaluate| N
    
    I -->|Predict| N
    N -->|Metrics| O["MSE, RMSE, MAE, R²"]
    N -->|Save| P["artifacts/training/"]
    
    style A fill:#c8e6c9
    style B fill:#fff9c4
    style C fill:#fff9c4
    style D fill:#fff9c4
    style E fill:#fff9c4
    style F fill:#ffe0b2
    style G fill:#ffe0b2
    style H fill:#ffccbc
    style I fill:#ffccbc
    style J fill:#f8bbd0
    style K fill:#f8bbd0
    style L fill:#f8bbd0
    style M fill:#f8bbd0
    style N fill:#d1c4e9
    style O fill:#c8e6c9
    style P fill:#c8e6c9
```

## Model Training Workflow

```mermaid
graph TD
    subgraph "Model Factory"
        MF1["Initialize<br/>4 Models"]
        MF2["Linear Regression"]
        MF3["Random Forest<br/>100 est"]
        MF4["XGBoost<br/>100 est"]
        MF5["Gradient Boosting<br/>100 est"]
    end
    
    subgraph "Training Phase"
        TR1["Train on<br/>X_train, y_train"]
        TR2["Model 1 Trained"]
        TR3["Model 2 Trained"]
        TR4["Model 3 Trained"]
        TR5["Model 4 Trained"]
    end
    
    subgraph "Evaluation Phase"
        EV1["5-Fold Cross<br/>Validation"]
        EV2["CV Scores"]
        EV3["Test Set<br/>Evaluation"]
        EV4["Performance<br/>Metrics"]
    end
    
    subgraph "Selection"
        SEL1["Compare<br/>Metrics"]
        SEL2["Select Best<br/>Model"]
    end
    
    subgraph "Finalization"
        FIN1["Feature<br/>Importance"]
        FIN2["MLflow<br/>Tracking"]
        FIN3["Version<br/>Model"]
        FIN4["Save<br/>Artifacts"]
    end
    
    MF1 --> MF2
    MF1 --> MF3
    MF1 --> MF4
    MF1 --> MF5
    
    MF2 --> TR1
    MF3 --> TR1
    MF4 --> TR1
    MF5 --> TR1
    
    TR1 --> TR2
    TR1 --> TR3
    TR1 --> TR4
    TR1 --> TR5
    
    TR2 --> EV1
    TR3 --> EV1
    TR4 --> EV1
    TR5 --> EV1
    
    EV1 --> EV2
    EV2 --> SEL1
    TR2 --> EV3
    TR3 --> EV3
    TR4 --> EV3
    TR5 --> EV3
    EV3 --> EV4
    EV4 --> SEL1
    
    SEL1 --> SEL2
    SEL2 --> FIN1
    SEL2 --> FIN2
    FIN2 --> FIN3
    FIN3 --> FIN4
    SEL2 --> FIN1
    
    style MF1 fill:#fff9c4
    style MF2 fill:#fff9c4
    style MF3 fill:#fff9c4
    style MF4 fill:#fff9c4
    style MF5 fill:#fff9c4
    style TR1 fill:#ffe0b2
    style TR2 fill:#ffe0b2
    style TR3 fill:#ffe0b2
    style TR4 fill:#ffe0b2
    style TR5 fill:#ffe0b2
    style EV1 fill:#ffccbc
    style EV2 fill:#ffccbc
    style EV3 fill:#ffccbc
    style EV4 fill:#ffccbc
    style SEL1 fill:#f8bbd0
    style SEL2 fill:#f8bbd0
    style FIN1 fill:#d1c4e9
    style FIN2 fill:#d1c4e9
    style FIN3 fill:#d1c4e9
    style FIN4 fill:#d1c4e9
```

## Data Preprocessing Details

```mermaid
graph TD
    A["Raw Features<br/>16 Columns"] 
    -->|Identify| B["Categorical<br/>Columns"]
    B -->|LabelEncode| C["Numeric<br/>Categories"]
    
    A -->|Check| D["Missing<br/>Values"]
    D -->|Replace '-'| E["String '-'<br/>to NaN"]
    E -->|Fill| F["Numeric NaN<br/>with Median"]
    
    C --> G["Preprocessed<br/>Data"]
    F --> G
    
    G -->|StandardScaler| H["Fit on<br/>Train Data"]
    G -->|StandardScaler| I["Transform<br/>Test Data"]
    
    H --> J["Scaled<br/>X_train"]
    I --> K["Scaled<br/>X_test"]
    
    J --> L["Ready for<br/>Training"]
    K --> M["Ready for<br/>Evaluation"]
    
    style A fill:#c8e6c9
    style B fill:#fff9c4
    style C fill:#fff9c4
    style D fill:#fff9c4
    style E fill:#fff9c4
    style F fill:#fff9c4
    style G fill:#ffe0b2
    style H fill:#ffccbc
    style I fill:#ffccbc
    style J fill:#f8bbd0
    style K fill:#f8bbd0
    style L fill:#d1c4e9
    style M fill:#d1c4e9
```

## Pipeline Execution Order

```mermaid
sequenceDiagram
    participant main.py as main.py
    participant Stage1 as Stage 1:<br/>Ingestion
    participant Stage2 as Stage 2:<br/>Base Model
    participant Stage3 as Stage 3:<br/>Training
    participant Stage4 as Stage 4:<br/>Evaluation
    participant Artifacts as Artifacts<br/>Storage

    main.py->>Stage1: Execute
    Stage1->>Artifacts: Save Data
    main.py->>Stage2: Execute
    Stage2->>Artifacts: Save Base Model
    main.py->>Stage3: Execute
    Stage3->>Stage3: 1. Load Data
    Stage3->>Stage3: 2. Preprocess
    Stage3->>Stage3: 3. Train Models
    Stage3->>Stage3: 4. Select Best
    Stage3->>Artifacts: Save Model
    main.py->>Stage4: Execute
    Stage4->>Artifacts: Load Model
    Stage4->>Stage4: Evaluate
    Stage4->>Artifacts: Save Metrics
    main.py->>main.py: Pipeline Complete
```

## Model Selection Process

```mermaid
graph TD
    A["4 Trained Models"]
    A -->|Model 1| B1["Linear Regression<br/>R²: -0.15"]
    A -->|Model 2| B2["Random Forest<br/>R²: 0.45"]
    A -->|Model 3| B3["XGBoost<br/>R²: 0.52"]
    A -->|Model 4| B4["Gradient Boost<br/>R²: 0.48"]
    
    B1 -->|Compare| C["Evaluation<br/>Metrics"]
    B2 -->|Compare| C
    B3 -->|Compare| C
    B4 -->|Compare| C
    
    C -->|Highest R²| D["XGBoost<br/>Selected"]
    C -->|Save Results| E["model_comparison.json"]
    
    D -->|Use for| F["Feature Importance"]
    D -->|Save| G["Production Model"]
    D -->|Track| H["MLflow"]
    D -->|Version| I["Version History"]
    
    style A fill:#fff9c4
    style B1 fill:#ffccbc
    style B2 fill:#ffccbc
    style B3 fill:#ffccbc
    style B4 fill:#ffccbc
    style C fill:#f8bbd0
    style D fill:#d1c4e9
    style E fill:#c8e6c9
    style F fill:#d1c4e9
    style G fill:#c8e6c9
    style H fill:#b3e5fc
    style I fill:#b3e5fc
```

---

## Key Metrics Tracked

| Stage | Metrics | Output |
|-------|---------|--------|
| **Stage 3** | CV R², Test R², RMSE, MAE, MSE | model_comparison.json |
| **Stage 4** | R², RMSE, MAE, MSE | scores.json |
| **Training** | Feature Importance | feature_importance.csv |
| **Tracking** | Experiment metrics | MLflow Server |

---

## Pipeline Configuration

- **Cross-Validation Folds:** 5
- **Train/Test Split:** 80/20
- **Feature Scaling:** StandardScaler
- **Random State:** 42
- **Number of Models:** 4
- **Feature Count:** 16


# Technology Stack

This document provides a comprehensive overview of all technologies, libraries, and tools used in the Car Price Prediction project.

## Complete Technology Stack Architecture

```mermaid
graph TB
    subgraph "Application Layer"
        APP["Car Price<br/>Prediction System"]
    end
    
    subgraph "Web Framework"
        FLASK["Flask 3.0.0"]
        RESTX["Flask-RESTX<br/>Swagger UI"]
        CORS["Flask-CORS<br/>Cross-Origin"]
    end
    
    subgraph "Data Science"
        PANDAS["pandas 2.0.3<br/>Data manipulation"]
        NUMPY["numpy 1.24.3<br/>Numerical ops"]
        SK["scikit-learn 1.3.0<br/>ML algorithms"]
    end
    
    subgraph "Machine Learning Models"
        LR["Linear Regression"]
        RF["Random Forest<br/>n_estimators=50"]
        XGB["XGBoost<br/>n_estimators=100"]
        GB["Gradient Boosting<br/>n_estimators=100"]
    end
    
    subgraph "Model Serialization"
        JOBLIB["joblib 1.3.1<br/>Model saving"]
        PICKLE["pickle<br/>Serialization"]
    end
    
    subgraph "Data Validation"
        PYDANTIC["Pydantic 2.0<br/>Schema validation"]
    end
    
    subgraph "Monitoring & Tracking"
        MLFLOW["MLflow 2.0<br/>Experiment tracking"]
        DVC["DVC 3.0<br/>Data versioning"]
    end
    
    subgraph "Visualization"
        MPL["matplotlib 3.7.2<br/>Static plots"]
        SEABORN["seaborn 0.12.2<br/>Statistical viz"]
    end
    
    subgraph "Deployment"
        DOCKER["Docker<br/>Containerization"]
        COMPOSE["docker-compose<br/>Orchestration"]
    end
    
    subgraph "Development"
        PYTHON["Python 3.11<br/>Runtime"]
        SETUPTOOLS["setuptools<br/>Packaging"]
    end
    
    APP --> FLASK
    APP --> PANDAS
    APP --> SK
    
    FLASK --> RESTX
    FLASK --> CORS
    FLASK --> PYDANTIC
    
    PANDAS --> NUMPY
    NUMPY --> SK
    
    SK --> LR & RF & XGB & GB
    
    LR --> JOBLIB
    RF --> JOBLIB
    XGB --> JOBLIB
    GB --> JOBLIB
    
    JOBLIB --> PICKLE
    
    APP --> MLFLOW
    APP --> DVC
    
    SK --> MPL
    SK --> SEABORN
    
    APP --> DOCKER
    DOCKER --> COMPOSE
    
    PYTHON --> APP
    SETUPTOOLS --> PYTHON
    
    style APP fill:#c8e6c9
    style FLASK fill:#fff9c4
    style RESTX fill:#fff9c4
    style CORS fill:#fff9c4
    style PANDAS fill:#ffe0b2
    style NUMPY fill:#ffe0b2
    style SK fill:#ffe0b2
    style LR fill:#ffccbc
    style RF fill:#ffccbc
    style XGB fill:#ffccbc
    style GB fill:#ffccbc
    style JOBLIB fill:#ffb74d
    style PICKLE fill:#ffb74d
    style PYDANTIC fill:#ffb74d
    style MLFLOW fill:#b3e5fc
    style DVC fill:#b3e5fc
    style MPL fill:#d1c4e9
    style SEABORN fill:#d1c4e9
    style DOCKER fill:#a5d6a7
    style COMPOSE fill:#a5d6a7
    style PYTHON fill:#c8e6c9
    style SETUPTOOLS fill:#c8e6c9
```

## Dependency Tree

```mermaid
graph TD
    PYTHON["Python 3.11"]
    
    PYTHON -->|Core| NUMPY["numpy 1.24.3"]
    PYTHON -->|Core| PANDAS["pandas 2.0.3"]
    PYTHON -->|Core| FLASK["Flask 3.0.0"]
    PYTHON -->|Core| PYDANTIC["Pydantic 2.0"]
    
    NUMPY -->|Math| SK["scikit-learn 1.3.0"]
    PANDAS -->|DataFrame| SK
    
    SK -->|Models| SKLEARN_LR["LR, RF, XGB, GB"]
    
    PANDAS -->|Export| MATPLOTLIB["matplotlib 3.7.2"]
    SK -->|Viz| SEABORN["seaborn 0.12.2"]
    
    PYTHON -->|Serialize| JOBLIB["joblib 1.3.1"]
    JOBLIB -->|Save Models| MODELS["model.pkl"]
    JOBLIB -->|Save Scalers| SCALERS["scaler.pkl"]
    JOBLIB -->|Save Encoders| ENCODERS["encoders.pkl"]
    
    FLASK -->|Extend| RESTX["Flask-RESTX"]
    FLASK -->|Extend| CORS["Flask-CORS"]
    
    PYDANTIC -->|Validation| SCHEMAS["Request Schema"]
    
    PYTHON -->|Tracking| MLFLOW["MLflow 2.0"]
    PYTHON -->|Version| DVC["DVC 3.0"]
    
    PYTHON -->|Deploy| DOCKER["Docker"]
    DOCKER -->|Orchestrate| COMPOSE["docker-compose"]
    
    PYTHON -->|Package| SETUPTOOLS["setuptools"]
    
    style PYTHON fill:#c8e6c9
    style NUMPY fill:#fff9c4
    style PANDAS fill:#fff9c4
    style FLASK fill:#fff9c4
    style PYDANTIC fill:#fff9c4
    style SK fill:#ffe0b2
    style SKLEARN_LR fill:#ffe0b2
    style MATPLOTLIB fill:#ffe0b2
    style SEABORN fill:#ffe0b2
    style JOBLIB fill:#ffccbc
    style MODELS fill:#ffccbc
    style SCALERS fill:#ffccbc
    style ENCODERS fill:#ffccbc
    style RESTX fill:#ffb74d
    style CORS fill:#ffb74d
    style SCHEMAS fill:#ffb74d
    style MLFLOW fill:#b3e5fc
    style DVC fill:#b3e5fc
    style DOCKER fill:#d1c4e9
    style COMPOSE fill:#d1c4e9
    style SETUPTOOLS fill:#c8e6c9
```

## Core Libraries Details

```mermaid
graph TB
    subgraph "Data Manipulation"
        A["pandas<br/>Version: 2.0.3<br/>Purpose: DataFrames<br/>CSV read/write<br/>Data cleaning"]
        B["numpy<br/>Version: 1.24.3<br/>Purpose: Arrays<br/>Math operations<br/>Matrix operations"]
    end
    
    subgraph "Machine Learning"
        C["scikit-learn<br/>Version: 1.3.0<br/>Algorithms:<br/>- LinearRegression<br/>- RandomForestRegressor<br/>- XGBRegressor<br/>- GradientBoostingRegressor<br/>Tools:<br/>- train_test_split<br/>- StandardScaler<br/>- LabelEncoder<br/>- cross_val_score"]
    end
    
    subgraph "Web Framework"
        D["Flask<br/>Version: 3.0.0<br/>Purpose: REST API<br/>HTTP routing<br/>Request handling"]
        E["Flask-RESTX<br/>Purpose: API extension<br/>Automatic Swagger<br/>Namespace organization"]
        F["Flask-CORS<br/>Purpose: Cross-Origin<br/>CORS headers"]
    end
    
    subgraph "Data Validation"
        G["Pydantic<br/>Version: 2.0<br/>Purpose: Schema validation<br/>Type checking<br/>Custom validators<br/>Error messages"]
    end
    
    subgraph "Model Management"
        H["joblib<br/>Version: 1.3.1<br/>Purpose: Save/load models<br/>Save scalers<br/>Save encoders"]
        I["pickle<br/>Purpose: Serialization<br/>Alternative to joblib"]
    end
    
    subgraph "Visualization"
        J["matplotlib<br/>Version: 3.7.2<br/>Purpose: Static plots<br/>Charts, graphs<br/>Feature importance"]
        K["seaborn<br/>Version: 0.12.2<br/>Purpose: Statistical plots<br/>Enhanced visuals"]
    end
    
    subgraph "Monitoring"
        L["MLflow<br/>Version: 2.0<br/>Purpose: Experiment tracking<br/>Model versioning<br/>Metrics logging"]
        M["DVC<br/>Version: 3.0<br/>Purpose: Data versioning<br/>Pipeline tracking"]
    end
    
    style A fill:#fff9c4
    style B fill:#fff9c4
    style C fill:#ffe0b2
    style D fill:#ffccbc
    style E fill:#ffccbc
    style F fill:#ffccbc
    style G fill:#ffb74d
    style H fill:#ffb74d
    style I fill:#ffb74d
    style J fill:#b3e5fc
    style K fill:#b3e5fc
    style L fill:#d1c4e9
    style M fill:#d1c4e9
```

## Integration Points

```mermaid
graph TD
    A["Pipeline Stages"]
    
    A -->|Stage 1| B["Data Ingestion"]
    B -->|Uses| B1["pandas"]
    B -->|Outputs| B2["DataFrame"]
    
    A -->|Stage 2| C["Prepare Base Model"]
    C -->|Uses| C1["sklearn"]
    C -->|Uses| C2["numpy"]
    C -->|Outputs| C3["Base model ready"]
    
    A -->|Stage 3| D["Training"]
    D -->|Uses| D1["sklearn models"]
    D -->|Uses| D2["joblib"]
    D -->|Uses| D3["MLflow"]
    D -->|Outputs| D4["model.pkl"]
    
    A -->|Stage 4| E["Evaluation"]
    E -->|Uses| E1["sklearn metrics"]
    E -->|Uses| E2["matplotlib"]
    E -->|Outputs| E3["Metrics report"]
    
    A -->|Stage 5| F["Prediction"]
    F -->|Uses| F1["joblib<br/>load"]
    F -->|Uses| F2["numpy"]
    F -->|Outputs| F3["Price prediction"]
    
    B2 -->|Powers| G["Flask API"]
    D4 -->|Powers| G
    
    G -->|Uses| G1["Flask-RESTX"]
    G -->|Uses| G2["Pydantic"]
    G -->|Uses| G3["Flask-CORS"]
    
    D4 -->|Tracked by| H["MLflow Server"]
    
    G -->|Containerized| I["Docker"]
    H -->|Orchestrated| I
    I -->|Uses| J["docker-compose"]
    
    style A fill:#c8e6c9
    style B fill:#fff9c4
    style B1 fill:#fff9c4
    style B2 fill:#fff9c4
    style C fill:#ffe0b2
    style C1 fill:#ffe0b2
    style C2 fill:#ffe0b2
    style C3 fill:#ffe0b2
    style D fill:#ffccbc
    style D1 fill:#ffccbc
    style D2 fill:#ffccbc
    style D3 fill:#ffccbc
    style D4 fill:#ffccbc
    style E fill:#ffb74d
    style E1 fill:#ffb74d
    style E2 fill:#ffb74d
    style E3 fill:#ffb74d
    style F fill:#b3e5fc
    style F1 fill:#b3e5fc
    style F2 fill:#b3e5fc
    style F3 fill:#b3e5fc
    style G fill:#d1c4e9
    style G1 fill:#d1c4e9
    style G2 fill:#d1c4e9
    style G3 fill:#d1c4e9
    style H fill:#a5d6a7
    style I fill:#a5d6a7
    style J fill:#a5d6a7
```

## Version Matrix

```mermaid
graph TB
    subgraph "Core Runtime"
        PYTHON["Python 3.11.0<br/>Latest stable<br/>Linux/Mac/Windows"]
    end
    
    subgraph "Data Stack (Latest)"
        PANDAS["pandas 2.0.3"]
        NUMPY["numpy 1.24.3"]
    end
    
    subgraph "ML Stack (Latest)"
        SK["scikit-learn 1.3.0"]
        JOBLIB["joblib 1.3.1"]
    end
    
    subgraph "Web Framework (Latest)"
        FLASK["Flask 3.0.0"]
        RESTX["Flask-RESTX"]
        CORS["Flask-CORS"]
    end
    
    subgraph "Validation (Latest)"
        PYDANTIC["Pydantic 2.0"]
    end
    
    subgraph "Visualization (Latest)"
        MPL["matplotlib 3.7.2"]
        SEABORN["seaborn 0.12.2"]
    end
    
    subgraph "DevOps (Latest)"
        MLFLOW["MLflow 2.0"]
        DVC["DVC 3.0"]
        DOCKER["Docker (latest)"]
    end
    
    PYTHON --> PANDAS & NUMPY & SK & FLASK & PYDANTIC & MPL & MLFLOW
    
    style PYTHON fill:#c8e6c9
    style PANDAS fill:#fff9c4
    style NUMPY fill:#fff9c4
    style SK fill:#ffe0b2
    style JOBLIB fill:#ffe0b2
    style FLASK fill:#ffccbc
    style RESTX fill:#ffccbc
    style CORS fill:#ffccbc
    style PYDANTIC fill:#ffb74d
    style MPL fill:#b3e5fc
    style SEABORN fill:#b3e5fc
    style MLFLOW fill:#d1c4e9
    style DVC fill:#d1c4e9
    style DOCKER fill:#a5d6a7
```

## Development & Deployment Tools

```mermaid
graph TD
    subgraph "Development"
        A["Source Control<br/>Git/GitHub"]
        B["Version Control<br/>DVC"]
        C["Code Editor<br/>VS Code"]
    end
    
    subgraph "Testing & Validation"
        D["Pytest<br/>Unit testing"]
        E["Black<br/>Code formatting"]
        F["Pylint<br/>Linting"]
    end
    
    subgraph "ML Operations"
        G["MLflow<br/>Experiment tracking<br/>Model registry"]
        H["DVC<br/>Pipeline tracking<br/>Data versioning"]
    end
    
    subgraph "Containerization"
        I["Docker<br/>Image creation<br/>Multi-stage builds"]
        J["docker-compose<br/>Service orchestration<br/>Volume management"]
    end
    
    subgraph "Production"
        K["Flask API<br/>REST endpoints<br/>Port 5000"]
        L["MLflow Server<br/>Model tracking<br/>Port 5001"]
    end
    
    A -->|Track code| E & F
    B -->|Track data| H
    C -->|Edit| A & B
    E -->|Format| D
    F -->|Lint| D
    D -->|Validate| G & H
    G -->|Register models| I
    H -->|Version data| I
    I -->|Build| J
    J -->|Launch| K & L
    
    style A fill:#c8e6c9
    style B fill:#c8e6c9
    style C fill:#c8e6c9
    style D fill:#fff9c4
    style E fill:#fff9c4
    style F fill:#fff9c4
    style G fill:#ffe0b2
    style H fill:#ffe0b2
    style I fill:#ffccbc
    style J fill:#ffccbc
    style K fill:#ffb74d
    style L fill:#ffb74d
```

## Technology Selection Rationale

```mermaid
graph TD
    A["Technology Choices"]
    
    A -->|Python| B["Reason:<br/>- Industry standard for ML<br/>- Rich ecosystem<br/>- Easy to learn"]
    
    A -->|scikit-learn| C["Reason:<br/>- Simple API<br/>- 4 algorithms ready<br/>- Production stable"]
    
    A -->|Flask| D["Reason:<br/>- Lightweight<br/>- Flexible<br/>- Easy to extend"]
    
    A -->|Pydantic| E["Reason:<br/>- Type safety<br/>- Auto validation<br/>- Clear errors"]
    
    A -->|Docker| F["Reason:<br/>- Reproducibility<br/>- Easy deployment<br/>- Platform independent"]
    
    A -->|MLflow| G["Reason:<br/>- Experiment tracking<br/>- Model registry<br/>- Production ready"]
    
    A -->|pandas| H["Reason:<br/>- Standard data tool<br/>- Easy CSV handling<br/>- Rich operations"]
    
    style A fill:#c8e6c9
    style B fill:#fff9c4
    style C fill:#ffe0b2
    style D fill:#ffccbc
    style E fill:#ffb74d
    style F fill:#b3e5fc
    style G fill:#d1c4e9
    style H fill:#a5d6a7
```

---

## Summary

**Total Dependencies:** 20+ libraries  
**Python Version:** 3.11 (latest stable)  
**Latest Package Versions:** All major packages at latest stable versions  
**Compatibility:** Tested on Python 3.11, Docker available for containerization  

**Key Technology Categories:**
- **Data Processing:** pandas, numpy
- **Machine Learning:** scikit-learn, 4 algorithms
- **Web API:** Flask, Flask-RESTX, Pydantic
- **Model Management:** joblib, MLflow
- **Visualization:** matplotlib, seaborn
- **Deployment:** Docker, docker-compose
- **Version Control:** Git, DVC


# Data Flow

This document describes how data flows through the entire system, from ingestion to prediction.

## Complete Data Processing Pipeline

```mermaid
graph TD
    A["Raw Data<br/>CSV File"]
    -->|Load| B["pandas.read_csv()"]
    
    B -->|DataFrame| C["Initial Data<br/>~500 rows<br/>16 columns"]
    
    C -->|Inspect| D["Data Profiling"]
    D -->|Missing Values| D1["Check NaN"]
    D -->|Data Types| D2["Check dtype"]
    D -->|Statistics| D3["Describe()"]
    
    C -->|Separate| E["Feature Engineering"]
    E -->|Categorical| E1["Brand, Model, Transmission<br/>Fuel Type, Owner Type"]
    E -->|Numerical| E2["Year, Mileage, Engine CC<br/>Power, Seats"]
    E -->|Target| E3["Price<br/>Regression Target"]
    
    E -->|Process| F["Data Cleaning"]
    F -->|Handle NaN| F1["Drop/Fill Missing"]
    F -->|Remove Duplicates| F2["Drop Duplicates"]
    F -->|Remove Outliers| F3["IQR Method"]
    
    F -->|Transform| G["Categorical Encoding"]
    G -->|LabelEncoder| G1["Brand → 0-n"]
    G -->|LabelEncoder| G2["Model → 0-m"]
    G -->|LabelEncoder| G3["Transmission → 0-3"]
    G -->|LabelEncoder| G4["Fuel Type → 0-3"]
    G -->|LabelEncoder| G5["Owner Type → 0-2"]
    
    G -->|Scale| H["Feature Scaling<br/>StandardScaler"]
    H -->|Normalize| H1["All Features<br/>μ=0, σ=1"]
    
    H -->|Split| I["Train-Test Split"]
    I -->|80%| I1["Training Set<br/>400 samples"]
    I -->|20%| I2["Test Set<br/>100 samples"]
    
    I1 -->|Train| J["Model Training<br/>4 Algorithms"]
    I2 -->|Evaluate| K["Model Evaluation"]
    
    J -->|Linear| J1["Linear Regression"]
    J -->|Forest| J2["Random Forest"]
    J -->|Boosting| J3["XGBoost"]
    J -->|Gradient| J4["Gradient Boosting"]
    
    K -->|Metrics| K1["R² Score"]
    K -->|Metrics| K2["MSE"]
    K -->|Metrics| K3["RMSE"]
    K -->|Metrics| K4["MAE"]
    
    K -->|Best Model| L["Model Selection<br/>Highest R²"]
    
    L -->|Save| M["Model Artifacts"]
    M -->|Binary| M1["model.pkl<br/>joblib format"]
    M -->|Scaler| M2["scaler.pkl<br/>Feature scaling"]
    M -->|Encoders| M3["encoders.pkl<br/>Categorical"]
    
    M -->|Load at Runtime| N["API Prediction"]
    N -->|Input| O["New Features<br/>16 values"]
    O -->|Preprocess| P["Apply Same<br/>Transformations"]
    P -->|Encode| P1["Categorical<br/>using saved encoders"]
    P -->|Scale| P2["Numerical<br/>using saved scaler"]
    P -->|Array| P3["Feature Vector<br/>1 × 11"]
    P3 -->|Predict| Q["Loaded Model<br/>model.pkl"]
    Q -->|Output| R["Price Prediction<br/>₹ value"]
    
    style A fill:#c8e6c9
    style B fill:#fff9c4
    style C fill:#fff9c4
    style D fill:#fff9c4
    style D1 fill:#fff9c4
    style D2 fill:#fff9c4
    style D3 fill:#fff9c4
    style E fill:#ffe0b2
    style E1 fill:#ffe0b2
    style E2 fill:#ffe0b2
    style E3 fill:#ffe0b2
    style F fill:#ffe0b2
    style F1 fill:#ffe0b2
    style F2 fill:#ffe0b2
    style F3 fill:#ffe0b2
    style G fill:#ffccbc
    style G1 fill:#ffccbc
    style G2 fill:#ffccbc
    style G3 fill:#ffccbc
    style G4 fill:#ffccbc
    style G5 fill:#ffccbc
    style H fill:#ffccbc
    style H1 fill:#ffccbc
    style I fill:#ffb74d
    style I1 fill:#ffb74d
    style I2 fill:#ffb74d
    style J fill:#b3e5fc
    style J1 fill:#b3e5fc
    style J2 fill:#b3e5fc
    style J3 fill:#b3e5fc
    style J4 fill:#b3e5fc
    style K fill:#b3e5fc
    style K1 fill:#b3e5fc
    style K2 fill:#b3e5fc
    style K3 fill:#b3e5fc
    style K4 fill:#b3e5fc
    style L fill:#d1c4e9
    style M fill:#d1c4e9
    style M1 fill:#d1c4e9
    style M2 fill:#d1c4e9
    style M3 fill:#d1c4e9
    style N fill:#a5d6a7
    style O fill:#a5d6a7
    style P fill:#a5d6a7
    style P1 fill:#a5d6a7
    style P2 fill:#a5d6a7
    style P3 fill:#a5d6a7
    style Q fill:#a5d6a7
    style R fill:#a5d6a7
```

## Data Preprocessing Details

```mermaid
graph TD
    A["Raw Data"]
    
    subgraph "Step 1: Load"
        B["CSV → DataFrame<br/>car_price_prediction.csv"]
    end
    
    subgraph "Step 2: Inspect"
        C["Check Shape"]
        D["Check Dtypes"]
        E["Check Missing Values"]
        F["View Statistics"]
    end
    
    subgraph "Step 3: Handle Missing"
        G["Identify NaN"]
        H["Strategy: Drop Row<br/>if NaN in any column"]
    end
    
    subgraph "Step 4: Remove Duplicates"
        I["Drop Duplicate<br/>Rows"]
    end
    
    subgraph "Step 5: Categorical Encoding"
        J["LabelEncoder<br/>for each categorical"]
        J1["Brand: 0-48"]
        J2["Model: 0-126"]
        J3["Transmission: 0-3"]
        J4["Fuel Type: 0-3"]
        J5["Owner Type: 0-2"]
    end
    
    subgraph "Step 6: Feature Scaling"
        K["StandardScaler"]
        K1["μ = 0"]
        K2["σ = 1"]
    end
    
    subgraph "Step 7: Prepare Features"
        L["Select 11 Features<br/>Drop: Name, Price"]
        M["Features: Brand, Model, Year,<br/>Mileage, Engine CC, Power,<br/>Transmission, Fuel, Owner Type,<br/>Seats, New/Used"]
    end
    
    A --> B
    B --> C & D & E & F
    C --> G
    D --> G
    E --> G
    F --> G
    G --> H
    H --> I
    I --> J
    J --> J1 & J2 & J3 & J4 & J5
    J1 --> K
    J2 --> K
    J3 --> K
    J4 --> K
    J5 --> K
    K --> K1 & K2
    K1 --> L
    K2 --> L
    L --> M
    
    style A fill:#c8e6c9
    style B fill:#fff9c4
    style C fill:#fff9c4
    style D fill:#fff9c4
    style E fill:#fff9c4
    style F fill:#fff9c4
    style G fill:#ffe0b2
    style H fill:#ffe0b2
    style I fill:#ffe0b2
    style J fill:#ffccbc
    style J1 fill:#ffccbc
    style J2 fill:#ffccbc
    style J3 fill:#ffccbc
    style J4 fill:#ffccbc
    style J5 fill:#ffccbc
    style K fill:#ffb74d
    style K1 fill:#ffb74d
    style K2 fill:#ffb74d
    style L fill:#b3e5fc
    style M fill:#b3e5fc
```

## Feature Engineering Process

```mermaid
graph TD
    A["Raw Features<br/>16 columns"]
    -->|Extract| B["Numerical Features"]
    A -->|Extract| C["Categorical Features"]
    
    B -->|List| B1["Year, Mileage, Engine CC,<br/>Power, Seats"]
    C -->|List| C1["Brand, Model,<br/>Transmission, Fuel Type,<br/>Owner Type, New/Used"]
    
    B1 -->|Validation| B2["Range Check"]
    B2 -->|Year| B2A["1980-2023"]
    B2 -->|Mileage| B2B["0-500000"]
    B2 -->|Engine CC| B2C["500-5000"]
    B2 -->|Power| B2D["20-500 bhp"]
    B2 -->|Seats| B2E["2-10"]
    
    C1 -->|Validation| C2["Category Check"]
    C2 -->|Brand| C2A["48 categories"]
    C2 -->|Model| C2B["126 categories"]
    C2 -->|Transmission| C2C["4 types"]
    C2 -->|Fuel Type| C2D["4 types"]
    C2 -->|Owner Type| C2E["3 types"]
    
    B1 -->|Transform| B3["Keep As-Is<br/>Numerical stable"]
    C1 -->|Transform| C3["Encode to Int<br/>0-N per category"]
    
    B3 -->|Combine| D["Feature Vector<br/>11 features total"]
    C3 -->|Combine| D
    
    D -->|Remove| E["Drop Target (Price)<br/>Keep only features"]
    E -->|Output| F["X: Feature Matrix<br/>n_samples × 11"]
    
    A -->|Extract| G["Target Variable"]
    G -->|Price| G1["Continuous Value<br/>₹ 50,000 - ₹ 5,000,000"]
    G1 -->|Output| H["y: Target Vector<br/>n_samples × 1"]
    
    style A fill:#c8e6c9
    style B fill:#fff9c4
    style C fill:#fff9c4
    style B1 fill:#fff9c4
    style C1 fill:#fff9c4
    style B2 fill:#ffe0b2
    style B2A fill:#ffe0b2
    style B2B fill:#ffe0b2
    style B2C fill:#ffe0b2
    style B2D fill:#ffe0b2
    style B2E fill:#ffe0b2
    style C2 fill:#ffe0b2
    style C2A fill:#ffe0b2
    style C2B fill:#ffe0b2
    style C2C fill:#ffe0b2
    style C2D fill:#ffe0b2
    style C2E fill:#ffe0b2
    style B3 fill:#ffccbc
    style C3 fill:#ffccbc
    style D fill:#ffb74d
    style E fill:#ffb74d
    style F fill:#b3e5fc
    style G fill:#fff9c4
    style G1 fill:#fff9c4
    style H fill:#b3e5fc
```

## Train-Test Split Strategy

```mermaid
graph TD
    A["Cleaned Data<br/>n=480 samples"]
    
    subgraph "Random Shuffling"
        B["Shuffle samples<br/>random_state=42"]
        B1["Ensures reproducibility"]
    end
    
    subgraph "Train-Test Split"
        C["test_size=0.2"]
        D["Train: 80%<br/>384 samples"]
        E["Test: 20%<br/>96 samples"]
    end
    
    subgraph "Stratification"
        F["Optional: Stratify<br/>by price range"]
        F1["Low: <₹30L"]
        F2["Medium: ₹30L-₹60L"]
        F3["High: >₹60L"]
    end
    
    subgraph "Training Data"
        G["X_train<br/>384 × 11"]
        H["y_train<br/>384 × 1"]
    end
    
    subgraph "Testing Data"
        I["X_test<br/>96 × 11"]
        J["y_test<br/>96 × 1"]
    end
    
    A --> B
    B --> B1
    B1 --> C
    C --> D & E
    D --> G & H
    E --> I & J
    D -.->|Optional| F
    F --> F1 & F2 & F3
    
    style A fill:#c8e6c9
    style B fill:#fff9c4
    style B1 fill:#fff9c4
    style C fill:#fff9c4
    style D fill:#ffe0b2
    style E fill:#ffe0b2
    style F fill:#ffccbc
    style F1 fill:#ffccbc
    style F2 fill:#ffccbc
    style F3 fill:#ffccbc
    style G fill:#b3e5fc
    style H fill:#b3e5fc
    style I fill:#ffb74d
    style J fill:#ffb74d
```

## Feature Scaling Pipeline

```mermaid
graph LR
    A["Unscaled Features"]
    
    subgraph "Unscaled"
        A1["Year: 1980-2023<br/>Range: 43"]
        A2["Mileage: 0-500K<br/>Range: 500K"]
        A3["Power: 20-500<br/>Range: 480"]
    end
    
    subgraph "StandardScaler"
        B["Formula:<br/>X_scaled = X - μ / σ"]
        B1["Calculate μ<br/>on train data"]
        B2["Calculate σ<br/>on train data"]
    end
    
    subgraph "Scaled"
        C["Year: -2.1 to 1.8<br/>μ=0, σ=1"]
        C1["Mileage: -0.8 to 2.3<br/>μ=0, σ=1"]
        C2["Power: -1.5 to 1.9<br/>μ=0, σ=1"]
    end
    
    A --> A1 & A2 & A3
    A1 --> B
    A2 --> B
    A3 --> B
    B --> B1 & B2
    B1 --> C
    B2 --> C1
    C & C1 & C2 --> D["Scaled Features<br/>Ready for ML"]
    
    style A fill:#c8e6c9
    style A1 fill:#c8e6c9
    style A2 fill:#c8e6c9
    style A3 fill:#c8e6c9
    style B fill:#fff9c4
    style B1 fill:#fff9c4
    style B2 fill:#fff9c4
    style C fill:#b3e5fc
    style C1 fill:#b3e5fc
    style C2 fill:#b3e5fc
    style D fill:#a5d6a7
```

## Data Storage and Retrieval

```mermaid
graph TD
    subgraph "Data Storage"
        A["artifacts/data_ingestion/<br/>car_price_prediction.csv"]
        B["artifacts/prepare_base_model/<br/>base_model/"]
    end
    
    subgraph "During Training"
        C["Processed Data<br/>in Memory"]
        D["Encoders<br/>in Memory"]
        E["Scaler<br/>in Memory"]
    end
    
    subgraph "After Training"
        F["artifacts/training/<br/>model.pkl"]
        G["artifacts/training/<br/>scaler.pkl"]
        H["artifacts/training/<br/>encoders.pkl"]
    end
    
    subgraph "Runtime (Prediction)"
        I["Load model.pkl"]
        J["Load scaler.pkl"]
        K["Load encoders.pkl"]
        L["Apply Transformations"]
    end
    
    A -->|Read| C
    B -->|Reference| C
    C -->|Save| F
    D -->|Save| H
    E -->|Save| G
    
    F -->|Load| I
    G -->|Load| J
    H -->|Load| K
    
    I -->|Use| L
    J -->|Use| L
    K -->|Use| L
    
    L -->|Predict| M["Price Output"]
    
    style A fill:#c8e6c9
    style B fill:#c8e6c9
    style C fill:#fff9c4
    style D fill:#fff9c4
    style E fill:#fff9c4
    style F fill:#ffe0b2
    style G fill:#ffe0b2
    style H fill:#ffe0b2
    style I fill:#ffccbc
    style J fill:#ffccbc
    style K fill:#ffccbc
    style L fill:#ffb74d
    style M fill:#a5d6a7
```

## Prediction Request Data Flow

```mermaid
graph TD
    A["Client Request<br/>16 Features"]
    -->|HTTP POST| B["Flask API<br/>/predict/price"]
    
    B -->|Validate| C["Pydantic Schema<br/>PredictionRequest"]
    C -->|Check Types| C1["String, Int, Float"]
    C -->|Check Ranges| C2["Valid ranges<br/>for all fields"]
    C -->|Check Required| C3["16 fields<br/>required"]
    
    C -->|Valid| D["Extract Features"]
    D -->|Build Array| E["Feature Array<br/>16 × 1"]
    
    E -->|Encode Categorical| F["Apply LabelEncoders<br/>from encoders.pkl"]
    F -->|Encode| F1["Brand → int"]
    F -->|Encode| F2["Model → int"]
    F -->|Encode| F3["Transmission → int"]
    
    E -->|Scale Numerical| G["Apply StandardScaler<br/>from scaler.pkl"]
    G -->|Scale| G1["Year, Mileage,<br/>Engine CC, Power"]
    
    F1 -->|Combine| H["Preprocessed Vector<br/>11 × 1"]
    F2 -->|Combine| H
    F3 -->|Combine| H
    G1 -->|Combine| H
    
    H -->|Load Model| I["model.pkl<br/>Best trained model"]
    I -->|Predict| J["model.predict()"]
    
    J -->|Output| K["Price Prediction<br/>Float value"]
    K -->|Format| L["JSON Response<br/>{'price': value}"]
    
    L -->|HTTP 200| M["Return to Client"]
    
    C -->|Invalid| N["Validation Error"]
    N -->|HTTP 422| O["Error Response<br/>Validation details"]
    
    style A fill:#c8e6c9
    style B fill:#fff9c4
    style C fill:#ffe0b2
    style C1 fill:#ffe0b2
    style C2 fill:#ffe0b2
    style C3 fill:#ffe0b2
    style D fill:#ffccbc
    style E fill:#ffccbc
    style F fill:#ffccbc
    style F1 fill:#ffccbc
    style F2 fill:#ffccbc
    style F3 fill:#ffccbc
    style G fill:#ffccbc
    style G1 fill:#ffccbc
    style H fill:#ffb74d
    style I fill:#b3e5fc
    style J fill:#b3e5fc
    style K fill:#d1c4e9
    style L fill:#d1c4e9
    style M fill:#a5d6a7
    style N fill:#ef5350
    style O fill:#ef5350
```

---

## Data Flow Summary

- **Raw Data → Preprocessing** (8 steps of cleaning and transformation)
- **Features → Scaling** (StandardScaler with μ=0, σ=1)
- **Train/Test Split** (80:20 ratio with reproducibility)
- **Model Training** (4 algorithms compared)
- **Artifacts Storage** (model, scaler, encoders saved)
- **Runtime Prediction** (exact same transformations applied)


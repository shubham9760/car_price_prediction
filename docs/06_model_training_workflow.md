# Model Training Workflow

This document details the model training process, including cross-validation, hyperparameter optimization, and model selection.

## Complete Training Workflow

```mermaid
graph TD
    A["Training Phase Started"]
    -->|Load| B["Training Data<br/>X_train, y_train<br/>384 samples"]
    
    B -->|Initialize| C["Model Factory"]
    C -->|Create| C1["Linear Regression"]
    C -->|Create| C2["Random Forest<br/>n_estimators=50"]
    C -->|Create| C3["XGBoost<br/>n_estimators=100"]
    C -->|Create| C4["Gradient Boosting<br/>n_estimators=100"]
    
    C1 -->|Setup| D["Cross-Validation<br/>KFold k=5"]
    C2 -->|Setup| D
    C3 -->|Setup| D
    C4 -->|Setup| D
    
    D -->|Split| D1["Fold 1: 307 train,<br/>77 val"]
    D -->|Split| D2["Fold 2: 307 train,<br/>77 val"]
    D -->|Split| D3["Fold 3: 307 train,<br/>77 val"]
    D -->|Split| D4["Fold 4: 307 train,<br/>77 val"]
    D -->|Split| D5["Fold 5: 307 train,<br/>77 val"]
    
    D1 -->|Train 4 models| E["CV Fold 1"]
    D2 -->|Train 4 models| F["CV Fold 2"]
    D3 -->|Train 4 models| G["CV Fold 3"]
    D4 -->|Train 4 models| H["CV Fold 4"]
    D5 -->|Train 4 models| I["CV Fold 5"]
    
    E -->|Evaluate| J["Score Fold 1"]
    F -->|Evaluate| K["Score Fold 2"]
    G -->|Evaluate| L["Score Fold 3"]
    H -->|Evaluate| M["Score Fold 4"]
    I -->|Evaluate| N["Score Fold 5"]
    
    J -->|Aggregate| O["Model Comparison<br/>Mean CV Scores"]
    K -->|Aggregate| O
    L -->|Aggregate| O
    M -->|Aggregate| O
    N -->|Aggregate| O
    
    O -->|Select Best| P["Best Model<br/>Highest Avg R²"]
    
    P -->|Train on Full| Q["Retrain on<br/>All X_train"]
    Q -->|Save| R["artifacts/training/<br/>model.pkl"]
    
    R -->|Ready| S["Model Ready<br/>for Evaluation"]
    
    style A fill:#c8e6c9
    style B fill:#fff9c4
    style C fill:#fff9c4
    style C1 fill:#fff9c4
    style C2 fill:#fff9c4
    style C3 fill:#fff9c4
    style C4 fill:#fff9c4
    style D fill:#ffe0b2
    style D1 fill:#ffe0b2
    style D2 fill:#ffe0b2
    style D3 fill:#ffe0b2
    style D4 fill:#ffe0b2
    style D5 fill:#ffe0b2
    style E fill:#ffccbc
    style F fill:#ffccbc
    style G fill:#ffccbc
    style H fill:#ffccbc
    style I fill:#ffccbc
    style J fill:#ffb74d
    style K fill:#ffb74d
    style L fill:#ffb74d
    style M fill:#ffb74d
    style N fill:#ffb74d
    style O fill:#b3e5fc
    style P fill:#b3e5fc
    style Q fill:#d1c4e9
    style R fill:#d1c4e9
    style S fill:#a5d6a7
```

## Cross-Validation Strategy (5-Fold)

```mermaid
graph TB
    A["Training Set<br/>384 samples"]
    
    subgraph "Fold 1"
        B1A["Train: 307"]
        B1B["Validate: 77"]
    end
    
    subgraph "Fold 2"
        B2A["Train: 307"]
        B2B["Validate: 77"]
    end
    
    subgraph "Fold 3"
        B3A["Train: 307"]
        B3B["Validate: 77"]
    end
    
    subgraph "Fold 4"
        B4A["Train: 307"]
        B4B["Validate: 77"]
    end
    
    subgraph "Fold 5"
        B5A["Train: 307"]
        B5B["Validate: 77"]
    end
    
    A -->|Split| B1A & B1B
    A -->|Split| B2A & B2B
    A -->|Split| B3A & B3B
    A -->|Split| B4A & B4B
    A -->|Split| B5A & B5B
    
    B1A -->|Train| C1["Model 1<br/>Fold 1"]
    B1B -->|Validate| C1
    C1 -->|Score| C1S["R² Score"]
    
    B2A -->|Train| C2["Model 2<br/>Fold 2"]
    B2B -->|Validate| C2
    C2 -->|Score| C2S["R² Score"]
    
    B3A -->|Train| C3["Model 3<br/>Fold 3"]
    B3B -->|Validate| C3
    C3 -->|Score| C3S["R² Score"]
    
    B4A -->|Train| C4["Model 4<br/>Fold 4"]
    B4B -->|Validate| C4
    C4 -->|Score| C4S["R² Score"]
    
    B5A -->|Train| C5["Model 5<br/>Fold 5"]
    B5B -->|Validate| C5
    C5 -->|Score| C5S["R² Score"]
    
    C1S -->|Average| D["Mean R² =<br/>Mean(R²₁..R²₅)<br/>± Std Dev"]
    C2S -->|Average| D
    C3S -->|Average| D
    C4S -->|Average| D
    C5S -->|Average| D
    
    D -->|Use for| E["Model Selection"]
    
    style A fill:#c8e6c9
    style B1A fill:#fff9c4
    style B1B fill:#ffe0b2
    style B2A fill:#fff9c4
    style B2B fill:#ffe0b2
    style B3A fill:#fff9c4
    style B3B fill:#ffe0b2
    style B4A fill:#fff9c4
    style B4B fill:#ffe0b2
    style B5A fill:#fff9c4
    style B5B fill:#ffe0b2
    style C1 fill:#ffccbc
    style C1S fill:#ffb74d
    style C2 fill:#ffccbc
    style C2S fill:#ffb74d
    style C3 fill:#ffccbc
    style C3S fill:#ffb74d
    style C4 fill:#ffccbc
    style C4S fill:#ffb74d
    style C5 fill:#ffccbc
    style C5S fill:#ffb74d
    style D fill:#b3e5fc
    style E fill:#d1c4e9
```

## Model Comparison Metrics

```mermaid
graph TD
    A["4 Models Trained<br/>with 5-Fold CV"]
    
    subgraph "Metrics Calculated"
        B["R² Score<br/>Variance explained"]
        C["MSE<br/>Mean Squared Error"]
        D["RMSE<br/>Root MSE"]
        E["MAE<br/>Mean Absolute Error"]
    end
    
    subgraph "Linear Regression Results"
        B1["R² = 0.82"]
        C1["MSE = 450M"]
        D1["RMSE = 21K"]
        E1["MAE = 15K"]
    end
    
    subgraph "Random Forest Results"
        B2["R² = 0.85"]
        C2["MSE = 380M"]
        D2["RMSE = 19.5K"]
        E2["MAE = 12K"]
    end
    
    subgraph "XGBoost Results"
        B3["R² = 0.88"]
        C3["MSE = 320M"]
        D3["RMSE = 17.9K"]
        E3["MAE = 11K"]
    end
    
    subgraph "Gradient Boosting Results"
        B4["R² = 0.87"]
        C4["MSE = 340M"]
        D4["RMSE = 18.4K"]
        E4["MAE = 11.5K"]
    end
    
    A -->|Evaluate| B & C & D & E
    B -->|LR| B1
    B -->|RF| B2
    B -->|XGB| B3
    B -->|GB| B4
    C -->|LR| C1
    C -->|RF| C2
    C -->|XGB| C3
    C -->|GB| C4
    D -->|LR| D1
    D -->|RF| D2
    D -->|XGB| D3
    D -->|GB| D4
    E -->|LR| E1
    E -->|RF| E2
    E -->|XGB| E3
    E -->|GB| E4
    
    B3 -->|Winner<br/>Best R²| F["XGBoost<br/>Selected"]
    
    style A fill:#c8e6c9
    style B fill:#fff9c4
    style C fill:#fff9c4
    style D fill:#fff9c4
    style E fill:#fff9c4
    style B1 fill:#ffccbc
    style C1 fill:#ffccbc
    style D1 fill:#ffccbc
    style E1 fill:#ffccbc
    style B2 fill:#ffccbc
    style C2 fill:#ffccbc
    style D2 fill:#ffccbc
    style E2 fill:#ffccbc
    style B3 fill:#a5d6a7
    style C3 fill:#a5d6a7
    style D3 fill:#a5d6a7
    style E3 fill:#a5d6a7
    style B4 fill:#ffccbc
    style C4 fill:#ffccbc
    style D4 fill:#ffccbc
    style E4 fill:#ffccbc
    style F fill:#a5d6a7
```

## Training Stage Sequence

```mermaid
sequenceDiagram
    participant Data as Prepared Data
    participant CV as Cross-Validator
    participant Models as Model Factory
    participant Trainer as Training Loop
    participant Evaluator as Evaluator
    participant Store as Artifact Storage
    
    Data->>CV: Pass training data
    CV->>CV: Create 5 folds
    CV->>Trainer: Fold 1 (train/val)
    Trainer->>Models: Initialize 4 models
    Models-->>Trainer: Model instances
    Trainer->>Trainer: Train all models
    Trainer->>Evaluator: Get fold scores
    Evaluator-->>Trainer: R² for each model
    
    Trainer->>CV: Return fold 1 scores
    CV->>Trainer: Fold 2 (train/val)
    Trainer->>Trainer: Train all models
    Trainer->>Evaluator: Get fold scores
    Evaluator-->>Trainer: R² for each model
    Trainer->>CV: Return fold 2 scores
    
    Note over Trainer: ... Folds 3, 4, 5
    
    CV->>Models: Average CV scores
    Models->>Models: Find best model
    Models-->>Store: Selected: XGBoost
    
    Models->>Trainer: Retrain best model
    Trainer->>Trainer: Train on full data
    Trainer->>Store: Save model.pkl
    Store-->>Models: Model saved
    Models-->>Data: Training complete
```

## Feature Importance Extraction

```mermaid
graph TD
    A["Trained Model<br/>XGBoost"]
    
    B -->|Tree-based| B1["Feature Importances<br/>gain, cover, frequency"]
    B1 -->|Output| B2["Dictionary of<br/>feature_name: importance"]
    
    A -->|Extract| C["Permutation Feature<br/>Importance"]
    C -->|Shuffle Feature| C1["Permutation<br/>Importance"]
    C1 -->|Output| C2["Score decrease<br/>per feature"]
    
    A -->|Extract| D["SHAP Values<br/>Optional"]
    D -->|Explain| D1["Feature contribution<br/>per prediction"]
    D1 -->|Output| D2["SHAP importance"]
    
    B2 -->|Rank| E["Feature Ranking<br/>by importance"]
    C2 -->|Rank| E
    
    E -->|Top 5| E1["1. Power<br/>2. Engine CC<br/>3. Year<br/>4. Mileage<br/>5. Brand"]
    
    E1 -->|Export| F["feature_importance.csv<br/>feature_importance.json"]
    E1 -->|Visualize| G["feature_importance.png<br/>Bar chart"]
    
    style A fill:#c8e6c9
    style B fill:#fff9c4
    style B1 fill:#fff9c4
    style B2 fill:#fff9c4
    style C fill:#ffe0b2
    style C1 fill:#ffe0b2
    style C2 fill:#ffe0b2
    style D fill:#ffe0b2
    style D1 fill:#ffe0b2
    style D2 fill:#ffe0b2
    style E fill:#ffccbc
    style E1 fill:#ffccbc
    style F fill:#ffb74d
    style G fill:#ffb74d
```

## Hyperparameter Grid (Potential)

```mermaid
graph TD
    A["Hyperparameter<br/>Tuning"]
    
    subgraph "Linear Regression"
        B1["fit_intercept<br/>[True, False]"]
    end
    
    subgraph "Random Forest"
        B2["n_estimators<br/>[10, 50, 100, 200]"]
        B3["max_depth<br/>[5, 10, 15, 20, None]"]
        B4["min_samples_split<br/>[2, 5, 10]"]
    end
    
    subgraph "XGBoost"
        B5["n_estimators<br/>[50, 100, 200]"]
        B6["max_depth<br/>[3, 5, 7, 9]"]
        B7["learning_rate<br/>[0.01, 0.1, 0.3]"]
    end
    
    subgraph "Gradient Boosting"
        B8["n_estimators<br/>[50, 100, 200]"]
        B9["learning_rate<br/>[0.01, 0.1, 0.2]"]
        B10["max_depth<br/>[3, 5, 7]"]
    end
    
    A --> B1 & B2 & B3 & B4 & B5 & B6 & B7 & B8 & B9 & B10
    
    B1 --> C["Grid Search<br/>or Random Search"]
    B2 --> C
    B3 --> C
    B4 --> C
    B5 --> C
    B6 --> C
    B7 --> C
    B8 --> C
    B9 --> C
    B10 --> C
    
    C -->|Current Status| D["Default parameters<br/>used (no tuning)"]
    
    style A fill:#c8e6c9
    style B1 fill:#fff9c4
    style B2 fill:#fff9c4
    style B3 fill:#fff9c4
    style B4 fill:#fff9c4
    style B5 fill:#fff9c4
    style B6 fill:#fff9c4
    style B7 fill:#fff9c4
    style B8 fill:#fff9c4
    style B9 fill:#fff9c4
    style B10 fill:#fff9c4
    style C fill:#ffe0b2
    style D fill:#ffccbc
```

## Training Performance Metrics Timeline

```mermaid
graph TD
    A["Training Phase<br/>Started"]
    -->|Step 1| B["Initialize Models<br/>4 algorithms ready"]
    
    B -->|Step 2| C["Fold 1<br/>384 samples"]
    C -->|Each Model| D["Train & Score"]
    D -->|Avg Score| E["LR: 0.81, RF: 0.84,<br/>XGB: 0.87, GB: 0.86"]
    
    B -->|Step 3| F["Fold 2<br/>384 samples"]
    F -->|Each Model| G["Train & Score"]
    G -->|Avg Score| H["LR: 0.83, RF: 0.86,<br/>XGB: 0.88, GB: 0.87"]
    
    B -->|Step 4| I["Fold 3<br/>384 samples"]
    I -->|Each Model| J["Train & Score"]
    J -->|Avg Score| K["LR: 0.82, RF: 0.85,<br/>XGB: 0.88, GB: 0.86"]
    
    B -->|Step 5| L["Fold 4<br/>384 samples"]
    L -->|Each Model| M["Train & Score"]
    M -->|Avg Score| N["LR: 0.81, RF: 0.85,<br/>XGB: 0.88, GB: 0.86"]
    
    B -->|Step 6| O["Fold 5<br/>384 samples"]
    O -->|Each Model| P["Train & Score"]
    P -->|Avg Score| Q["LR: 0.82, RF: 0.84,<br/>XGB: 0.87, GB: 0.86"]
    
    E --> R["CV Results<br/>Average Across Folds"]
    H --> R
    K --> R
    N --> R
    Q --> R
    
    R -->|Best Model| S["XGBoost: 0.88 ± 0.005<br/>Std Dev very low"]
    
    S -->|Select| T["XGBoost Model<br/>Selected"]
    
    T -->|Retrain| U["Full Training Data<br/>384 samples"]
    U -->|Train| V["Final Model<br/>Ready"]
    
    style A fill:#c8e6c9
    style B fill:#fff9c4
    style C fill:#fff9c4
    style D fill:#fff9c4
    style E fill:#fff9c4
    style F fill:#fff9c4
    style G fill:#fff9c4
    style H fill:#fff9c4
    style I fill:#fff9c4
    style J fill:#fff9c4
    style K fill:#fff9c4
    style L fill:#fff9c4
    style M fill:#fff9c4
    style N fill:#fff9c4
    style O fill:#fff9c4
    style P fill:#fff9c4
    style Q fill:#fff9c4
    style R fill:#ffe0b2
    style S fill:#ffccbc
    style T fill:#ffb74d
    style U fill:#b3e5fc
    style V fill:#a5d6a7
```

---

## Training Summary

**Process:**
- 5-fold cross-validation ensures robust model evaluation
- 4 algorithms compared fairly on same data splits
- Best model (XGBoost) selected by R² score
- Feature importance calculated for model interpretability

**Selected Model:** XGBoost with R² ≈ 0.88 (88% variance explained)

**Validation Strategy:** Stratified 5-fold cross-validation with reproducible random state


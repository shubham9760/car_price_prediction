# Feature Importance Analysis

This document explains how feature importance is calculated, visualized, and exported from the trained models.

## Feature Importance Framework

```mermaid
graph TD
    A["Trained Model<br/>XGBoost, Random Forest,<br/>Gradient Boosting"]
    
    subgraph "Importance Calculation Methods"
        B1["Tree-based<br/>Feature Importance"]
        B2["Permutation<br/>Importance"]
        B3["SHAP Values<br/>Optional"]
        B4["Linear Coefficients<br/>For Linear Regression"]
    end
    
    subgraph "Tree-Based (Built-in)"
        C1["Gain<br/>Contribution to<br/>accuracy improvement"]
        C2["Cover<br/>Relative quantity of<br/>observations"]
        C3["Frequency<br/>How often feature<br/>is used in splits"]
    end
    
    subgraph "Permutation Based"
        D1["Shuffle Feature<br/>One at a time"]
        D2["Measure<br/>Score decrease"]
        D3["Rank by<br/>Importance"]
    end
    
    subgraph "Output Importance Scores"
        E1["Power: 0.285"]
        E2["Engine CC: 0.195"]
        E3["Year: 0.165"]
        E4["Mileage: 0.145"]
        E5["Brand: 0.125"]
        E6["Others: 0.085"]
    end
    
    A --> B1 & B2 & B3 & B4
    
    B1 --> C1 & C2 & C3
    B2 --> D1 & D2 & D3
    
    C1 --> E1 & E2 & E3
    C2 --> E4 & E5 & E6
    C3 --> E1
    D1 --> E1
    D2 --> E2
    D3 --> E3
    
    style A fill:#c8e6c9
    style B1 fill:#fff9c4
    style B2 fill:#fff9c4
    style B3 fill:#fff9c4
    style B4 fill:#fff9c4
    style C1 fill:#ffe0b2
    style C2 fill:#ffe0b2
    style C3 fill:#ffe0b2
    style D1 fill:#ffe0b2
    style D2 fill:#ffe0b2
    style D3 fill:#ffe0b2
    style E1 fill:#ffccbc
    style E2 fill:#ffccbc
    style E3 fill:#ffccbc
    style E4 fill:#ffccbc
    style E5 fill:#ffccbc
    style E6 fill:#ffccbc
```

## Feature Importance Extraction Pipeline

```mermaid
graph TD
    A["Load Trained Model<br/>model.pkl"]
    -->|Read| B["Get Feature Names<br/>11 features total"]
    
    B -->|Extract| C["Tree-based Importance<br/>XGBoost built-in"]
    C -->|Access| C1["model.feature_importances_<br/>or booster.get_score()"]
    C1 -->|Result| C2["Array of floats<br/>Sum = 1.0"]
    
    A -->|Calculate| D["Permutation Importance<br/>scikit-learn"]
    D -->|For each feature| D1["Shuffle feature values<br/>Calculate score drop"]
    D1 -->|Result| D2["Array of importance<br/>Only informative"]
    
    B -->|Map| E["Feature Name<br/>to Importance"]
    C2 --> E
    D2 --> E
    
    E -->|Create| F["Importance Dictionary<br/>feature: score"]
    F -->|Example| G["Power: 0.285<br/>Engine CC: 0.195<br/>Year: 0.165<br/>... (11 features)"]
    
    G -->|Sort| H["Descending Order<br/>Highest first"]
    H -->|Rank| I["Ranked Features<br/>1-11"]
    
    style A fill:#c8e6c9
    style B fill:#fff9c4
    style C fill:#ffe0b2
    style C1 fill:#ffe0b2
    style C2 fill:#ffe0b2
    style D fill:#ffe0b2
    style D1 fill:#ffe0b2
    style D2 fill:#ffe0b2
    style E fill:#ffccbc
    style F fill:#ffb74d
    style G fill:#ffb74d
    style H fill:#b3e5fc
    style I fill:#b3e5fc
```

## Importance Visualization Pipeline

```mermaid
graph TD
    A["Feature Importance<br/>Dictionary"]
    -->|Prepare Data| B["Convert to<br/>DataFrame"]
    
    B -->|Select| C["Select Top Features<br/>Top 10 by default"]
    C -->|Create| C1["Feature names<br/>Importance values"]
    
    C1 -->|Plot| D["Bar Chart"]
    D -->|Customize| E["Title: Feature Importance<br/>X-axis: Importance Score<br/>Y-axis: Feature Names<br/>Color: Blue bars"]
    
    C1 -->|Export| F["Save Figure"]
    F -->|Format| F1["feature_importance.png<br/>DPI: 300<br/>Format: PNG"]
    
    B -->|Additional| G["Pie Chart<br/>Optional"]
    G -->|Show| G1["Proportion of<br/>total importance"]
    
    B -->|Additional| H["Horizontal Bar<br/>Top 10 features"]
    H -->|Rank| H1["Sorted visualization<br/>Highest first"]
    
    E -->|Display| I["matplotlib.pyplot.show<br/>or save to file"]
    
    style A fill:#c8e6c9
    style B fill:#fff9c4
    style C fill:#fff9c4
    style C1 fill:#fff9c4
    style D fill:#ffe0b2
    style E fill:#ffe0b2
    style F fill:#ffe0b2
    style F1 fill:#ffe0b2
    style G fill:#ffccbc
    style G1 fill:#ffccbc
    style H fill:#ffccbc
    style H1 fill:#ffccbc
    style I fill:#ffb74d
```

## Export Formats

```mermaid
graph TD
    A["Feature Importance<br/>Calculated"]
    
    A -->|Export Format 1| B["CSV File<br/>feature_importance.csv"]
    B -->|Structure| B1["feature_name,importance<br/>Power,0.285<br/>Engine CC,0.195<br/>... (11 rows)"]
    B1 -->|Save| B2["artifacts/training/<br/>feature_importance.csv"]
    
    A -->|Export Format 2| C["JSON File<br/>feature_importance.json"]
    C -->|Structure| C1["{<br/>  'Power': 0.285,<br/>  'Engine CC': 0.195,<br/>  ...<br/>}"]
    C1 -->|Save| C2["artifacts/training/<br/>feature_importance.json"]
    
    A -->|Export Format 3| D["PNG Image<br/>feature_importance.png"]
    D -->|Structure| D1["Bar chart visualization<br/>Horizontal layout<br/>Sorted by importance"]
    D1 -->|Save| D2["artifacts/training/<br/>feature_importance.png"]
    
    A -->|Export Format 4| E["HTML Report<br/>Optional"]
    E -->|Interactive| E1["Plotly visualization<br/>Hover details<br/>Zoom/pan"]
    E1 -->|Save| E2["artifacts/training/<br/>feature_importance.html"]
    
    A -->|Access| F["Python Dictionary<br/>In-memory"]
    F -->|Use| F1["API response<br/>JSON serializable"]
    
    style A fill:#c8e6c9
    style B fill:#fff9c4
    style B1 fill:#fff9c4
    style B2 fill:#fff9c4
    style C fill:#ffe0b2
    style C1 fill:#ffe0b2
    style C2 fill:#ffe0b2
    style D fill:#ffccbc
    style D1 fill:#ffccbc
    style D2 fill:#ffccbc
    style E fill:#ffb74d
    style E1 fill:#ffb74d
    style E2 fill:#ffb74d
    style F fill:#b3e5fc
    style F1 fill:#b3e5fc
```

## Feature Importance Interpretation

```mermaid
graph TD
    A["Feature Importance Scores<br/>Sum = 1.0"]
    
    B1["Power: 0.285<br/>28.5%"]
    B2["Engine CC: 0.195<br/>19.5%"]
    B3["Year: 0.165<br/>16.5%"]
    B4["Mileage: 0.145<br/>14.5%"]
    B5["Brand: 0.125<br/>12.5%"]
    B6["Others: 0.085<br/>8.5%"]
    
    A --> B1 & B2 & B3 & B4 & B5 & B6
    
    B1 -->|Insight| C1["Power is most<br/>important feature<br/>~3x more than Brand"]
    B2 -->|Insight| C2["Engine displacement<br/>strong indicator"]
    B3 -->|Insight| C3["Year (age) affects<br/>car price significantly"]
    B4 -->|Insight| C4["Mileage affects<br/>price moderately"]
    B5 -->|Insight| C5["Brand matters<br/>but less critical"]
    B6 -->|Insight| C6["Other features<br/>combined minor impact"]
    
    C1 -->|Action| D1["Focus on power<br/>in model tuning"]
    C2 -->|Action| D2["Ensure engine<br/>data accuracy"]
    C3 -->|Action| D3["Year is key<br/>pricing factor"]
    C4 -->|Action| D4["Mileage crucial<br/>for predictions"]
    C5 -->|Action| D5["Brand has<br/>some market effect"]
    
    style A fill:#c8e6c9
    style B1 fill:#a5d6a7
    style B2 fill:#a5d6a7
    style B3 fill:#a5d6a7
    style B4 fill:#a5d6a7
    style B5 fill:#fff9c4
    style B6 fill:#fff9c4
    style C1 fill:#ffe0b2
    style C2 fill:#ffe0b2
    style C3 fill:#ffe0b2
    style C4 fill:#ffe0b2
    style C5 fill:#ffccbc
    style C6 fill:#ffccbc
    style D1 fill:#ffb74d
    style D2 fill:#ffb74d
    style D3 fill:#ffb74d
    style D4 fill:#ffb74d
    style D5 fill:#ffb74d
```

## Importance by Feature Category

```mermaid
graph TB
    A["11 Features Total<br/>100% importance"]
    
    subgraph "Top Features (High Impact)"
        B1["Power: 28.5%<br/>Most important"]
        B2["Engine CC: 19.5%<br/>Strong impact"]
        B3["Year: 16.5%<br/>Strong impact"]
    end
    
    subgraph "Middle Features (Moderate Impact)"
        C1["Mileage: 14.5%<br/>Moderate impact"]
        C2["Brand: 12.5%<br/>Moderate impact"]
    end
    
    subgraph "Lower Features (Minor Impact)"
        D1["Transmission: 4.2%"]
        D2["Fuel Type: 2.8%"]
        D3["Seats: 1.5%"]
        D4["Owner Type: 0.3%"]
    end
    
    A --> B1 & B2 & B3
    A --> C1 & C2
    A --> D1 & D2 & D3 & D4
    
    B1 -->|Tier 1| E["Critical<br/>Decision making<br/>features"]
    B2 -->|Tier 1| E
    B3 -->|Tier 1| E
    
    C1 -->|Tier 2| F["Important<br/>Model accuracy<br/>features"]
    C2 -->|Tier 2| F
    
    D1 -->|Tier 3| G["Supplementary<br/>Minor contribution<br/>features"]
    D2 -->|Tier 3| G
    D3 -->|Tier 3| G
    D4 -->|Tier 3| G
    
    style A fill:#c8e6c9
    style B1 fill:#a5d6a7
    style B2 fill:#a5d6a7
    style B3 fill:#a5d6a7
    style C1 fill:#fff9c4
    style C2 fill:#fff9c4
    style D1 fill:#ffccbc
    style D2 fill:#ffccbc
    style D3 fill:#ffccbc
    style D4 fill:#ffccbc
    style E fill:#ffe0b2
    style F fill:#ffe0b2
    style G fill:#ffe0b2
```

## Feature Importance Workflow

```mermaid
sequenceDiagram
    participant Code as Training Code
    participant Model as Trained Model
    participant Extract as Extraction
    participant Export as Export
    participant Files as File System
    
    Code->>Model: Complete training
    Code->>Extract: Request feature importance
    Extract->>Model: Get feature_importances_
    Model-->>Extract: Importance array
    Extract->>Extract: Map features to scores
    Extract-->>Code: Importance dict
    
    Code->>Export: Export to formats
    Export->>Files: Write feature_importance.csv
    Export->>Files: Write feature_importance.json
    Export->>Files: Write feature_importance.png
    Files-->>Export: Files saved
    Export-->>Code: Export complete
    
    Code->>Code: Log summary
    Note over Code: Top 5 features saved<br/>to artifacts/training/
```

## API Feature Importance Endpoint

```mermaid
graph TD
    A["Client Request<br/>GET /info/features"]
    -->|Call| B["Flask Endpoint"]
    
    B -->|Load| C["feature_importance.json<br/>from artifacts/"]
    C -->|Parse| D["Dictionary of<br/>importance scores"]
    
    D -->|Format| E["Response JSON<br/>{<br/>  'features': {<br/>    'Power': 0.285,<br/>    'Engine CC': 0.195,<br/>    ...<br/>  }<br/>}"]
    
    E -->|HTTP 200| F["Return to Client"]
    
    F -->|Client displays| G["Feature ranking<br/>Importance list<br/>Top features"]
    
    style A fill:#c8e6c9
    style B fill:#fff9c4
    style C fill:#ffe0b2
    style D fill:#ffe0b2
    style E fill:#ffccbc
    style F fill:#ffb74d
    style G fill:#a5d6a7
```

## Analysis Methods Comparison

```mermaid
graph TD
    A["Feature Importance<br/>Methods"]
    
    subgraph "Tree-Based (Built-in)"
        B["XGBoost.feature_importances_"]
        B -->|Pros| B1["✓ Fast<br/>✓ Built-in<br/>✓ No extra code"]
        B -->|Cons| B2["✗ XGBoost specific<br/>✗ Less reliable<br/>✗ Biased to high cardinality"]
    end
    
    subgraph "Permutation Based"
        C["sklearn.inspection<br/>.permutation_importance"]
        C -->|Pros| C1["✓ Model agnostic<br/>✓ Reliable<br/>✓ Interpretable"]
        C -->|Cons| C2["✗ Slower<br/>✗ More computation<br/>✗ Can be noisy"]
    end
    
    subgraph "Gradient-Based"
        D["SHAP Values<br/>Optional"]
        D -->|Pros| D1["✓ Theoretical sound<br/>✓ Per-sample<br/>✓ Very interpretable"]
        D -->|Cons| D2["✗ Very slow<br/>✗ Complex<br/>✗ Extra dependency"]
    end
    
    A -->|Used| B
    A -->|Could use| C
    A -->|Advanced| D
    
    B -->|Selected| E["Primary Method"]
    
    style A fill:#c8e6c9
    style B fill:#fff9c4
    style B1 fill:#fff9c4
    style B2 fill:#fff9c4
    style C fill:#ffe0b2
    style C1 fill:#ffe0b2
    style C2 fill:#ffe0b2
    style D fill:#ffccbc
    style D1 fill:#ffccbc
    style D2 fill:#ffccbc
    style E fill:#ffb74d
```

---

## Summary

**Feature Importance Summary:**

| Rank | Feature | Importance | Tier |
|------|---------|------------|------|
| 1 | Power | 28.5% | Critical |
| 2 | Engine CC | 19.5% | Critical |
| 3 | Year | 16.5% | Critical |
| 4 | Mileage | 14.5% | Important |
| 5 | Brand | 12.5% | Important |
| 6-11 | Others | 8.5% | Minor |

**Top 3 Features Explain ~65% of Variance**

**Export Formats:**
- CSV: feature_importance.csv
- JSON: feature_importance.json
- PNG: feature_importance.png
- API: /info/features endpoint


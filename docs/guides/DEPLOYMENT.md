# Car Price Prediction - Complete ML Project

A comprehensive machine learning project for predicting car prices using advanced regression models with a production-ready Flask REST API.

## Features

### Core ML Features
- **Multiple Models**: Linear Regression, Random Forest, XGBoost, Gradient Boosting
- **Cross-Validation**: K-fold cross-validation for robust model evaluation
- **Feature Importance Analysis**: Understand which features drive predictions
- **Model Comparison**: Automated comparison of all models with detailed metrics
- **Feature Scaling**: StandardScaler for optimal model performance

### Production Features
- **Flask REST API**: Full REST API with Swagger documentation
- **Data Validation**: Pydantic schemas for input validation
- **Model Versioning**: Track all model versions and metrics
- **MLflow Integration**: Experiment tracking and model registry
- **Docker Deployment**: Multi-stage Docker build for production
- **Logging**: Comprehensive logging throughout the pipeline
- **Health Checks**: Built-in health monitoring

## Project Structure

```
car_price_prediction/
├── src/car_price_prediction/
│   ├── components/
│   │   ├── data_ingestion.py           # Download and extract data
│   │   ├── prepare_base_model.py       # Create base model
│   │   ├── training.py                 # Train models
│   │   ├── evaluation.py               # Evaluate performance
│   │   ├── prepare_callbacks.py        # Model callbacks
│   │   ├── model_comparison.py         # Compare multiple models
│   │   └── feature_importance.py       # Feature importance analysis
│   ├── config/
│   │   ├── configuration.py            # Configuration management
│   ├── entity/
│   │   └── config_entity.py            # Config data classes
│   ├── pipeline/
│   │   ├── stage_01_data_ingestion.py
│   │   ├── stage_02_prepare_base_model.py
│   │   ├── stage_03_training.py
│   │   ├── stage_03_advanced_training.py
│   │   ├── stage_04_evaluation.py
│   │   └── stage_05_predict.py
│   ├── schemas/
│   │   └── prediction_schema.py        # Pydantic validation schemas
│   ├── utils/
│   │   └── common.py                   # Utility functions
│   └── model_tracking.py               # MLflow integration
├── app.py                              # Flask application
├── main.py                             # Main pipeline orchestrator
├── config/
│   └── config.yaml                     # Configuration file
├── params.yaml                         # Model parameters
├── Dockerfile                          # Docker container definition
├── docker-compose.yml                  # Multi-service composition
├── requirements.txt                    # Python dependencies
└── templates/
    └── index.html                      # Web UI template
```

## Installation

### Prerequisites
- Python 3.11+
- Docker & Docker Compose (for containerized deployment)
- Git

### Local Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd car_price_prediction
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the pipeline**
   ```bash
   python main.py
   ```

## Usage

### Running the ML Pipeline

```bash
# Execute complete pipeline
python main.py

# Or run individual stages
python src/car_price_prediction/pipeline/stage_01_data_ingestion.py
python src/car_price_prediction/pipeline/stage_02_prepare_base_model.py
python src/car_price_prediction/pipeline/stage_03_training.py
python src/car_price_prediction/pipeline/stage_04_evaluation.py
```

### Running the Flask API Locally

```bash
# Start Flask development server
python app.py

# API will be available at http://localhost:5000
# Swagger documentation at http://localhost:5000/api/docs
```

### Docker Deployment

#### Option 1: Using Docker Compose (Recommended)

```bash
# Start all services (API + MLflow)
docker-compose up -d

# Check status
docker-compose ps

# View logs
docker-compose logs -f api

# Stop services
docker-compose down
```

#### Option 2: Using Docker Only

```bash
# Build the image
docker build -t car-price-prediction:latest .

# Run the container
docker run -d \
  --name car-price-api \
  -p 5000:5000 \
  -v $(pwd)/artifacts:/app/artifacts \
  -v $(pwd)/logs:/app/logs \
  car-price-prediction:latest

# Check logs
docker logs -f car-price-api
```

## API Endpoints

### Prediction
- **POST** `/predict/price` - Predict price for a single car
  ```json
  {
    "Levy": 1000,
    "Manufacturer": "Toyota",
    "Model": "Camry",
    "Prod. year": 2020,
    "Category": "Sedan",
    "Leather interior": 1,
    "Fuel type": "Petrol",
    "Engine volume": 2.5,
    "Mileage": 50000,
    "Cylinders": 4,
    "Gear box type": "Automatic",
    "Drive wheels": "Front",
    "Doors": 4,
    "Wheel": "18",
    "Color": "Black",
    "Airbags": 8
  }
  ```

- **POST** `/predict/batch` - Predict prices for multiple cars
  ```json
  [
    { /* car 1 features */ },
    { /* car 2 features */ }
  ]
  ```

### Information
- **GET** `/info/status` - Model and API status
- **GET** `/info/features` - List of features used by model

### Web Interface
- **GET** `/` - Web UI for predictions

## Configuration

### config/config.yaml
```yaml
data_ingestion:
  source_URL: "https://github.com/datasets/Car_Price_Prediction/archive/refs/heads/master.zip"
  local_data_file: "artifacts/data_ingestion/data.zip"
  unzip_path: "artifacts/data_ingestion"

prepare_base_model:
  root_dir: "artifacts/prepare_base_model"
  base_model_name: "base_model.pkl"
  updated_base_model_name: "base_model_updated.pkl"
  base_model_path: "artifacts/prepare_base_model/base_model.pkl"
  updated_base_model_path: "artifacts/prepare_base_model/base_model_updated.pkl"
  test_data_path: "artifacts/data_ingestion/car_price_prediction.csv"

training:
  root_dir: "artifacts/training"
  trained_model_path: "artifacts/training/model.pkl"

evaluation:
  root_dir: "artifacts"
  path_of_model: "artifacts/training/model.pkl"
  path_of_scaler: "artifacts/training/scaler.pkl"
  metric_file_name: "artifacts/scores.json"
```

### params.yaml
```yaml
model:
  linear_regression:
    feature_columns:
      - "Levy"
      - "Manufacturer"
      - "Model"
      - ... (16 total features)
    target_column: "Price"

EPOCHS: 25
BATCH_SIZE: 16
LEARNING_RATE: 0.001
TEST_SIZE: 0.2
RANDOM_STATE: 42
```

## Model Performance

After training, the pipeline generates evaluation metrics:

- **R² Score**: Model's coefficient of determination
- **RMSE**: Root Mean Squared Error (in currency units)
- **MAE**: Mean Absolute Error (in currency units)
- **MSE**: Mean Squared Error

View results in `artifacts/scores.json`

## Advanced Features

### Model Comparison
The advanced training pipeline automatically compares:
- Linear Regression
- Random Forest Regressor
- XGBoost Regressor
- Gradient Boosting Regressor

Results saved to `artifacts/model_comparison/model_comparison.json`

### Feature Importance
Analyze which features drive price predictions:
- View importance scores in `artifacts/feature_importance/feature_importance.csv`
- Visualizations in `artifacts/feature_importance/feature_importance_plot.png`

### Model Versioning
Track all model versions:
- View history in `artifacts/model_versions/versions.json`
- Promote versions to production/staging/archived status

### MLflow Integration
Monitor experiments in MLflow UI:
```bash
# MLflow is available at http://localhost:5001 when using docker-compose
```

## Data Validation

The API uses Pydantic for strict data validation:
- Type checking
- Range validation
- Required fields enforcement
- Automatic error messages

Invalid requests return detailed validation errors.

## Logging

Comprehensive logging is implemented:
- Console output
- File logging to `logs/running_logs.log`
- Different log levels (DEBUG, INFO, WARNING, ERROR)

## Development

### Adding New Models
1. Update `src/car_price_prediction/components/model_comparison.py`
2. Add model to `ModelFactory._initialize_models()`
3. Re-run training pipeline

### Custom Predictions
```python
from car_price_prediction.config.configuration import ConfigurationManager
import joblib

# Load model and scaler
model = joblib.load('artifacts/training/model.pkl')
scaler = joblib.load('artifacts/training/scaler.pkl')

# Prepare features
features = [[1000, 1, 2, 2020, 3, 1, 1, 2.5, 50000, 4, 1, 1, 4, 1, 1, 8]]

# Predict
prediction = model.predict(scaler.transform(features))
```

## Troubleshooting

### MLflow Connection Error
If MLflow is not available, the app continues with local versioning only.

### Docker Port Conflicts
Change ports in `docker-compose.yml`:
```yaml
ports:
  - "5000:5000"  # Change 5000 to your port
```

### Out of Memory
For large datasets, adjust batch size in `params.yaml`

## Dependencies

Key packages:
- **pandas, numpy**: Data manipulation
- **scikit-learn**: ML models and preprocessing
- **xgboost**: Gradient boosting
- **Flask, Flask-RESTX**: REST API
- **pydantic**: Data validation
- **mlflow**: Experiment tracking
- **matplotlib**: Visualization
- **joblib**: Model serialization

See `requirements.txt` for complete list.

## Performance Optimization

- Feature scaling improves convergence
- Cross-validation prevents overfitting
- Model comparison finds the best algorithm
- Batch predictions for throughput
- Docker deployment for scalability

## Security Considerations

- Non-root user in Docker container
- Input validation on all endpoints
- Error messages don't expose sensitive data
- Health checks for availability monitoring

## Future Enhancements

- [ ] PostgreSQL database backend
- [ ] Kubernetes deployment
- [ ] Model A/B testing
- [ ] Real-time prediction monitoring
- [ ] Auto-retraining pipeline
- [ ] Web UI improvements

## License

See LICENSE file for details.

## Support

For issues or questions, please check:
1. `logs/running_logs.log` for error details
2. MLflow UI for experiment tracking
3. API Swagger documentation at `/api/docs`

## Contributors

Car Price Prediction Team

---

**Last Updated**: 2024
**Version**: 2.0 (Advanced ML with Production API)

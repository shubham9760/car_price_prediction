# Car Price Prediction API - Usage Guide

## Quick Start

### 1. Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Run the Flask API
python app.py

# API will be available at: http://localhost:5000
# Swagger UI at: http://localhost:5000/api/docs
```

### 2. Docker Deployment

```bash
# Using docker-compose (recommended)
docker-compose up -d

# API at: http://localhost:5000
# MLflow at: http://localhost:5001
```

---

## API Endpoints

### 1. Single Price Prediction

**Endpoint:** `POST /predict/price`

**Request:**
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

**Response:**
```json
{
  "price": 15234.50,
  "confidence": 0.85,
  "features_received": 16
}
```

**cURL Example:**
```bash
curl -X POST http://localhost:5000/predict/price \
  -H "Content-Type: application/json" \
  -d '{
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
  }'
```

**Python Example:**
```python
import requests

url = "http://localhost:5000/predict/price"

car_data = {
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

response = requests.post(url, json=car_data)
result = response.json()

print(f"Predicted Price: ${result['price']:.2f}")
print(f"Confidence: {result['confidence']:.2%}")
```

---

### 2. Batch Price Prediction

**Endpoint:** `POST /predict/batch`

**Request:**
```json
[
  {
    "Levy": 1000,
    "Manufacturer": "Toyota",
    "Model": "Camry",
    ...
  },
  {
    "Levy": 1500,
    "Manufacturer": "Honda",
    "Model": "Civic",
    ...
  }
]
```

**Response:**
```json
{
  "predictions": [
    {"price": 15234.50},
    {"price": 13456.75}
  ]
}
```

**Python Example:**
```python
import requests
import pandas as pd

cars = [
    {
        "Levy": 1000,
        "Manufacturer": "Toyota",
        ...
    },
    {
        "Levy": 1500,
        "Manufacturer": "Honda",
        ...
    }
]

response = requests.post("http://localhost:5000/predict/batch", json=cars)
results = response.json()

# Convert to DataFrame
prices = [r['price'] for r in results['predictions']]
predictions_df = pd.DataFrame({'predicted_price': prices})
```

---

### 3. Get API Status

**Endpoint:** `GET /info/status`

**Response:**
```json
{
  "model_loaded": true,
  "scaler_loaded": true,
  "model_path": "artifacts/training/model.pkl",
  "scaler_path": "artifacts/training/scaler.pkl",
  "timestamp": "2024-01-15T10:30:00"
}
```

**cURL Example:**
```bash
curl http://localhost:5000/info/status
```

---

### 4. Get Required Features

**Endpoint:** `GET /info/features`

**Response:**
```json
{
  "features": [
    "Levy",
    "Manufacturer",
    "Model",
    "Prod. year",
    "Category",
    "Leather interior",
    "Fuel type",
    "Engine volume",
    "Mileage",
    "Cylinders",
    "Gear box type",
    "Drive wheels",
    "Doors",
    "Wheel",
    "Color",
    "Airbags"
  ],
  "count": 16
}
```

**cURL Example:**
```bash
curl http://localhost:5000/info/features
```

---

### 5. Web Interface

**Access:** `http://localhost:5000/`

Interactive form for:
- Single car price prediction
- Real-time validation
- Visual result display
- API documentation reference

---

## Data Validation

### Required Fields

All fields are required for prediction:

| Field | Type | Constraints |
|-------|------|-------------|
| Levy | float | > 0 |
| Manufacturer | string | Non-empty |
| Model | string | Non-empty |
| Prod. year | integer | 1900 - 2030 |
| Category | string | Non-empty |
| Leather interior | integer | 0 or 1 |
| Fuel type | string | Non-empty |
| Engine volume | float | > 0 |
| Mileage | float | >= 0, <= 5,000,000 |
| Cylinders | integer | > 0 |
| Gear box type | string | Non-empty |
| Drive wheels | string | Non-empty |
| Doors | integer | 2-5 |
| Wheel | string | Non-empty |
| Color | string | Non-empty |
| Airbags | integer | 0-16 |

### Validation Errors

If validation fails, the API returns:
```json
{
  "error": "Validation failed",
  "details": [
    {
      "field": "Prod. year",
      "message": "ensure this value is less than 2030"
    }
  ]
}
```

---

## Error Handling

### Common Errors

**400 - Bad Request:**
```json
{
  "error": "Validation failed: Invalid data format"
}
```

**404 - Not Found:**
```json
{
  "error": "Resource not found"
}
```

**500 - Server Error:**
```json
{
  "error": "Internal server error"
}
```

### Error Handling in Code

```python
import requests

try:
    response = requests.post(
        "http://localhost:5000/predict/price",
        json=car_data,
        timeout=10
    )
    response.raise_for_status()
    result = response.json()
    print(f"Predicted Price: ${result['price']:.2f}")
except requests.exceptions.HTTPError as e:
    if e.response.status_code == 400:
        print("Validation Error:", e.response.json())
    elif e.response.status_code == 500:
        print("Server Error")
except requests.exceptions.RequestException as e:
    print(f"Connection Error: {e}")
```

---

## Advanced Usage

### Model Performance Metrics

After training, access metrics:
```bash
# View evaluation metrics
cat artifacts/scores.json

# View model comparison
cat artifacts/model_comparison/model_comparison.json

# View feature importance
cat artifacts/feature_importance/feature_importance.csv
```

### MLflow Tracking

```bash
# Start MLflow UI (when using docker-compose)
# Navigate to http://localhost:5001

# Or start locally
mlflow server --host 0.0.0.0 --port 5001
```

### Feature Importance

Access feature importance analysis:
```python
import pandas as pd

# Load importance scores
importance = pd.read_csv('artifacts/feature_importance/feature_importance.csv')
print(importance.head(10))

# Plot the image
from PIL import Image
img = Image.open('artifacts/feature_importance/feature_importance_plot.png')
img.show()
```

### Model Versioning

```python
import json

# Load version history
with open('artifacts/model_versions/versions.json') as f:
    versions = json.load(f)

# Latest version
latest = versions[-1]
print(f"Version {latest['version']}: R² = {latest['metrics']['r2']:.4f}")
```

---

## Performance Optimization

### Batch Processing

For multiple predictions, use batch endpoint:

```python
# Process 1000 cars
import requests

cars = [...]  # List of 1000 car dictionaries

# Batch in groups of 100
batch_size = 100
all_predictions = []

for i in range(0, len(cars), batch_size):
    batch = cars[i:i+batch_size]
    response = requests.post("http://localhost:5000/predict/batch", json=batch)
    predictions = response.json()['predictions']
    all_predictions.extend(predictions)

print(f"Total predictions: {len(all_predictions)}")
```

### Caching

```python
import functools
import requests

@functools.lru_cache(maxsize=1000)
def cached_prediction(levy, manufacturer, model):
    # Only cache immutable string version
    response = requests.get(f"http://localhost:5000/predict?levy={levy}&manufacturer={manufacturer}")
    return response.json()['price']
```

---

## Deployment to Production

### Using Gunicorn

```bash
pip install gunicorn

# Run with multiple workers
gunicorn --workers 4 --bind 0.0.0.0:5000 app:app
```

### Environment Variables

```bash
export FLASK_ENV=production
export FLASK_DEBUG=0
python app.py
```

### Docker Production

```bash
# Build production image
docker build -t car-price-api:latest .

# Run with resource limits
docker run -d \
  --name car-price-api \
  --memory=2g \
  --cpus=2 \
  -p 5000:5000 \
  -v $(pwd)/artifacts:/app/artifacts \
  car-price-api:latest
```

---

## Monitoring and Logging

### View Logs

```bash
# Local
tail -f logs/running_logs.log

# Docker
docker logs -f car-price-prediction-api
```

### Health Checks

```bash
# Manual health check
curl http://localhost:5000/info/status

# In health monitoring system
curl --fail http://localhost:5000/info/status || exit 1
```

---

## Troubleshooting

### Port Already in Use

```bash
# Find and kill process on port 5000
lsof -i :5000
kill -9 <PID>
```

### Model Not Loaded

```bash
# Check if artifacts exist
ls -la artifacts/training/

# Retrain model
python main.py
```

### Docker Issues

```bash
# Rebuild image
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

---

## API Rate Limiting (Optional)

For production deployments, consider adding rate limiting:

```python
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)

@app.route('/predict/price', methods=['POST'])
@limiter.limit("10 per minute")
def predict_price():
    ...
```

---

## Support

- **API Documentation:** http://localhost:5000/api/docs (Swagger)
- **Status Page:** http://localhost:5000/info/status
- **Feature List:** http://localhost:5000/info/features
- **Web UI:** http://localhost:5000/

For issues, check `logs/running_logs.log` or Docker logs.

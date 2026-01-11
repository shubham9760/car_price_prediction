# 🚀 Quick Start Guide - Car Price Prediction ML API

## 60-Second Setup

### Option 1: Docker (Recommended)

```bash
# 1. Build and run all services
docker-compose up -d

# 2. Wait for startup (30 seconds)
sleep 30

# 3. Access the API
curl http://localhost:5000/info/status
```

✅ **Done!** Your API is running:
- **Web UI:** http://localhost:5000
- **API Docs:** http://localhost:5000/api/docs
- **MLflow:** http://localhost:5001

---

### Option 2: Local Python

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Train the model
python main.py

# 3. Start the API
python app.py
```

✅ **Done!** API running at http://localhost:5000

---

## Predict Car Prices

### Web Interface
Open http://localhost:5000 in your browser and fill in the form.

### Python Script
```python
import requests

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

response = requests.post("http://localhost:5000/predict/price", json=car_data)
result = response.json()

print(f"Predicted Price: ${result['price']:.2f}")
print(f"Confidence: {result['confidence']:.0%}")
```

### cURL
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

---

## Available Endpoints

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/` | GET | Web interface |
| `/predict/price` | POST | Predict single car price |
| `/predict/batch` | POST | Predict multiple cars |
| `/info/status` | GET | API status |
| `/info/features` | GET | Required features |
| `/api/docs` | GET | Swagger documentation |

---

## Key Features

✨ **ML Models:**
- Linear Regression
- Random Forest
- XGBoost
- Gradient Boosting

📊 **Analysis:**
- Model comparison
- Feature importance
- Cross-validation (5-fold)
- Performance metrics

🛡️ **Production Ready:**
- Input validation
- Error handling
- Logging
- Docker deployment
- MLflow tracking

---

## Directory Structure

```
artifacts/
├── data_ingestion/          # Dataset
├── training/                # Trained models
├── model_comparison/        # Model comparison results
├── feature_importance/      # Feature analysis
└── model_versions/          # Version history

logs/
└── running_logs.log        # Application logs
```

---

## Troubleshooting

### Port 5000 Already in Use?
```bash
# Kill the process using port 5000
lsof -i :5000 | grep LISTEN | awk '{print $2}' | xargs kill -9
```

### Model Not Found?
```bash
# Retrain the model
python main.py
```

### Docker Issues?
```bash
# Rebuild and restart
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

### Check Logs
```bash
# Local
tail -f logs/running_logs.log

# Docker
docker-compose logs -f api
```

---

## What's New (8 Advanced Features)

1. **🌐 Flask REST API** - Production-grade API with CORS
2. **🤖 Advanced Models** - RandomForest + XGBoost comparison
3. **✅ Data Validation** - Pydantic schemas for all inputs
4. **📈 Cross-Validation** - 5-fold CV for robust evaluation
5. **📊 Feature Importance** - Analyze which features matter
6. **🐳 Docker Support** - Multi-stage Docker build + compose
7. **📖 Swagger Docs** - Interactive API documentation
8. **📦 Model Versioning** - MLflow integration + local tracking

---

## Performance Metrics

After training, check results:

```bash
# Model metrics
cat artifacts/scores.json

# Model comparison
cat artifacts/model_comparison/model_comparison.json

# Feature importance
cat artifacts/feature_importance/feature_importance.csv

# Version history
cat artifacts/model_versions/versions.json
```

---

## Next Steps

1. ✅ Start the API: `docker-compose up -d`
2. ✅ Open http://localhost:5000 in browser
3. ✅ Fill prediction form
4. ✅ View results
5. ✅ Explore API docs at `/api/docs`

---

## Support

- **Web UI:** http://localhost:5000
- **API Docs:** http://localhost:5000/api/docs
- **Status:** http://localhost:5000/info/status
- **Logs:** `logs/running_logs.log` or `docker-compose logs -f`

---

## Additional Resources

- [Full API Documentation](API_USAGE.md)
- [Deployment Guide](DEPLOYMENT.md)
- [Features Overview](FEATURES_IMPLEMENTED.md)
- [Configuration](config/config.yaml)

---

**Ready to predict car prices? Let's go! 🚗💨**

```bash
docker-compose up -d && echo "API ready at http://localhost:5000"
```

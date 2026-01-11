import os
import joblib
import pandas as pd
import numpy as np
from pathlib import Path
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from flask_restx import Api, Resource, fields, Namespace
from car_price_prediction import logger
from car_price_prediction.config.configuration import ConfigurationManager
from sklearn.preprocessing import LabelEncoder

# Initialize Flask app
app = Flask(__name__, template_folder='templates')
CORS(app)

# Setup Swagger API documentation
api = Api(app, version='1.0', title='Car Price Prediction API',
          description='A comprehensive API for predicting car prices',
          doc='/api/docs')

# Create namespaces
predict_ns = api.namespace('predict', description='Prediction operations')
info_ns = api.namespace('info', description='Information operations')

# Load configuration
config = ConfigurationManager()
prepare_base_model_config = config.get_prepare_base_model_config()

# Global variables for model and scaler
model = None
scaler = None
label_encoders = {}
feature_columns = prepare_base_model_config.feature_columns


def load_model_and_scaler():
    """Load the trained model and scaler"""
    global model, scaler
    try:
        model_path = Path("artifacts/training/model.pkl")
        scaler_path = Path("artifacts/training/scaler.pkl")
        
        if model_path.exists():
            model = joblib.load(model_path)
            logger.info("Model loaded successfully")
        else:
            logger.error(f"Model not found at {model_path}")
            
        if scaler_path.exists():
            scaler = joblib.load(scaler_path)
            logger.info("Scaler loaded successfully")
        else:
            logger.warning("Scaler not found")
    except Exception as e:
        logger.exception(f"Error loading model: {e}")


def preprocess_input(data):
    """Preprocess input data"""
    try:
        df = pd.DataFrame([data])
        
        # Handle categorical columns
        for col in df.columns:
            if df[col].dtype == 'object':
                le = LabelEncoder()
                df[col] = le.fit_transform(df[col].astype(str))
                label_encoders[col] = le
        
        # Ensure all columns are numeric
        df = df.astype(float)
        
        return df
    except Exception as e:
        logger.error(f"Error preprocessing input: {e}")
        return None


# Define Swagger models
price_model = api.model('Price', {
    'price': fields.Float(description='Predicted price'),
    'confidence': fields.Float(description='Confidence score')
})

car_features = api.model('CarFeatures', {
    'Levy': fields.Float(required=True, description='Levy'),
    'Manufacturer': fields.String(required=True, description='Car manufacturer'),
    'Model': fields.String(required=True, description='Car model'),
    'Prod. year': fields.Integer(required=True, description='Production year'),
    'Category': fields.String(required=True, description='Car category'),
    'Leather interior': fields.Integer(required=True, description='Leather interior (0/1)'),
    'Fuel type': fields.String(required=True, description='Fuel type'),
    'Engine volume': fields.Float(required=True, description='Engine volume'),
    'Mileage': fields.Float(required=True, description='Mileage'),
    'Cylinders': fields.Integer(required=True, description='Number of cylinders'),
    'Gear box type': fields.String(required=True, description='Gearbox type'),
    'Drive wheels': fields.String(required=True, description='Drive wheels'),
    'Doors': fields.Integer(required=True, description='Number of doors'),
    'Wheel': fields.String(required=True, description='Wheel type'),
    'Color': fields.String(required=True, description='Car color'),
    'Airbags': fields.Integer(required=True, description='Number of airbags')
})


@app.before_request
def initialize():
    """Initialize model and scaler on first request"""
    global model, scaler
    if model is None or scaler is None:
        load_model_and_scaler()


@app.route('/')
def index():
    """Serve the main web interface"""
    return render_template('index.html')


@predict_ns.route('/price')
class PredictPrice(Resource):
    """Predict car price from features"""
    
    @predict_ns.expect(car_features)
    @predict_ns.marshal_with(price_model)
    def post(self):
        """Predict price for given car features"""
        try:
            data = api.payload
            
            # Validate input
            if not data:
                api.abort(400, 'No input data provided')
            
            # Preprocess input
            processed_data = preprocess_input(data)
            if processed_data is None:
                api.abort(400, 'Error processing input data')
            
            # Select only required features
            X = processed_data[feature_columns]
            
            # Scale features
            if scaler:
                X_scaled = scaler.transform(X)
            else:
                X_scaled = X
            
            # Make prediction
            if model:
                price = model.predict(X_scaled)[0]
                confidence = 0.85  # Placeholder confidence
                
                logger.info(f"Prediction made: ${price:.2f}")
                
                return {
                    'price': float(price),
                    'confidence': confidence
                }, 200
            else:
                api.abort(503, 'Model not loaded')
                
        except Exception as e:
            logger.exception(f"Error during prediction: {e}")
            api.abort(500, f'Internal server error: {str(e)}')


@predict_ns.route('/batch')
class PredictBatch(Resource):
    """Predict prices for multiple cars"""
    
    def post(self):
        """Predict prices for batch of cars"""
        try:
            data = api.payload
            
            if not isinstance(data, list):
                api.abort(400, 'Expected list of car features')
            
            predictions = []
            for item in data:
                processed = preprocess_input(item)
                if processed is not None:
                    X = processed[feature_columns]
                    if scaler:
                        X_scaled = scaler.transform(X)
                    else:
                        X_scaled = X
                    
                    if model:
                        price = float(model.predict(X_scaled)[0])
                        predictions.append({'price': price})
            
            return {'predictions': predictions}, 200
            
        except Exception as e:
            logger.exception(f"Error during batch prediction: {e}")
            api.abort(500, f'Internal server error: {str(e)}')


@info_ns.route('/features')
class FeatureInfo(Resource):
    """Get information about model features"""
    
    def get(self):
        """Get list of features used by model"""
        return {
            'features': feature_columns,
            'count': len(feature_columns)
        }, 200


@info_ns.route('/status')
class ModelStatus(Resource):
    """Get model status information"""
    
    def get(self):
        """Get current model status"""
        return {
            'model_loaded': model is not None,
            'scaler_loaded': scaler is not None,
            'model_path': 'artifacts/training/model.pkl',
            'scaler_path': 'artifacts/training/scaler.pkl',
            'timestamp': str(pd.Timestamp.now())
        }, 200


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return {'error': 'Resource not found'}, 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    logger.error(f"Internal server error: {error}")
    return {'error': 'Internal server error'}, 500


if __name__ == '__main__':
    logger.info("Starting Car Price Prediction Flask Application")
    app.run(debug=True, host='0.0.0.0', port=5000)

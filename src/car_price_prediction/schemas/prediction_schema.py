from pydantic import BaseModel, Field, validator
from typing import Optional
from car_price_prediction import logger


class CarFeatures(BaseModel):
    """Pydantic model for car features validation"""
    
    Levy: float = Field(..., gt=0, description="Levy amount")
    Manufacturer: str = Field(..., min_length=1, description="Car manufacturer")
    Model: str = Field(..., min_length=1, description="Car model")
    Prod_year: int = Field(..., ge=1900, le=2030, alias="Prod. year", description="Production year")
    Category: str = Field(..., min_length=1, description="Car category")
    Leather_interior: int = Field(..., ge=0, le=1, alias="Leather interior", description="Has leather interior")
    Fuel_type: str = Field(..., min_length=1, alias="Fuel type", description="Fuel type")
    Engine_volume: float = Field(..., gt=0, description="Engine volume in liters")
    Mileage: float = Field(..., ge=0, description="Car mileage in km")
    Cylinders: int = Field(..., gt=0, description="Number of cylinders")
    Gear_box_type: str = Field(..., min_length=1, alias="Gear box type", description="Gearbox type")
    Drive_wheels: str = Field(..., min_length=1, alias="Drive wheels", description="Drive wheels type")
    Doors: int = Field(..., ge=2, le=5, description="Number of doors")
    Wheel: str = Field(..., min_length=1, description="Wheel type")
    Color: str = Field(..., min_length=1, description="Car color")
    Airbags: int = Field(..., ge=0, le=16, description="Number of airbags")
    
    class Config:
        populate_by_name = True
        str_strip_whitespace = True
    
    @validator('Manufacturer', 'Model', 'Category', 'Fuel_type', 
               'Gear_box_type', 'Drive_wheels', 'Wheel', 'Color')
    def validate_string_fields(cls, v):
        """Validate string fields"""
        if not v or not v.strip():
            raise ValueError('String fields cannot be empty')
        return v.strip()
    
    @validator('Prod_year')
    def validate_year(cls, v):
        """Validate production year"""
        import datetime
        current_year = datetime.datetime.now().year
        if v > current_year + 1:
            raise ValueError(f'Production year cannot be in the future')
        if v < 1886:  # First car was in 1886
            raise ValueError('Production year too old')
        return v
    
    @validator('Mileage')
    def validate_mileage(cls, v):
        """Validate mileage"""
        if v > 5000000:  # Sanity check - 5 million km
            raise ValueError('Mileage seems unrealistic')
        return v


class PredictionRequest(BaseModel):
    """Request model for prediction endpoint"""
    features: CarFeatures
    include_confidence: bool = Field(default=True, description="Include confidence score")


class PredictionResponse(BaseModel):
    """Response model for prediction"""
    price: float = Field(..., gt=0, description="Predicted price")
    confidence: float = Field(..., ge=0, le=1, description="Confidence score")
    features_received: int = Field(..., description="Number of features received")


class ValidationReport(BaseModel):
    """Report for data validation"""
    is_valid: bool
    errors: list = []
    warnings: list = []
    record_count: int = 0
    
    def add_error(self, field: str, message: str):
        """Add an error to the report"""
        self.errors.append(f"{field}: {message}")
        self.is_valid = False
    
    def add_warning(self, field: str, message: str):
        """Add a warning to the report"""
        self.warnings.append(f"{field}: {message}")
    
    def summary(self):
        """Get summary of validation"""
        return {
            'is_valid': self.is_valid,
            'error_count': len(self.errors),
            'warning_count': len(self.warnings),
            'record_count': self.record_count,
            'errors': self.errors[:5],  # First 5 errors
            'warnings': self.warnings[:5]  # First 5 warnings
        }


class DataValidator:
    """Data validation utility"""
    
    @staticmethod
    def validate_features(features_dict: dict) -> tuple[bool, list]:
        """Validate car features"""
        try:
            CarFeatures(**features_dict)
            logger.info("Features validation passed")
            return True, []
        except Exception as e:
            errors = []
            if hasattr(e, 'errors'):
                errors = [str(err) for err in e.errors()]
            else:
                errors = [str(e)]
            logger.warning(f"Features validation failed: {errors}")
            return False, errors
    
    @staticmethod
    def validate_dataframe(df):
        """Validate entire dataframe"""
        report = ValidationReport(record_count=len(df))
        
        try:
            # Check required columns
            required_cols = CarFeatures.__fields__.keys()
            missing_cols = set(required_cols) - set(df.columns)
            if missing_cols:
                report.add_error("columns", f"Missing columns: {missing_cols}")
            
            # Check for null values
            null_cols = df.columns[df.isnull().any()].tolist()
            if null_cols:
                report.add_warning("nulls", f"Null values in: {null_cols}")
            
            # Validate each row
            for idx, row in df.iterrows():
                try:
                    CarFeatures(**row.to_dict())
                except Exception as e:
                    if idx < 5:  # Report first 5 errors
                        report.add_error(f"row_{idx}", str(e)[:100])
            
            if len(report.errors) == 0:
                report.is_valid = True
                logger.info(f"Dataframe validation passed for {len(df)} records")
            
        except Exception as e:
            report.add_error("validation", str(e))
            logger.error(f"Error during dataframe validation: {e}")
        
        return report

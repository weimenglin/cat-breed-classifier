# Production Deployment Guide

## Package Contents
This directory contains the complete production deployment package:

```
phase4_production/
├── cat_breed_classifier_v1.0.model    # Trained WEKA model (22MB)
├── predict_cat_breed.py               # Python prediction interface  
├── weka.jar                          # WEKA toolkit (required)
├── README.md                         # User documentation
└── DEPLOYMENT_GUIDE.md              # This deployment guide
```

## Installation

### 1. System Prerequisites
- **Java**: Version 8 or higher
- **Python**: Version 3.6 or higher
- **Memory**: 2GB+ RAM recommended
- **Storage**: 50MB free space

### 2. Verification
```bash
# Verify Java installation
java -version

# Verify Python installation
python --version

# Test model interface
python predict_cat_breed.py --info
```

### 3. Expected Output
```
🤖 CAT BREED CLASSIFIER MODEL INFO
==================================================
Version: 1.0.0
Algorithm: Random Forest (300 trees)
Training Data: 2016 samples, 7 breeds
SNP Features: 93 biologically-encoded markers
Expected Accuracy: 90.58%
```

## Input Data Preparation

### ARFF Format Requirements
Input files must follow WEKA ARFF format:

```arff
@relation cat_breed_prediction

@attribute ISAGFC01 numeric
@attribute ISAGFC02 numeric
...
@attribute ISAGFC98 numeric

@data
0,1,2,-1,0,1,2,0,1,-1,...
-1,0,2,1,0,0,1,2,1,0,...
```

### Attribute Specifications
- **Required**: Exactly 93 numeric attributes
- **Names**: ISAGFC01, ISAGFC02, ISAGFC03, ISAGFC04, ISAGFC05, ISAGFC07-ISAGFC98
- **Excluded**: ISAGFC06, ISAGFC15, ISAGFC44, ISAGFC83, ISAGFC87 (quality control)
- **Values**: 0, 1, 2, -1 only (biological encoding)

### Data Validation
```bash
# Basic validation commands
head -20 your_sample.arff        # Check header format
grep "^@attribute" your_sample.arff | wc -l    # Should be 93
grep "^@data" -A 5 your_sample.arff             # Check data format
```

## Usage Examples

### Single Sample Prediction
```bash
# Predict breed for one sample
python predict_cat_breed.py sample1.arff

# Expected output:
🧬 CAT BREED CLASSIFICATION RESULTS
==================================================
Sample 1:
   🏆 Predicted Breed: Maine Coon
   📊 Confidence: 95.3%
   🎯 Confidence Level: 🟢 Very High
```

### Batch Processing
```bash
# Process multiple samples in one file
python predict_cat_breed.py batch_samples.arff

# Expected output for multiple samples:
Sample 1: Maine Coon (95.3%)
Sample 2: Bengal Cat (87.6%)  
Sample 3: Ragdoll (91.2%)
```

## Integration Options

### Command Line Integration
```bash
#!/bin/bash
RESULT=$(python predict_cat_breed.py "$1" 2>/dev/null)
if [ $? -eq 0 ]; then
    echo "Prediction successful: $RESULT"
else
    echo "Prediction failed"
fi
```

### Python API Integration
```python
import subprocess
import json

def predict_breed(arff_file):
    """Wrapper function for breed prediction"""
    try:
        result = subprocess.run(
            ['python', 'predict_cat_breed.py', arff_file],
            capture_output=True, text=True, timeout=30
        )
        if result.returncode == 0:
            return parse_prediction_output(result.stdout)
        else:
            return None
    except Exception as e:
        print(f"Prediction error: {e}")
        return None
```

## Performance Optimization

### Memory Tuning
For large batch processing, adjust Java heap size:
```bash
# Edit predict_cat_breed.py line 203:
# Change: "java", "-Xmx2048m", "-cp", self.weka_jar,
# To:     "java", "-Xmx4096m", "-cp", self.weka_jar,
```

### Batch Processing Tips
- **Small batches**: 10-50 samples per file for optimal performance
- **Large datasets**: Split into multiple files and process in parallel
- **Memory usage**: ~50MB per 100 samples

## Error Handling

### Common Issues and Solutions

1. **Java Heap Space Error**
   ```
   Solution: Increase heap size to -Xmx4096m or higher
   ```

2. **File Format Errors**
   ```
   Error: "Instances have different number of attributes"
   Solution: Verify exactly 93 numeric attributes present
   ```

3. **Missing Attributes**
   ```
   Error: "Attribute not found: ISAGFCXX"  
   Solution: Check attribute names match ISAG panel exactly
   ```

4. **Invalid Values**
   ```
   Error: "Invalid numeric value"
   Solution: Ensure only 0, 1, 2, -1 values used
   ```

## Monitoring and Validation

### Prediction Quality Checks
```bash
# Check prediction confidence distribution
python predict_cat_breed.py samples.arff | grep "Confidence:" | sort

# Monitor for low-confidence predictions
python predict_cat_breed.py samples.arff | grep "🔴 Low"
```

### Model Validation
- **Expected accuracy**: 90.58% on similar datasets
- **Confidence distribution**: 70%+ predictions should have >80% confidence
- **Breed balance**: All 7 breeds should be represented in large datasets

## Support and Troubleshooting

### Log Files
- Check WEKA error output in terminal
- Monitor system memory usage during large batches
- Verify Java classpath includes weka.jar

### Validation Dataset
Create test samples with known breeds to validate deployment:
```bash
# Test with known sample
python predict_cat_breed.py known_maine_coon.arff
# Expected: High confidence Maine Coon prediction
```

### Contact Information
For technical support or model updates, contact the development team with:
- Model version (1.0.0)
- Error messages and logs
- Sample data format examples
- System specifications

## Version History
- **v1.0.0** (Sept 2025): Initial production release
  - 90.58% accuracy on 7-breed classification
  - 300-tree Random Forest with biological encoding
  - Complete ARFF input/output pipeline
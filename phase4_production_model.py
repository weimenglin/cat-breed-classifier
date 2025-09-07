#!/usr/bin/env python3
"""
Phase 4: Create optimized production model and deployment pipeline
"""

from pathlib import Path
import subprocess

def create_production_model_script():
    """Create production-ready model training script"""
    
    script_content = '''#!/bin/bash
# Production Cat Breed Classification Model
# Optimized configuration based on Phase 3 breakthrough results

echo "=========================================="
echo "PRODUCTION MODEL TRAINING"
echo "=========================================="

WEKA_JAR="weka.jar"
MEMORY="-Xmx4096m"
INPUT_FILE="cat_breed_snp_v1_missing_neg1_purebred_fixed.arff"
OUTPUT_MODEL="cat_breed_classifier_production.model"

# Verify prerequisites
if [ ! -f "$WEKA_JAR" ]; then
    echo "ERROR: weka.jar not found"
    exit 1
fi

if [ ! -f "$INPUT_FILE" ]; then
    echo "ERROR: Input dataset not found: $INPUT_FILE"
    exit 1
fi

echo "Training production model with optimal configuration:"
echo "- Algorithm: Resampled Random Forest"
echo "- Trees: 500"
echo "- Features per split: sqrt(features) = default"
echo "- Class balancing: Resample filter (100% rate)"
echo "- Dataset: V1 numerical encoding (2,417 instances, 26 breeds)"
echo ""

# Train and save production model
java $MEMORY -cp "$WEKA_JAR" weka.classifiers.meta.FilteredClassifier \\
    -F "weka.filters.supervised.instance.Resample -B 1.0 -S 1 -Z 100.0" \\
    -W weka.classifiers.trees.RandomForest \\
    -t "$INPUT_FILE" \\
    -d "$OUTPUT_MODEL" \\
    -- -I 500 -K 0 -depth 0 -num-slots 4

if [ $? -eq 0 ]; then
    echo "✓ Production model saved to: $OUTPUT_MODEL"
    echo ""
    echo "Model specifications:"
    echo "- Expected accuracy: 89.24% (±2%)"
    echo "- Expected kappa: 0.8607 (almost perfect agreement)"
    echo "- Supports 26 purebred cat classifications"
    echo "- Input: V1 numerical SNP encoding"
    echo "- Missing value handling: -1 encoding"
    echo ""
    echo "Deployment ready! 🚀"
else
    echo "✗ Model training failed"
    exit 1
fi
'''
    
    script_path = "train_production_model.sh"
    with open(script_path, 'w') as f:
        f.write(script_content)
    
    # Make executable
    subprocess.run(['chmod', '+x', script_path], check=True)
    
    print(f"Created production training script: {script_path}")
    return script_path

def create_prediction_pipeline():
    """Create prediction pipeline for new samples"""
    
    pipeline_content = '''#!/usr/bin/env python3
"""
Production Prediction Pipeline for Cat Breed Classification
Usage: python predict_breed.py input_sample.arff
"""

import sys
import subprocess
from pathlib import Path

def predict_breed(input_file):
    """Predict breed for new sample using production model"""
    
    model_file = "cat_breed_classifier_production.model"
    weka_jar = "weka.jar"
    
    if not Path(model_file).exists():
        print(f"ERROR: Production model not found: {model_file}")
        print("Please train the production model first using train_production_model.sh")
        return False
    
    if not Path(input_file).exists():
        print(f"ERROR: Input file not found: {input_file}")
        return False
    
    print(f"Predicting breed for: {input_file}")
    print(f"Using model: {model_file}")
    print("")
    
    # Run prediction
    cmd = [
        "java", "-Xmx2048m", "-cp", weka_jar,
        "weka.classifiers.meta.FilteredClassifier",
        "-l", model_file,
        "-T", input_file,
        "-p", "0"
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        
        # Parse predictions
        predictions = []
        for line in result.stdout.split('\\n'):
            if line.strip() and not line.startswith('=') and not line.startswith('inst'):
                parts = line.strip().split()
                if len(parts) >= 3 and parts[0].isdigit():
                    actual = parts[1] if len(parts) > 1 else "unknown"
                    predicted = parts[2] if len(parts) > 2 else "unknown"
                    confidence = parts[3] if len(parts) > 3 else "0.0"
                    predictions.append((actual, predicted, confidence))
        
        # Display results
        print("PREDICTION RESULTS:")
        print("=" * 50)
        for i, (actual, predicted, confidence) in enumerate(predictions, 1):
            breed_name = predicted.split(':')[1] if ':' in predicted else predicted
            conf_val = float(confidence) if confidence.replace('.','').isdigit() else 0.0
            conf_pct = (1.0 - conf_val) * 100
            
            print(f"Sample {i}: {breed_name} (confidence: {conf_pct:.1f}%)")
        
        print("")
        print(f"Total samples processed: {len(predictions)}")
        
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"ERROR: Prediction failed")
        print(f"Command: {' '.join(cmd)}")
        print(f"Error: {e}")
        return False

def main():
    if len(sys.argv) != 2:
        print("Usage: python predict_breed.py input_sample.arff")
        print("")
        print("Input file should contain SNP data in ARFF format with V1 numerical encoding:")
        print("- Missing values: -1")
        print("- Allele values: 0, 1, 2")
        print("- Same 192 SNP loci as training data")
        sys.exit(1)
    
    input_file = sys.argv[1]
    success = predict_breed(input_file)
    
    if success:
        print("✓ Prediction completed successfully")
    else:
        print("✗ Prediction failed")
        sys.exit(1)

if __name__ == "__main__":
    main()
'''
    
    script_path = "predict_breed.py"
    with open(script_path, 'w') as f:
        f.write(pipeline_content)
    
    print(f"Created prediction pipeline: {script_path}")
    return script_path

def main():
    print("=" * 60)
    print("PHASE 4: PRODUCTION MODEL CREATION")
    print("=" * 60)
    
    # Create production model training script
    train_script = create_production_model_script()
    
    # Create prediction pipeline
    predict_script = create_prediction_pipeline()
    
    print("")
    print("Production deployment files created:")
    print(f"1. {train_script} - Train production model")
    print(f"2. {predict_script} - Predict breeds for new samples")
    
    print("")
    print("Deployment workflow:")
    print(f"1. Run: ./{train_script}")
    print(f"2. Use: python {predict_script} new_sample.arff")
    
    print("")
    print("Model specifications:")
    print("- Algorithm: Resampled Random Forest")
    print("- Expected accuracy: 89.24% (±2%)")
    print("- Supported breeds: 26 purebred categories")
    print("- Input format: V1 numerical SNP encoding")
    print("- Production ready for deployment")

if __name__ == "__main__":
    main()
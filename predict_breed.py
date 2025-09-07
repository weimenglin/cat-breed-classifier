#!/usr/bin/env python3
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
        for line in result.stdout.split('\n'):
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

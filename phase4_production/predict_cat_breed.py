#!/usr/bin/env python3
"""
Cat Breed Prediction Interface
Production model for cat breed classification using SNP data.

Usage:
    python predict_cat_breed.py input_sample.arff
    python predict_cat_breed.py --info
"""

import subprocess
import sys
import argparse
from pathlib import Path

class CatBreedPredictor:
    def __init__(self):
        self.model_file = "cat_breed_classifier_v1.0.model"
        self.weka_jar = "../weka.jar"
        
        # Breed mapping (production names)
        self.breed_mapping = {
            'Bengal': 'Bengal Cat',
            'British_Shorthair': 'British Shorthair',
            'Maine_Coon': 'Maine Coon',
            'Norwegian_Forest_Cat': 'Norwegian Forest Cat',
            'Ragdoll': 'Ragdoll',
            'Sphinx': 'Sphynx Cat',
            'Thai': 'Thai Cat'
        }
        
    def predict_sample(self, input_file):
        """Predict breed for SNP sample(s)"""
        
        if not Path(input_file).exists():
            print(f"❌ Input file not found: {input_file}")
            return None
        
        command = [
            "java", "-Xmx2048m", "-cp", self.weka_jar,
            "weka.classifiers.meta.FilteredClassifier",
            "-l", self.model_file,
            "-T", input_file,
            "-p", "0",
            "-distribution"
        ]
        
        try:
            result = subprocess.run(command, capture_output=True, text=True, timeout=60)
            
            if result.returncode == 0:
                predictions = self.parse_predictions(result.stdout)
                self.display_predictions(predictions)
                return predictions
            else:
                print(f"❌ Prediction failed: {result.stderr}")
                return None
                
        except Exception as e:
            print(f"❌ Prediction error: {e}")
            return None
    
    def parse_predictions(self, output):
        """Parse WEKA prediction output"""
        lines = output.split('\n')
        predictions = []
        
        for line in lines:
            if line.strip() and ':' in line and '(' in line:
                try:
                    parts = line.split(':')
                    if len(parts) >= 3:
                        instance_num = int(parts[0].strip())
                        predicted_class = parts[1].strip()
                        
                        confidence_part = parts[2].split('(')[0].strip()
                        confidence = float(confidence_part)
                        
                        predictions.append({
                            'instance': instance_num,
                            'predicted_breed': self.breed_mapping.get(predicted_class, predicted_class),
                            'confidence': confidence
                        })
                except:
                    pass
        
        return predictions
    
    def display_predictions(self, predictions):
        """Display predictions in user-friendly format"""
        print("\n🧬 CAT BREED CLASSIFICATION RESULTS")
        print("=" * 50)
        
        for pred in predictions:
            print(f"Sample {pred['instance']}:")
            print(f"   🏆 Predicted Breed: {pred['predicted_breed']}")
            print(f"   📊 Confidence: {pred['confidence']:.1%}")
            
            if pred['confidence'] >= 0.9:
                confidence_level = "🟢 Very High"
            elif pred['confidence'] >= 0.7:
                confidence_level = "🟡 High" 
            elif pred['confidence'] >= 0.5:
                confidence_level = "🟠 Moderate"
            else:
                confidence_level = "🔴 Low"
                
            print(f"   🎯 Confidence Level: {confidence_level}")
            print()
    
    def get_model_info(self):
        """Display model information"""
        print("🤖 CAT BREED CLASSIFIER MODEL INFO")
        print("=" * 50)
        print("Version: 1.0.0")
        print("Algorithm: Random Forest (300 trees)")
        print("Training Data: 2016 samples, 7 breeds")
        print("SNP Features: 93 biologically-encoded markers")
        print("Expected Accuracy: 90.58%")
        print("Validation: 5-fold cross-validation")
        print("\nSupported Breeds:")
        for orig, display in self.breed_mapping.items():
            print(f"   - {display}")
        print("\nInput Requirements:")
        print("   - ARFF format file")
        print("   - 93 SNP attributes (ISAGFC01-ISAGFC98)")
        print("   - Biological encoding (0=Ref/Ref, 1=Het, 2=Alt/Alt, -1=Missing)")

def main():
    parser = argparse.ArgumentParser(description='Cat Breed Classification using SNP data')
    parser.add_argument('input_file', nargs='?', help='Input ARFF file with SNP data')
    parser.add_argument('--info', action='store_true', help='Show model information')
    
    args = parser.parse_args()
    
    predictor = CatBreedPredictor()
    
    if args.info:
        predictor.get_model_info()
    elif args.input_file:
        predictor.predict_sample(args.input_file)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
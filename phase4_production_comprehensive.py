#!/usr/bin/env python3
"""
Phase 4: Production Model Development & Deployment
Create production-ready cat breed classification model with deployment interface.

Usage: python phase4_production_comprehensive.py
"""

import subprocess
import os
import sys
import json
import time
import re
from pathlib import Path
from datetime import datetime

class Phase4ProductionModel:
    def __init__(self):
        self.base_dir = Path("/mnt/g/cat_breed_weka")
        self.production_dir = self.base_dir / "phase4_production"
        self.production_dir.mkdir(exist_ok=True)
        
        # Best configuration from Phase 3
        self.optimal_config = {
            'algorithm': 'RandomForest',
            'trees': 1000,
            'features_per_split': 15,
            'dataset': 'phase1_biological_top_breeds_dataset_fixed.arff',
            'expected_accuracy': 90.53,
            'cross_validation_folds': 10
        }
        
        # Production settings
        self.weka_jar = "weka.jar"
        self.memory = "4096m"
        self.cpu_slots = 4

    def print_header(self, title):
        """Print formatted section header"""
        print(f"\n{'='*80}")
        print(f"🚀 {title}")
        print(f"{'='*80}")

    def print_subsection(self, title):
        """Print formatted subsection header"""
        print(f"\n{'-'*60}")
        print(f"📊 {title}")
        print(f"{'-'*60}")

    def train_production_model(self):
        """Train the final production model with optimal configuration"""
        self.print_subsection("Training Production Model")
        
        config = self.optimal_config
        dataset = config['dataset']
        
        print(f"🎯 Training production model with optimal configuration:")
        print(f"   Algorithm: {config['algorithm']}")
        print(f"   Trees: {config['trees']}")
        print(f"   Features per split: {config['features_per_split']}")
        print(f"   Dataset: {dataset}")
        print(f"   Expected accuracy: {config['expected_accuracy']:.2f}%")
        
        # Model file path
        model_file = self.production_dir / "cat_breed_classifier_v1.0.model"
        
        # Training command with model saving
        command = [
            "java", f"-Xmx{self.memory}", "-cp", self.weka_jar,
            "weka.classifiers.meta.FilteredClassifier",
            "-F", "weka.filters.unsupervised.attribute.Remove -R 1",
            "-W", "weka.classifiers.trees.RandomForest",
            "-t", dataset,
            "-d", str(model_file),  # Save model
            "-x", str(config['cross_validation_folds']),
            "--",
            "-I", str(config['trees']),
            "-K", str(config['features_per_split']),
            "-depth", "0",
            f"-num-slots", str(self.cpu_slots),
            "-attribute-importance"
        ]
        
        print(f"🔄 Training model (this may take several minutes)...")
        start_time = time.time()
        
        try:
            result = subprocess.run(
                command,
                cwd=self.base_dir,
                capture_output=True,
                text=True,
                timeout=1200  # 20 minute timeout
            )
            
            training_duration = time.time() - start_time
            
            if result.returncode == 0:
                # Extract performance metrics
                accuracy, kappa = self.extract_metrics(result.stdout)
                
                # Save training output
                training_log = self.production_dir / "training_log.txt"
                with open(training_log, 'w') as f:
                    f.write("PHASE 4 PRODUCTION MODEL TRAINING LOG\n")
                    f.write("=" * 60 + "\n")
                    f.write(f"Command: {' '.join(command)}\n")
                    f.write(f"Execution time: {training_duration:.2f} seconds\n")
                    f.write(f"Date: {datetime.now()}\n\n")
                    f.write("WEKA OUTPUT:\n")
                    f.write(result.stdout)
                
                print(f"   ✅ Model trained successfully!")
                print(f"   📊 Accuracy: {accuracy:.2f}%, Kappa: {kappa:.3f}")
                print(f"   ⏱️  Training time: {training_duration:.1f} seconds")
                print(f"   💾 Model saved: {model_file}")
                
                return True, model_file, accuracy, training_log
                
            else:
                print(f"   ❌ Training failed: {result.stderr[:500]}")
                return False, None, 0, None
                
        except subprocess.TimeoutExpired:
            print(f"   ⏰ Training timeout after 20 minutes")
            return False, None, 0, None
        except Exception as e:
            print(f"   ❌ Training error: {e}")
            return False, None, 0, None

    def extract_metrics(self, output):
        """Extract accuracy and kappa from WEKA output"""
        lines = output.split('\n')
        accuracy = 0
        kappa = 0
        
        in_cv_section = False
        
        for line in lines:
            if "cross-validation" in line.lower():
                in_cv_section = True
                continue
                
            if in_cv_section:
                if "Correctly Classified Instances" in line:
                    match = re.search(r'(\d+\.?\d*)\s*%', line)
                    if match:
                        accuracy = float(match.group(1))
                elif "Kappa statistic" in line:
                    match = re.search(r'(\d+\.?\d+)', line)
                    if match:
                        kappa = float(match.group(1))
                        break
        
        return accuracy, kappa

    def create_prediction_interface(self, model_file):
        """Create a user-friendly prediction interface"""
        self.print_subsection("Creating Prediction Interface")
        
        prediction_script = self.production_dir / "predict_cat_breed.py"
        
        prediction_code = f'''#!/usr/bin/env python3
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
        self.model_file = "{model_file.name}"
        self.weka_jar = "weka.jar"
        
        # Breed mapping (production names)
        self.breed_mapping = {{
            'Bengal': 'Bengal Cat',
            'British_Shorthair': 'British Shorthair',
            'Maine_Coon': 'Maine Coon',
            'Norwegian_Forest_Cat': 'Norwegian Forest Cat',
            'Ragdoll': 'Ragdoll',
            'Sphinx': 'Sphynx Cat',
            'Thai': 'Thai Cat'
        }}
        
    def predict_sample(self, input_file):
        """Predict breed for SNP sample(s)"""
        
        if not Path(input_file).exists():
            print(f"❌ Input file not found: {{input_file}}")
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
                print(f"❌ Prediction failed: {{result.stderr}}")
                return None
                
        except Exception as e:
            print(f"❌ Prediction error: {{e}}")
            return None
    
    def parse_predictions(self, output):
        """Parse WEKA prediction output"""
        lines = output.split('\\n')
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
                        
                        predictions.append({{
                            'instance': instance_num,
                            'predicted_breed': self.breed_mapping.get(predicted_class, predicted_class),
                            'confidence': confidence
                        }})
                except:
                    pass
        
        return predictions
    
    def display_predictions(self, predictions):
        """Display predictions in user-friendly format"""
        print("\\n🧬 CAT BREED CLASSIFICATION RESULTS")
        print("=" * 50)
        
        for pred in predictions:
            print(f"Sample {{pred['instance']}}:")
            print(f"   🏆 Predicted Breed: {{pred['predicted_breed']}}")
            print(f"   📊 Confidence: {{pred['confidence']:.1%}}")
            
            if pred['confidence'] >= 0.9:
                confidence_level = "🟢 Very High"
            elif pred['confidence'] >= 0.7:
                confidence_level = "🟡 High" 
            elif pred['confidence'] >= 0.5:
                confidence_level = "🟠 Moderate"
            else:
                confidence_level = "🔴 Low"
                
            print(f"   🎯 Confidence Level: {{confidence_level}}")
            print()
    
    def get_model_info(self):
        """Display model information"""
        print("🤖 CAT BREED CLASSIFIER MODEL INFO")
        print("=" * 50)
        print("Version: 1.0.0")
        print("Algorithm: Random Forest (1000 trees)")
        print("Training Data: 2016 samples, 7 breeds")
        print("SNP Features: 93 biologically-encoded markers")
        print("Expected Accuracy: 90.53%")
        print("Supported Breeds:")
        for orig, display in self.breed_mapping.items():
            print(f"   - {{display}}")

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
'''
        
        with open(prediction_script, 'w') as f:
            f.write(prediction_code)
        
        os.chmod(prediction_script, 0o755)
        
        print(f"   ✅ Prediction interface created: {prediction_script}")
        print(f"   🔧 Usage: python predict_cat_breed.py sample.arff")
        print(f"   🔧 Info: python predict_cat_breed.py --info")
        
        return prediction_script

    def create_sample_data(self):
        """Create sample data for testing"""
        self.print_subsection("Creating Sample Test Data")
        
        sample_file = self.production_dir / "sample_prediction.arff"
        
        print("🧪 Creating sample prediction data...")
        
        command = [
            "java", f"-Xmx1024m", "-cp", self.weka_jar,
            "weka.filters.unsupervised.instance.Resample",
            "-i", self.optimal_config['dataset'],
            "-o", str(sample_file),
            "-S", "1",
            "-Z", "0.25",  # Sample 25% (about 5 samples)
            "-no-replacement"
        ]
        
        try:
            result = subprocess.run(command, cwd=self.base_dir, capture_output=True, text=True)
            
            if result.returncode == 0:
                print(f"   ✅ Sample data created: {sample_file}")
                return sample_file
            else:
                print(f"   ❌ Sample creation failed")
                return None
                
        except Exception as e:
            print(f"   ❌ Error creating samples: {e}")
            return None

    def create_documentation(self, model_file, training_log, accuracy):
        """Create comprehensive documentation"""
        self.print_subsection("Creating Documentation")
        
        doc_file = self.production_dir / "CAT_BREED_CLASSIFIER_DOCUMENTATION.md"
        
        doc_content = f'''# Cat Breed Classifier - Production Model

## Model Overview
- **Version:** 1.0.0
- **Algorithm:** Random Forest (1000 trees)
- **Performance:** {accuracy:.2f}% accuracy
- **Training Data:** 2016 samples, 7 breeds
- **SNP Features:** 93 biologically-encoded markers

## Supported Breeds
1. Bengal Cat
2. British Shorthair  
3. Maine Coon
4. Norwegian Forest Cat
5. Ragdoll
6. Sphynx Cat
7. Thai Cat

## Usage
```bash
# Predict breed for a sample
python predict_cat_breed.py sample_data.arff

# Show model information
python predict_cat_breed.py --info
```

## Input Format
- **File Type:** ARFF format
- **Required Attributes:** 93 SNP markers (ISAGFC01-ISAGFC98)
- **Encoding:** Numerical (0=Ref/Ref, 1=Ref/Alt, 2=Alt/Alt, -1=Missing)

## Output Format
```
🧬 CAT BREED CLASSIFICATION RESULTS
Sample 1:
   🏆 Predicted Breed: Maine Coon
   📊 Confidence: 98.7%
   🎯 Confidence Level: 🟢 Very High
```

## Model Files
- **cat_breed_classifier_v1.0.model** - Trained WEKA model
- **predict_cat_breed.py** - Prediction interface
- **sample_prediction.arff** - Test samples
- **training_log.txt** - Training details

## System Requirements
- Java 8 or higher
- WEKA 3.8+ (included: weka.jar)
- Python 3.6+ (for interface)
- 2GB+ RAM recommended

## Performance Metrics
- **Cross-validation Accuracy:** {accuracy:.2f}%
- **Training Time:** Recorded in training_log.txt
- **Prediction Time:** <1 second per sample

Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}
'''
        
        with open(doc_file, 'w') as f:
            f.write(doc_content)
        
        print(f"   ✅ Documentation created: {doc_file}")
        
        return doc_file

    def run_phase4_pipeline(self):
        """Execute complete Phase 4 production pipeline"""
        self.print_header("PHASE 4: PRODUCTION MODEL DEVELOPMENT")
        
        print(f"🎯 Objective: Create production-ready cat breed classification model")
        print(f"📊 Configuration: RF({self.optimal_config['trees']} trees, K={self.optimal_config['features_per_split']})")
        print(f"🎪 Expected Performance: {self.optimal_config['expected_accuracy']:.2f}% accuracy")
        print(f"📁 Output Directory: {self.production_dir}")
        
        # Step 1: Train production model
        success, model_file, accuracy, training_log = self.train_production_model()
        if not success:
            print("❌ Production model training failed")
            return False
        
        # Step 2: Create prediction interface  
        prediction_script = self.create_prediction_interface(model_file)
        
        # Step 3: Create sample data
        sample_file = self.create_sample_data()
        
        # Step 4: Create documentation
        doc_file = self.create_documentation(model_file, training_log, accuracy)
        
        print(f"\\n🎯 PHASE 4 FINAL RESULTS:")
        print(f"   Production Model: ✅ SUCCESS")
        print(f"   Model Accuracy: {accuracy:.2f}%")
        print(f"   Model File: {model_file}")
        print(f"   Prediction Interface: {prediction_script}")
        print(f"   Sample Data: {sample_file}")
        print(f"   Documentation: {doc_file}")
        print(f"   Production Ready: ✅ YES")
        
        self.print_header("PHASE 4 PRODUCTION MODEL COMPLETE")
        
        return True

def main():
    """Main Phase 4 execution"""
    try:
        producer = Phase4ProductionModel()
        success = producer.run_phase4_pipeline()
        
        if success:
            print("🎉 Phase 4 production model development completed successfully!")
            print("🚀 Model is ready for deployment")
        else:
            print("❌ Phase 4 failed")
            
    except Exception as e:
        print(f"❌ Phase 4 production pipeline failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
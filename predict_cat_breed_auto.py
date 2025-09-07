#!/usr/bin/env python3
"""
Automated Cat Breed Prediction Script
Usage: python predict_cat_breed_auto.py try_sample.csv

Automatically converts ACTG data to numerical format and predicts cat breed.
"""

import sys
import csv
import subprocess
import tempfile
import os
from pathlib import Path
import re

def convert_actg_to_numeric_inline(input_file, verbose=True):
    """
    Convert ACTG CSV data to numerical format (simplified version)
    Returns the numerical data as a list
    """
    
    if verbose:
        print(f"🧬 Converting ACTG data: {input_file}")
    
    # Read input CSV
    try:
        with open(input_file, 'r', newline='', encoding='utf-8') as f:
            reader = csv.reader(f)
            header = next(reader)
            rows = list(reader)
            
        if not rows:
            raise ValueError("No data rows found")
            
        print(f"✓ Read {len(rows)} samples with {len(header)} columns")
        
    except Exception as e:
        print(f"❌ ERROR: Could not read input file: {e}")
        return None
    
    # Simple ACTG to numeric conversion
    # This is a simplified version - assumes standard genotype patterns
    def convert_genotype(genotype):
        """Convert single genotype to numeric"""
        if not genotype or genotype.upper() in ['', 'NA', 'N/A', 'NULL', '?', '*', '.', 'N']:
            return -1
        
        genotype = str(genotype).upper().strip()
        
        # Handle different formats
        if genotype in ['AA', 'TT', 'CC', 'GG']:
            return 0  # Homozygous (assuming reference)
        elif len(genotype) == 2 and genotype[0] != genotype[1] and all(c in 'ATCG' for c in genotype):
            return 1  # Heterozygous
        elif genotype == '*':
            return -1  # Missing
        elif len(genotype) == 1 and genotype in 'ATCG':
            return 0  # Single allele, assume homozygous
        else:
            return -1  # Unknown format
    
    # Convert each row
    converted_rows = []
    for row_idx, row in enumerate(rows):
        converted_row = []
        
        for col_idx, genotype in enumerate(row):
            numeric_value = convert_genotype(genotype)
            converted_row.append(numeric_value)
        
        converted_rows.append(converted_row)
        
        if verbose and len(converted_rows) == 1:
            missing_count = converted_row.count(-1)
            total_count = len(converted_row)
            print(f"✓ Converted sample: {missing_count}/{total_count} missing ({missing_count/total_count*100:.1f}%)")
    
    return converted_rows[0] if converted_rows else None

def create_arff_file(numeric_data, output_file):
    """Create ARFF file with proper attribute names and breed classes"""
    
    # Correct attribute names (with .1 suffixes for duplicates)
    attributes = [
        'ISAGFC02a', 'ISAGFC02b', 'ISAGFC04a', 'ISAGFC04b', 'ISAGFC05a', 'ISAGFC05b',
        'ISAGFC06a', 'ISAGFC06b', 'ISAGFC07a', 'ISAGFC07b', 'ISAGFC08a', 'ISAGFC08b',
        'ISAGFC09a', 'ISAGFC09b', 'ISAGFC10a', 'ISAGFC10b', 'ISAGFC03a', 'ISAGFC03b',
        'ISAGFC01a', 'ISAGFC01b', 'ISAGFC12a', 'ISAGFC12b', 'ISAGFC15a', 'ISAGFC15b',
        'ISAGFC11a', 'ISAGFC11b', 'ISAGFC18a', 'ISAGFC18b', 'ISAGFC19a', 'ISAGFC19b',
        'ISAGFC12a.1', 'ISAGFC12b.1', 'ISAGFC20a', 'ISAGFC20b', 'ISAGFC13a', 'ISAGFC13b',
        'ISAGFC14a', 'ISAGFC14b', 'ISAGFC16a', 'ISAGFC16b', 'ISAGFC26a', 'ISAGFC26b',
        'ISAGFC22a', 'ISAGFC22b', 'ISAGFC21a', 'ISAGFC21b', 'ISAGFC23a', 'ISAGFC23b',
        'ISAGFC24a', 'ISAGFC24b', 'ISAGFC25a', 'ISAGFC25b', 'ISAGFC30a', 'ISAGFC30b',
        'ISAGFC33a', 'ISAGFC33b', 'ISAGFC31a', 'ISAGFC31b', 'ISAGFC27a', 'ISAGFC27b',
        'ISAGFC34a', 'ISAGFC34b', 'ISAGFC32a', 'ISAGFC32b', 'ISAGFC28a', 'ISAGFC28b',
        'ISAGFC29a', 'ISAGFC29b', 'ISAGFC36a', 'ISAGFC36b', 'ISAGFC37a', 'ISAGFC37b',
        'ISAGFC38a', 'ISAGFC38b', 'ISAGFC30a.1', 'ISAGFC30b.1', 'ISAGFC43a', 'ISAGFC43b',
        'ISAGFC42a', 'ISAGFC42b', 'ISAGFC41a', 'ISAGFC41b', 'ISAGFC40a', 'ISAGFC40b',
        'ISAGFC41a.1', 'ISAGFC41b.1', 'ISAGFC49a', 'ISAGFC49b', 'ISAGFC50a', 'ISAGFC50b',
        'ISAGFC46a', 'ISAGFC46b', 'ISAGFC45a', 'ISAGFC45b', 'ISAGFC47a', 'ISAGFC47b',
        'ISAGFC48a', 'ISAGFC48b', 'ISAGFC54a', 'ISAGFC54b', 'ISAGFC55a', 'ISAGFC55b',
        'ISAGFC56a', 'ISAGFC56b', 'ISAGFC57a', 'ISAGFC57b', 'ISAGFC59a', 'ISAGFC59b',
        'ISAGFC58a', 'ISAGFC58b', 'ISAGFC51a', 'ISAGFC51b', 'ISAGFC52a', 'ISAGFC52b',
        'ISAGFC53a', 'ISAGFC53b', 'ISAGFC60a', 'ISAGFC60b', 'ISAGFC64a', 'ISAGFC64b',
        'ISAGFC61a', 'ISAGFC61b', 'ISAGFC62a', 'ISAGFC62b', 'ISAGFC63a', 'ISAGFC63b',
        'ISAGFC68a', 'ISAGFC68b', 'ISAGFC66a', 'ISAGFC66b', 'ISAGFC67a', 'ISAGFC67b',
        'ISAGFC65a', 'ISAGFC65b', 'ISAGFC69a', 'ISAGFC69b', 'ISAGFC70a', 'ISAGFC70b',
        'ISAGFC71a', 'ISAGFC71b', 'ISAGFC73a', 'ISAGFC73b', 'ISAGFC72a', 'ISAGFC72b',
        'ISAGFC74a', 'ISAGFC74b', 'ISAGFC75a', 'ISAGFC75b', 'ISAGFC76a', 'ISAGFC76b',
        'ISAGFC78a', 'ISAGFC78b', 'ISAGFC79a', 'ISAGFC79b', 'ISAGFC80a', 'ISAGFC80b',
        'ISAGFC81a', 'ISAGFC81b', 'ISAGFC82a', 'ISAGFC82b', 'ISAGFC84a', 'ISAGFC84b',
        'ISAGFC85a', 'ISAGFC85b', 'ISAGFC83a', 'ISAGFC83b', 'ISAGFC86a', 'ISAGFC86b',
        'ISAGFC87a', 'ISAGFC87b', 'ISAGFC88a', 'ISAGFC88b', 'ISAGFC89a', 'ISAGFC89b',
        'ISAGFC90a', 'ISAGFC90b', 'ISAGFC91a', 'ISAGFC91b', 'ISAGFC92a', 'ISAGFC92b',
        'ISAGFC93a', 'ISAGFC93b', 'ISAGFC94a', 'ISAGFC94b', 'ISAGFC95a', 'ISAGFC95b',
        'ISAGFC96a', 'ISAGFC96b', 'ISAGFC97a', 'ISAGFC97b', 'ISAGFC98a', 'ISAGFC98b'
    ]
    
    # Breed classes from training data
    breed_classes = [
        'Abyssinian', 'Bengal', 'Birman', 'British Longhair', 'British Shorthair',
        'Burmese', 'Cornish Rex', 'Devon Rex', 'Egyptian Mau', 'Exotic Shorthair',
        'Highland Fold', 'Maine Coon', 'Norwegian Forest Cat', 'Oriental Short hair',
        'Persian', 'Ragdoll', 'Russian blue', 'Savannah', 'Scottish Fold', 'Siamese',
        'Siberian Cat', 'Siberian cat', 'Somali', 'Sphinx', 'Thai', 'Tonkinese'
    ]
    
    try:
        with open(output_file, 'w', newline='', encoding='utf-8') as f:
            # Write ARFF header
            f.write("@RELATION cat_breed_prediction\n\n")
            
            # Write SNP attributes
            for attr in attributes:
                f.write(f"@ATTRIBUTE {attr} NUMERIC\n")
            
            # Write breed class attribute (with proper quoting)
            breed_str = ','.join([f"'{breed}'" if ' ' in breed else breed for breed in breed_classes])
            f.write(f"@ATTRIBUTE BREED {{{breed_str}}}\n\n")
            
            # Write data section
            f.write("@DATA\n")
            data_str = ','.join(str(val) for val in numeric_data)
            f.write(f"{data_str},?\n")
            
        print(f"✓ Created ARFF file: {output_file}")
        return True
        
    except Exception as e:
        print(f"❌ ERROR: Could not create ARFF file: {e}")
        return False

def run_weka_prediction(arff_file, model_file="cat_breed_classifier_production.model", weka_jar="weka.jar"):
    """Run WEKA prediction and parse results"""
    
    try:
        # Check if required files exist
        if not Path(model_file).exists():
            raise FileNotFoundError(f"Model file not found: {model_file}")
        if not Path(weka_jar).exists():
            raise FileNotFoundError(f"WEKA jar not found: {weka_jar}")
        if not Path(arff_file).exists():
            raise FileNotFoundError(f"ARFF file not found: {arff_file}")
        
        print("🤖 Running WEKA prediction...")
        
        # Run WEKA command
        cmd = [
            "java", "-Xmx4G", "-cp", weka_jar,
            "weka.classifiers.meta.FilteredClassifier",
            "-l", model_file,
            "-T", arff_file,
            "-p", "0",
            "-distribution"
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        
        if result.returncode != 0:
            raise RuntimeError(f"WEKA prediction failed: {result.stderr}")
        
        return result.stdout
        
    except subprocess.TimeoutExpired:
        raise RuntimeError("WEKA prediction timed out")
    except Exception as e:
        raise RuntimeError(f"Prediction error: {e}")

def parse_prediction_results(weka_output):
    """Parse WEKA output to extract breed prediction and confidence"""
    
    try:
        lines = weka_output.strip().split('\n')
        
        # Look for prediction data line (not header)
        prediction_line = None
        for line in lines:
            if line.strip() and line.strip()[0].isdigit() and '?' in line:
                prediction_line = line.strip()
                break
        
        if not prediction_line:
            raise ValueError("Could not find prediction in WEKA output")
        
        # Parse prediction line: "        1        1:? 16:Ragdoll       0.028,0.014,..."
        parts = prediction_line.split()
        if len(parts) < 4:
            raise ValueError(f"Unexpected prediction format: {prediction_line}")
        
        # Extract breed name from predicted part
        predicted_part = parts[2]  # "16:Ragdoll"  
        breed_name = predicted_part.split(':')[1] if ':' in predicted_part else predicted_part
        
        # Find distribution values (look for the comma-separated part)
        distribution_str = None
        for part in parts[3:]:
            if ',' in part and any(c.isdigit() for c in part):
                distribution_str = part
                break
        
        if not distribution_str:
            raise ValueError("Could not find distribution data")
        distribution_values = [float(x.replace('*', '')) for x in distribution_str.split(',')]
        
        # Map to breed names (in order from training data)
        breed_classes = [
            'Abyssinian', 'Bengal', 'Birman', 'British Longhair', 'British Shorthair',
            'Burmese', 'Cornish Rex', 'Devon Rex', 'Egyptian Mau', 'Exotic Shorthair',
            'Highland Fold', 'Maine Coon', 'Norwegian Forest Cat', 'Oriental Short hair',
            'Persian', 'Ragdoll', 'Russian blue', 'Savannah', 'Scottish Fold', 'Siamese',
            'Siberian Cat', 'Siberian cat', 'Somali', 'Sphinx', 'Thai', 'Tonkinese'
        ]
        
        distribution = {}
        for i, prob in enumerate(distribution_values):
            if i < len(breed_classes):
                distribution[breed_classes[i]] = prob
        
        # Find the highest confidence breed and value
        max_breed = max(distribution.items(), key=lambda x: x[1])
        confidence = max_breed[1]
        
        return {
            'breed': breed_name,
            'confidence': confidence,
            'confidence_percent': confidence * 100,
            'distribution': distribution
        }
        
    except Exception as e:
        print(f"⚠️ Could not parse full results: {e}")
        print("Raw WEKA output:")
        print(weka_output)
        return None

def main():
    """Main prediction pipeline"""
    
    if len(sys.argv) != 2:
        print("Usage: python predict_cat_breed_auto.py try_sample.csv")
        print()
        print("This script will:")
        print("1. Convert ACTG genetic data to numerical format")
        print("2. Create proper ARFF file for WEKA")
        print("3. Run breed prediction using the production model")
        print("4. Display results with confidence scores")
        sys.exit(1)
    
    input_file = sys.argv[1]
    
    print("=" * 60)
    print("🐱 AUTOMATED CAT BREED PREDICTION")
    print("=" * 60)
    
    # Step 1: Check input file
    if not Path(input_file).exists():
        print(f"❌ ERROR: Input file not found: {input_file}")
        sys.exit(1)
    
    print(f"📁 Input file: {input_file}")
    
    # Step 2: Convert ACTG to numerical
    print("\n📊 Step 1: Converting ACTG to numerical format...")
    numeric_data = convert_actg_to_numeric_inline(input_file)
    
    if numeric_data is None:
        print("❌ Conversion failed")
        sys.exit(1)
    
    # Step 3: Create ARFF file
    print("\n📝 Step 2: Creating ARFF file...")
    with tempfile.NamedTemporaryFile(mode='w', suffix='.arff', delete=False) as temp_arff:
        temp_arff_path = temp_arff.name
    
    if not create_arff_file(numeric_data, temp_arff_path):
        print("❌ ARFF creation failed")
        sys.exit(1)
    
    # Step 4: Run prediction
    print("\n🎯 Step 3: Running breed prediction...")
    try:
        weka_output = run_weka_prediction(temp_arff_path)
        results = parse_prediction_results(weka_output)
        
        if results:
            print("\n" + "=" * 60)
            print("🏆 PREDICTION RESULTS")
            print("=" * 60)
            print(f"🐾 Predicted Breed: {results['breed']}")
            print(f"📈 Confidence: {results['confidence']:.3f} ({results['confidence_percent']:.1f}%)")
            
            # Data quality assessment
            missing_count = numeric_data.count(-1)
            total_count = len(numeric_data)
            missing_percent = (missing_count / total_count) * 100
            
            print(f"\n📋 Data Quality:")
            print(f"   Missing SNPs: {missing_count}/{total_count} ({missing_percent:.1f}%)")
            
            if missing_percent > 20:
                print("⚠️  High missing data may reduce prediction accuracy")
            elif results['confidence'] < 0.1:
                print("⚠️  Low confidence - consider getting more complete genetic data")
            else:
                print("✅ Good data quality for prediction")
            
            # Show top predictions if distribution available
            if results['distribution']:
                print(f"\n🔍 Top breed probabilities:")
                sorted_breeds = sorted(results['distribution'].items(), key=lambda x: x[1], reverse=True)
                for breed, prob in sorted_breeds[:5]:
                    print(f"   {breed}: {prob:.3f} ({prob*100:.1f}%)")
        
        else:
            print("❌ Could not parse prediction results")
            print("Raw output:")
            print(weka_output)
    
    except Exception as e:
        print(f"❌ Prediction failed: {e}")
        sys.exit(1)
    
    finally:
        # Clean up temporary file
        try:
            os.unlink(temp_arff_path)
        except:
            pass
    
    print("\n✅ Prediction completed successfully!")

if __name__ == "__main__":
    main()
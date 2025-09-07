#!/usr/bin/env python3
"""
Production Prediction Pipeline for Cat Breed Classification - CSV Input Version
Usage: python predict_breed_csv.py input_sample.csv [output_results.csv]

Converts CSV SNP data to ARFF format and predicts cat breeds using the production model.
"""

import sys
import subprocess
import csv
import tempfile
import os
from pathlib import Path

def create_arff_header():
    """Create ARFF header with all 192 SNP attributes and 26 breed classes"""
    
    # All 192 SNP loci (from the training dataset)
    snp_attributes = [
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
    
    # 26 supported cat breeds
    breeds = [
        "Abyssinian", "Bengal", "Birman", "British Longhair", "British Shorthair",
        "Burmese", "Cornish Rex", "Devon Rex", "Egyptian Mau", "Exotic Shorthair",
        "Highland Fold", "Maine Coon", "Norwegian Forest Cat", "Oriental Short hair",
        "Persian", "Ragdoll", "Russian blue", "Savannah", "Scottish Fold", "Siamese",
        "Siberian Cat", "Siberian cat", "Somali", "Sphinx", "Thai", "Tonkinese"
    ]
    
    # Create ARFF header
    header_lines = []
    header_lines.append("@RELATION cat_breed_prediction\\n\\n")
    
    # Add SNP attributes as NUMERIC
    for snp in snp_attributes:
        header_lines.append(f"@ATTRIBUTE {snp} NUMERIC\\n")
    
    # Add breed class attribute
    breed_values = ",".join([f"'{breed}'" if ' ' in breed else breed for breed in breeds])
    header_lines.append(f"@ATTRIBUTE BREED {{{breed_values}}}\\n")
    
    header_lines.append("\\n@DATA\\n")
    
    return "".join(header_lines)

def validate_csv_format(csv_file):
    """Validate CSV format and return column information"""
    
    try:
        with open(csv_file, 'r', newline='', encoding='utf-8') as f:
            # Try different delimiters
            sample = f.read(1024)
            f.seek(0)
            
            # Detect delimiter
            delimiter = ','
            if ';' in sample and sample.count(';') > sample.count(','):
                delimiter = ';'
            elif '\\t' in sample:
                delimiter = '\\t'
            
            reader = csv.reader(f, delimiter=delimiter)
            
            # Read header
            header = next(reader)
            header = [col.strip() for col in header]
            
            # Read first data row to check format
            first_row = next(reader)
            
            print(f"CSV Format Detection:")
            print(f"- Delimiter: '{delimiter}'")
            print(f"- Columns: {len(header)}")
            print(f"- Expected: 192 SNP columns (+ optional sample ID)")
            
            return header, delimiter, len(header)
            
    except Exception as e:
        print(f"ERROR: Could not read CSV file: {e}")
        return None, None, 0

def convert_csv_to_arff(csv_file, output_arff):
    """Convert CSV SNP data to ARFF format"""
    
    # Validate CSV format
    header, delimiter, num_cols = validate_csv_format(csv_file)
    if header is None:
        return False
    
    # Check column count
    expected_snps = 192
    if num_cols < expected_snps:
        print(f"ERROR: CSV has {num_cols} columns, but need {expected_snps} SNP values")
        return False
    elif num_cols > expected_snps + 1:  # Allow for sample ID column
        print(f"WARNING: CSV has {num_cols} columns, using first {expected_snps} as SNP data")
    
    # Determine if first column is sample ID
    has_sample_id = False
    if num_cols == expected_snps + 1:
        # Check if first column looks like sample IDs (non-numeric)
        try:
            with open(csv_file, 'r', newline='', encoding='utf-8') as f:
                reader = csv.reader(f, delimiter=delimiter)
                next(reader)  # Skip header
                first_row = next(reader)
                
                # Try to parse first column as number
                try:
                    float(first_row[0])
                    if '.' not in first_row[0] and first_row[0] not in ['-1', '0', '1', '2']:
                        has_sample_id = True  # Looks like ID if not a typical SNP value
                except ValueError:
                    has_sample_id = True  # Non-numeric = sample ID
                    
        except Exception:
            pass
    
    print(f"Data format: {'Sample ID + 192 SNPs' if has_sample_id else '192 SNPs only'}")
    
    try:
        with open(csv_file, 'r', newline='', encoding='utf-8') as infile:
            with open(output_arff, 'w', encoding='utf-8') as outfile:
                
                # Write ARFF header
                arff_header = create_arff_header()
                outfile.write(arff_header)
                
                # Read and convert data
                reader = csv.reader(infile, delimiter=delimiter)
                next(reader)  # Skip header row
                
                sample_count = 0
                for row in reader:
                    if not row or len(row) < expected_snps:
                        continue
                    
                    # Extract SNP data (skip sample ID if present)
                    snp_start = 1 if has_sample_id else 0
                    snp_data = row[snp_start:snp_start + expected_snps]
                    
                    # Validate and convert SNP values
                    converted_snps = []
                    for snp_val in snp_data:
                        snp_val = snp_val.strip()
                        
                        # Handle missing values
                        if snp_val in ['', 'NA', 'N/A', 'null', '?', '*']:
                            converted_snps.append('-1')
                        # Handle valid SNP values
                        elif snp_val in ['-1', '0', '1', '2']:
                            converted_snps.append(snp_val)
                        # Try to convert other formats
                        else:
                            try:
                                val = int(float(snp_val))
                                if val in [-1, 0, 1, 2]:
                                    converted_snps.append(str(val))
                                else:
                                    converted_snps.append('-1')  # Invalid -> missing
                            except:
                                converted_snps.append('-1')  # Invalid -> missing
                    
                    # Add unknown breed class (will be predicted)
                    converted_snps.append('?')
                    
                    # Write ARFF data line
                    outfile.write(','.join(converted_snps) + '\\n')
                    sample_count += 1
                
                print(f"✓ Converted {sample_count} samples to ARFF format")
                return True
                
    except Exception as e:
        print(f"ERROR: Failed to convert CSV to ARFF: {e}")
        return False

def predict_from_arff(arff_file, output_csv=None):
    """Predict breeds from ARFF file and optionally save to CSV"""
    
    model_file = "cat_breed_classifier_production.model"
    weka_jar = "weka.jar"
    
    if not Path(model_file).exists():
        print(f"ERROR: Production model not found: {model_file}")
        print("Please train the production model first using: ./train_production_model.sh")
        return False
    
    print(f"\\nRunning breed prediction...")
    print(f"Using model: {model_file}")
    
    # Run WEKA prediction
    cmd = [
        "java", "-Xmx2048m", "-cp", weka_jar,
        "weka.classifiers.meta.FilteredClassifier",
        "-l", model_file,
        "-T", arff_file,
        "-p", "0"  # Output predictions with instance numbers
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        
        # Parse predictions
        predictions = []
        confidence_scores = []
        
        lines = result.stdout.split('\\n')
        in_predictions = False
        
        for line in lines:
            line = line.strip()
            
            if line.startswith('inst#'):
                in_predictions = True
                continue
            elif in_predictions and line and not line.startswith('='):
                
                parts = line.split()
                if len(parts) >= 3 and parts[0].isdigit():
                    
                    instance_num = int(parts[0])
                    actual = parts[1] if len(parts) > 1 else "?"
                    predicted = parts[2] if len(parts) > 2 else "unknown"
                    confidence = parts[4] if len(parts) > 4 else "0.0"
                    
                    # Extract breed name from prediction
                    if ':' in predicted:
                        breed_name = predicted.split(':', 1)[1]
                    else:
                        breed_name = predicted
                    
                    # Convert confidence (lower = more confident in WEKA)
                    try:
                        conf_val = float(confidence)
                        conf_pct = max(0, min(100, (1.0 - conf_val) * 100))
                    except:
                        conf_pct = 0.0
                    
                    predictions.append({
                        'sample_id': f"Sample_{instance_num}",
                        'predicted_breed': breed_name,
                        'confidence': conf_pct
                    })
        
        # Display results
        print(f"\\n" + "="*60)
        print("BREED PREDICTION RESULTS")
        print("="*60)
        
        for pred in predictions:
            print(f"{pred['sample_id']:12} → {pred['predicted_breed']:25} ({pred['confidence']:.1f}% confidence)")
        
        print(f"\\nTotal samples processed: {len(predictions)}")
        
        # Save to CSV if requested
        if output_csv and predictions:
            try:
                with open(output_csv, 'w', newline='', encoding='utf-8') as f:
                    writer = csv.DictWriter(f, fieldnames=['sample_id', 'predicted_breed', 'confidence'])
                    writer.writeheader()
                    writer.writerows(predictions)
                
                print(f"✓ Results saved to: {output_csv}")
                
            except Exception as e:
                print(f"WARNING: Could not save to CSV: {e}")
        
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"ERROR: Prediction failed")
        print(f"Command: {' '.join(cmd)}")
        print(f"Error output: {e.stderr}")
        return False

def main():
    if len(sys.argv) < 2 or len(sys.argv) > 3:
        print("Usage: python predict_breed_csv.py input_sample.csv [output_results.csv]")
        print("")
        print("CSV Input Format:")
        print("  Option 1: 192 SNP columns (ISAGFC02a, ISAGFC02b, ...)")
        print("  Option 2: Sample ID + 192 SNP columns")
        print("")
        print("SNP Values:")
        print("  - Valid: -1 (missing), 0, 1, 2 (allele states)")
        print("  - Missing: NA, N/A, null, ?, *, empty")
        print("")
        print("Example:")
        print("  python predict_breed_csv.py samples.csv results.csv")
        print("")
        print("Supported Breeds (26):")
        breeds = [
            "Abyssinian", "Bengal", "Birman", "British Longhair", "British Shorthair",
            "Burmese", "Cornish Rex", "Devon Rex", "Egyptian Mau", "Exotic Shorthair", 
            "Highland Fold", "Maine Coon", "Norwegian Forest Cat", "Oriental Short hair",
            "Persian", "Ragdoll", "Russian blue", "Savannah", "Scottish Fold", "Siamese",
            "Siberian Cat", "Siberian cat", "Somali", "Sphinx", "Thai", "Tonkinese"
        ]
        for i, breed in enumerate(breeds, 1):
            print(f"  {i:2d}. {breed}")
        
        sys.exit(1)
    
    input_csv = sys.argv[1]
    output_csv = sys.argv[2] if len(sys.argv) > 2 else None
    
    # Verify input file
    if not Path(input_csv).exists():
        print(f"ERROR: Input CSV file not found: {input_csv}")
        sys.exit(1)
    
    print("="*60)
    print("CAT BREED PREDICTION - CSV INPUT")
    print("="*60)
    print(f"Input file: {input_csv}")
    if output_csv:
        print(f"Output file: {output_csv}")
    
    # Create temporary ARFF file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.arff', delete=False) as tmp_arff:
        temp_arff_file = tmp_arff.name
    
    try:
        # Convert CSV to ARFF
        print(f"\\nStep 1: Converting CSV to ARFF format...")
        if not convert_csv_to_arff(input_csv, temp_arff_file):
            sys.exit(1)
        
        # Run prediction
        print(f"\\nStep 2: Running cat breed classification...")
        success = predict_from_arff(temp_arff_file, output_csv)
        
        if success:
            print(f"\\n✅ Prediction completed successfully!")
            if output_csv:
                print(f"📄 Results saved to: {output_csv}")
        else:
            print(f"\\n❌ Prediction failed")
            sys.exit(1)
            
    finally:
        # Clean up temporary file
        try:
            os.unlink(temp_arff_file)
        except:
            pass

if __name__ == "__main__":
    main()
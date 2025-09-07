#!/usr/bin/env python3
"""
Excel to Cat Breed Prediction Pipeline
Reads Excel files with SNP data and performs direct breed classification.

Usage:
    python predict_from_excel.py sample.xlsx
    python predict_from_excel.py sample.xlsx --output results.txt
    python predict_from_excel.py --help
"""

import pandas as pd
import subprocess
import sys
import argparse
import os
import tempfile
from pathlib import Path
import time

class ExcelCatBreedPredictor:
    def __init__(self):
        self.model_file = "cat_breed_classifier_v1.0.model"
        self.weka_jar = "weka.jar"
        self.reference_panel_file = "../ISAG_reference_panel.xlsx"
        
        # Load ISAG reference panel for biological encoding
        self.reference_panel = self.load_reference_panel()
        
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
        
        # Expected SNP markers (93 total) - must match training data exactly
        self.expected_snps = [
            'ISAGFC01', 'ISAGFC02', 'ISAGFC03', 'ISAGFC04', 'ISAGFC05', 
            'ISAGFC06', 'ISAGFC07', 'ISAGFC08', 'ISAGFC09', 'ISAGFC10',
            'ISAGFC11', 'ISAGFC12', 'ISAGFC13', 'ISAGFC14', 'ISAGFC15', 
            'ISAGFC16', 'ISAGFC18', 'ISAGFC19', 'ISAGFC20', 'ISAGFC21',
            'ISAGFC22', 'ISAGFC23', 'ISAGFC24', 'ISAGFC25', 'ISAGFC26',
            'ISAGFC27', 'ISAGFC28', 'ISAGFC29', 'ISAGFC30', 'ISAGFC31',
            'ISAGFC32', 'ISAGFC33', 'ISAGFC34', 'ISAGFC36', 'ISAGFC37',
            'ISAGFC38', 'ISAGFC40', 'ISAGFC41', 'ISAGFC42', 'ISAGFC43',
            'ISAGFC45', 'ISAGFC46', 'ISAGFC47', 'ISAGFC48', 'ISAGFC49',
            'ISAGFC50', 'ISAGFC51', 'ISAGFC52', 'ISAGFC53', 'ISAGFC54',
            'ISAGFC55', 'ISAGFC56', 'ISAGFC57', 'ISAGFC58', 'ISAGFC59',
            'ISAGFC60', 'ISAGFC61', 'ISAGFC62', 'ISAGFC63', 'ISAGFC64',
            'ISAGFC65', 'ISAGFC66', 'ISAGFC67', 'ISAGFC68', 'ISAGFC69',
            'ISAGFC70', 'ISAGFC71', 'ISAGFC72', 'ISAGFC73', 'ISAGFC74',
            'ISAGFC75', 'ISAGFC76', 'ISAGFC78', 'ISAGFC79', 'ISAGFC80',
            'ISAGFC81', 'ISAGFC82', 'ISAGFC83', 'ISAGFC84', 'ISAGFC85',
            'ISAGFC86', 'ISAGFC87', 'ISAGFC88', 'ISAGFC89', 'ISAGFC90',
            'ISAGFC91', 'ISAGFC92', 'ISAGFC93', 'ISAGFC94', 'ISAGFC95',
            'ISAGFC96', 'ISAGFC97', 'ISAGFC98'
        ]

    def load_reference_panel(self):
        """Load ISAG reference panel for biological encoding"""
        try:
            if os.path.exists(self.reference_panel_file):
                ref_df = pd.read_excel(self.reference_panel_file)
                # Create mapping dictionary
                ref_dict = {}
                for _, row in ref_df.iterrows():
                    snp_id = row['ISAG SNP ID']
                    ref_allele = row['Ref']
                    alt_allele = row['Alt']
                    ref_dict[snp_id] = {'ref': ref_allele, 'alt': alt_allele}
                print(f"✅ Loaded reference panel: {len(ref_dict)} SNPs")
                return ref_dict
            else:
                print(f"⚠️  Reference panel not found: {self.reference_panel_file}")
                print("   Using default encoding without biological validation")
                return {}
        except Exception as e:
            print(f"⚠️  Error loading reference panel: {e}")
            return {}

    def encode_genotype_biological(self, genotype_str, snp_id):
        """
        Convert genotype string to biological encoding
        0 = Ref/Ref, 1 = Ref/Alt (Het), 2 = Alt/Alt, -1 = Missing
        """
        if pd.isna(genotype_str) or genotype_str == '' or genotype_str == '??':
            return -1
        
        genotype_str = str(genotype_str).upper().strip()
        
        if len(genotype_str) != 2:
            return -1
        
        allele1, allele2 = genotype_str[0], genotype_str[1]
        
        # Get reference alleles for this SNP
        if snp_id in self.reference_panel:
            ref_allele = self.reference_panel[snp_id]['ref'].upper()
            alt_allele = self.reference_panel[snp_id]['alt'].upper()
        else:
            # If no reference panel, use first allele as ref, second as alt
            unique_alleles = sorted(set([allele1, allele2]))
            if len(unique_alleles) == 1:
                ref_allele = unique_alleles[0]
                alt_allele = unique_alleles[0]  # Homozygous
            else:
                ref_allele = unique_alleles[0]  # Alphabetically first
                alt_allele = unique_alleles[1]   # Alphabetically second
        
        # Count reference and alternative alleles
        ref_count = sum([1 for allele in [allele1, allele2] if allele == ref_allele])
        alt_count = sum([1 for allele in [allele1, allele2] if allele == alt_allele])
        
        # Encode based on biological meaning
        if ref_count == 2:
            return 0  # Homozygous reference
        elif ref_count == 1 and alt_count == 1:
            return 1  # Heterozygous
        elif alt_count == 2:
            return 2  # Homozygous alternative
        else:
            return -1  # Invalid genotype

    def load_excel_data(self, excel_file):
        """Load and validate Excel SNP data"""
        print(f"📊 Loading Excel file: {excel_file}")
        
        try:
            df = pd.read_excel(excel_file)
            print(f"   File loaded: {df.shape[0]} samples, {df.shape[1]} columns")
            
            # Check for expected SNP columns
            missing_snps = [snp for snp in self.expected_snps if snp not in df.columns]
            extra_columns = [col for col in df.columns if col not in self.expected_snps]
            
            if missing_snps:
                print(f"⚠️  Missing SNP columns: {len(missing_snps)} ({missing_snps[:5]}...)")
            
            if extra_columns and len(extra_columns) <= 10:
                print(f"   Extra columns found: {extra_columns}")
            
            # Use only expected SNP columns that exist
            available_snps = [snp for snp in self.expected_snps if snp in df.columns]
            df_filtered = df[available_snps].copy()
            
            print(f"   Using {len(available_snps)}/93 expected SNP columns")
            
            if len(available_snps) < 50:
                print(f"⚠️  Warning: Only {len(available_snps)} SNPs available - predictions may be less reliable")
            
            return df_filtered, available_snps
            
        except Exception as e:
            print(f"❌ Error loading Excel file: {e}")
            return None, []

    def encode_snp_data(self, df, available_snps):
        """Convert SNP data to biological numerical encoding"""
        print(f"🧬 Converting SNP data to biological encoding...")
        
        encoded_data = []
        
        for idx, row in df.iterrows():
            encoded_row = {}
            
            # Process each expected SNP
            for snp in self.expected_snps:
                if snp in available_snps:
                    genotype = row[snp]
                    encoded_value = self.encode_genotype_biological(genotype, snp)
                    encoded_row[snp] = encoded_value
                else:
                    # Missing SNP - encode as missing
                    encoded_row[snp] = -1
            
            encoded_data.append(encoded_row)
        
        encoded_df = pd.DataFrame(encoded_data)
        
        # Calculate encoding statistics
        total_genotypes = len(encoded_df.columns) * len(encoded_df)
        missing_count = (encoded_df == -1).sum().sum()
        valid_count = total_genotypes - missing_count
        
        print(f"   ✅ Encoded {len(encoded_df)} samples")
        print(f"   📊 Valid genotypes: {valid_count}/{total_genotypes} ({valid_count/total_genotypes*100:.1f}%)")
        print(f"   📊 Missing genotypes: {missing_count} ({missing_count/total_genotypes*100:.1f}%)")
        
        return encoded_df

    def create_arff_file(self, encoded_df, temp_file):
        """Create ARFF file from encoded data"""
        print(f"📝 Creating ARFF file: {temp_file}")
        
        with open(temp_file, 'w') as f:
            # Write ARFF header
            f.write("@relation cat_breed_prediction\n\n")
            
            # Write attribute definitions - must match training format
            f.write("@attribute Sample_Name string\n")  # First attribute like training data
            for snp in self.expected_snps:
                f.write(f"@attribute {snp} {{-1,0,1,2}}\n")  # Nominal format like training
            f.write("@attribute BREED {Bengal,British_Shorthair,Maine_Coon,Norwegian_Forest_Cat,Ragdoll,Sphinx,Thai}\n")  # Class attribute
            
            # Write data section
            f.write("\n@data\n")
            
            # Write encoded data
            for idx, row in encoded_df.iterrows():
                sample_name = f'"Sample_{idx+1}"'  # Sample name
                values = [sample_name] + [str(row[snp]) for snp in self.expected_snps] + ['?']  # ? for unknown class
                f.write(','.join(values) + '\n')
        
        print(f"   ✅ ARFF file created with {len(encoded_df)} samples")

    def run_prediction(self, arff_file):
        """Run WEKA prediction on ARFF file"""
        print(f"🤖 Running breed prediction...")
        
        command = [
            "java", "-Xmx2048m", "-cp", self.weka_jar,
            "weka.classifiers.meta.FilteredClassifier",
            "-l", self.model_file,
            "-T", arff_file,
            "-p", "0",
            "-distribution"
        ]
        
        try:
            result = subprocess.run(command, capture_output=True, text=True, timeout=60)
            
            if result.returncode == 0:
                predictions = self.parse_predictions(result.stdout)
                return predictions
            else:
                print(f"❌ Prediction failed")
                print(f"   Command: {' '.join(command)}")
                if result.stderr:
                    print(f"   Error: {result.stderr}")
                if result.stdout:
                    print(f"   Output: {result.stdout}")
                return None
                
        except subprocess.TimeoutExpired:
            print(f"❌ Prediction timeout after 60 seconds")
            return None
        except Exception as e:
            print(f"❌ Prediction error: {e}")
            return None

    def parse_predictions(self, output):
        """Parse WEKA prediction output"""
        lines = output.split('\n')
        predictions = []
        
        for line in lines:
            line = line.strip()
            # Look for prediction lines like: "1        1:?  5:Ragdoll       0.013,0.018,0.026,0.016,*0.903,0.007,0.018"
            if line and not line.startswith('=') and not line.startswith('inst#'):
                try:
                    # Split by whitespace and find the predicted class and confidence
                    parts = line.split()
                    if len(parts) >= 4:
                        instance_num = int(parts[0])
                        predicted_part = parts[2]  # Should be like "5:Ragdoll"
                        distribution_part = parts[3]  # Should be probabilities
                        
                        # Extract predicted class name
                        if ':' in predicted_part:
                            predicted_class = predicted_part.split(':')[1]
                        else:
                            predicted_class = predicted_part
                        
                        # Extract confidence from distribution (marked with *)
                        confidence = 0.0
                        if '*' in distribution_part:
                            for prob in distribution_part.split(','):
                                if '*' in prob:
                                    confidence = float(prob.replace('*', ''))
                                    break
                        
                        predictions.append({
                            'instance': instance_num,
                            'predicted_breed': self.breed_mapping.get(predicted_class, predicted_class),
                            'confidence': confidence
                        })
                except:
                    pass
        
        return predictions

    def display_predictions(self, predictions, excel_file):
        """Display predictions in user-friendly format"""
        print(f"\n🧬 CAT BREED CLASSIFICATION RESULTS")
        print("=" * 60)
        print(f"📁 Input File: {Path(excel_file).name}")
        print(f"📊 Model: Cat Breed Classifier v1.0 (90.58% accuracy)")
        print(f"🕒 Analysis Time: {time.strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 60)
        
        for pred in predictions:
            print(f"\nSample {pred['instance']}:")
            print(f"   🏆 Predicted Breed: {pred['predicted_breed']}")
            print(f"   📊 Confidence: {pred['confidence']:.1%}")
            
            if pred['confidence'] >= 0.9:
                confidence_level = "🟢 Very High"
                reliability = "Excellent prediction quality"
            elif pred['confidence'] >= 0.7:
                confidence_level = "🟡 High" 
                reliability = "Good prediction quality"
            elif pred['confidence'] >= 0.5:
                confidence_level = "🟠 Moderate"
                reliability = "Acceptable with caution"
            else:
                confidence_level = "🔴 Low"
                reliability = "Consider manual review"
                
            print(f"   🎯 Confidence Level: {confidence_level}")
            print(f"   💡 Interpretation: {reliability}")
        
        # Summary statistics
        if predictions:
            avg_confidence = sum(p['confidence'] for p in predictions) / len(predictions)
            high_confidence = sum(1 for p in predictions if p['confidence'] >= 0.8)
            
            print(f"\n📈 PREDICTION SUMMARY:")
            print(f"   • Total samples processed: {len(predictions)}")
            print(f"   • Average confidence: {avg_confidence:.1%}")
            print(f"   • High confidence predictions: {high_confidence}/{len(predictions)}")
            
            # Breed distribution
            breed_counts = {}
            for pred in predictions:
                breed = pred['predicted_breed']
                breed_counts[breed] = breed_counts.get(breed, 0) + 1
            
            if len(breed_counts) > 1:
                print(f"   • Predicted breed distribution:")
                for breed, count in sorted(breed_counts.items()):
                    print(f"     - {breed}: {count} sample(s)")

    def save_results(self, predictions, excel_file, output_file):
        """Save results to text file"""
        try:
            with open(output_file, 'w') as f:
                f.write("Cat Breed Classification Results\n")
                f.write("=" * 50 + "\n")
                f.write(f"Input File: {Path(excel_file).name}\n")
                f.write(f"Analysis Date: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"Model: Cat Breed Classifier v1.0\n\n")
                
                for pred in predictions:
                    f.write(f"Sample {pred['instance']}:\n")
                    f.write(f"  Predicted Breed: {pred['predicted_breed']}\n")
                    f.write(f"  Confidence: {pred['confidence']:.1%}\n")
                    
                    if pred['confidence'] >= 0.9:
                        f.write(f"  Quality: Very High\n")
                    elif pred['confidence'] >= 0.7:
                        f.write(f"  Quality: High\n")
                    elif pred['confidence'] >= 0.5:
                        f.write(f"  Quality: Moderate\n")
                    else:
                        f.write(f"  Quality: Low\n")
                    f.write("\n")
                
                # Summary
                if predictions:
                    avg_confidence = sum(p['confidence'] for p in predictions) / len(predictions)
                    f.write(f"Summary:\n")
                    f.write(f"  Total samples: {len(predictions)}\n")
                    f.write(f"  Average confidence: {avg_confidence:.1%}\n")
            
            print(f"💾 Results saved to: {output_file}")
            
        except Exception as e:
            print(f"⚠️  Could not save results: {e}")

    def predict_from_excel(self, excel_file, output_file=None):
        """Complete pipeline: Excel -> Encoding -> Prediction -> Results"""
        print(f"🚀 Starting Excel-to-Prediction Pipeline")
        print("=" * 60)
        
        # Step 1: Load Excel data
        df, available_snps = self.load_excel_data(excel_file)
        if df is None:
            return False
        
        # Step 2: Encode SNP data
        encoded_df = self.encode_snp_data(df, available_snps)
        
        # Step 3: Create temporary ARFF file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.arff', delete=False) as temp_file:
            temp_arff_path = temp_file.name
        
        try:
            self.create_arff_file(encoded_df, temp_arff_path)
            
            # Step 4: Run prediction
            predictions = self.run_prediction(temp_arff_path)
            
            if predictions:
                # Step 5: Display results
                self.display_predictions(predictions, excel_file)
                
                # Step 6: Save results if requested
                if output_file:
                    self.save_results(predictions, excel_file, output_file)
                
                return True
            else:
                print("❌ Prediction failed")
                return False
                
        finally:
            # Clean up temporary file
            if os.path.exists(temp_arff_path):
                os.unlink(temp_arff_path)

def main():
    parser = argparse.ArgumentParser(
        description='Predict cat breeds from Excel SNP data',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  python predict_from_excel.py sample.xlsx
  python predict_from_excel.py sample.xlsx --output results.txt
  python predict_from_excel.py --help

Input Requirements:
  - Excel file (.xlsx) with SNP genotype data
  - Column names: ISAGFC01, ISAGFC02, ..., ISAGFC98
  - Genotype format: Two-letter codes (e.g., 'AT', 'GC', 'TT')
  - Missing values: Empty cells, '??', or blank
        '''
    )
    
    parser.add_argument('excel_file', help='Input Excel file with SNP data')
    parser.add_argument('--output', '-o', help='Output file for results (optional)')
    
    args = parser.parse_args()
    
    # Check if Excel file exists
    if not Path(args.excel_file).exists():
        print(f"❌ Excel file not found: {args.excel_file}")
        sys.exit(1)
    
    # Create predictor and run pipeline
    try:
        predictor = ExcelCatBreedPredictor()
        success = predictor.predict_from_excel(args.excel_file, args.output)
        
        if success:
            print(f"\n✅ Prediction completed successfully!")
        else:
            print(f"\n❌ Prediction failed")
            sys.exit(1)
            
    except Exception as e:
        print(f"❌ Pipeline error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
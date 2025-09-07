# Excel-to-Prediction Pipeline - Usage Guide

## Overview
The `predict_from_excel.py` script provides a complete pipeline for predicting cat breeds directly from Excel files containing SNP genotype data. It handles Excel reading, biological encoding conversion, and breed classification with confidence scoring.

## Quick Start

### Basic Usage
```bash
# Predict breeds from Excel file
python predict_from_excel.py sample.xlsx

# Save results to file
python predict_from_excel.py sample.xlsx --output results.txt

# Show help
python predict_from_excel.py --help
```

### Example Output
```
🧬 CAT BREED CLASSIFICATION RESULTS
============================================================
📁 Input File: try_sample.xlsx
📊 Model: Cat Breed Classifier v1.0 (90.58% accuracy)
🕒 Analysis Time: 2025-09-06 14:52:34
============================================================

Sample 1:
   🏆 Predicted Breed: Ragdoll
   📊 Confidence: 90.3%
   🎯 Confidence Level: 🟢 Very High
   💡 Interpretation: Excellent prediction quality

📈 PREDICTION SUMMARY:
   • Total samples processed: 1
   • Average confidence: 90.3%
   • High confidence predictions: 1/1
```

## Excel File Requirements

### File Format
- **Format**: Excel (.xlsx files)
- **Samples**: Rows represent individual cat samples
- **SNPs**: Columns represent SNP markers

### Column Requirements
- **93 SNP columns** with names: ISAGFC01, ISAGFC02, ISAGFC03, etc.
- **Required SNPs**: All SNPs from ISAGFC01-ISAGFC98 except ISAGFC17, ISAGFC35, ISAGFC39, ISAGFC44, ISAGFC77
- **Column order**: No specific order required (script finds columns by name)

### Genotype Format
- **Two-letter codes**: AT, GC, TT, CC, etc.
- **Missing values**: Empty cells, "??", or blank entries
- **Example**: ISAGFC01 column might contain: CT, AA, GG, ??, TT

### Sample Excel Structure
```
| ISAGFC01 | ISAGFC02 | ISAGFC03 | ... | ISAGFC98 |
|----------|----------|----------|-----|----------|
|    CT    |    AG    |    AA    | ... |    TT    |
|    AA    |    GG    |    ??    | ... |    CC    |
```

## Biological Encoding Process

### Reference Panel Integration
- Uses ISAG reference panel for Ref/Alt allele definitions
- Automatically loaded from `../ISAG_reference_panel.xlsx`
- Provides biological interpretation of genotypes

### Encoding Rules
- **0**: Homozygous Reference (Ref/Ref) - e.g., AA when A=Ref
- **1**: Heterozygous (Ref/Alt) - e.g., AT when A=Ref, T=Alt  
- **2**: Homozygous Alternative (Alt/Alt) - e.g., TT when T=Alt
- **-1**: Missing genotype data

### Example Encoding
```
SNP: ISAGFC01 (Ref=C, Alt=T)
Input: CT → Output: 1 (Heterozygous)
Input: CC → Output: 0 (Homozygous Reference)  
Input: TT → Output: 2 (Homozygous Alternative)
Input: ?? → Output: -1 (Missing)
```

## Command Line Options

### Required Arguments
- `excel_file`: Path to Excel file with SNP data

### Optional Arguments
- `--output`, `-o`: Save results to text file
- `--help`: Show detailed help message

### Usage Examples
```bash
# Basic prediction
python predict_from_excel.py cats_sample.xlsx

# Save results to specific file
python predict_from_excel.py cats_sample.xlsx -o breed_results.txt

# Process multiple samples in one Excel file
python predict_from_excel.py batch_samples.xlsx --output batch_results.txt
```

## Prediction Results

### Breed Classifications
The model predicts among 7 cat breeds:
- Bengal Cat
- British Shorthair
- Maine Coon
- Norwegian Forest Cat
- Ragdoll
- Sphynx Cat
- Thai Cat

### Confidence Levels
- 🟢 **Very High** (≥90%): Excellent prediction quality
- 🟡 **High** (70-89%): Good prediction quality
- 🟠 **Moderate** (50-69%): Acceptable with caution
- 🔴 **Low** (<50%): Consider manual review

### Output Interpretation
- **Confidence scores** reflect model certainty
- **High confidence** predictions (>80%) are most reliable
- **Low confidence** may indicate mixed ancestry or poor data quality

## Technical Details

### Processing Pipeline
1. **Excel Loading**: Read .xlsx file and validate columns
2. **Reference Integration**: Load ISAG panel for biological encoding
3. **Genotype Encoding**: Convert two-letter codes to numerical values
4. **ARFF Generation**: Create WEKA-compatible format file
5. **Model Prediction**: Run Random Forest classifier
6. **Results Display**: Parse and format predictions

### Performance Metrics
- **Model Accuracy**: 90.58% (cross-validation)
- **Processing Speed**: <1 second per sample
- **Memory Usage**: <2GB for typical files
- **File Size Limit**: No theoretical limit (memory dependent)

### Quality Control
- **Missing SNPs**: Automatically handled as -1 encoding
- **Invalid genotypes**: Converted to missing (-1)
- **Column validation**: Warns about missing expected SNPs
- **Coverage reporting**: Shows percentage of valid genotypes

## Troubleshooting

### Common Issues

1. **File Not Found**
   ```
   ❌ Excel file not found: sample.xlsx
   ```
   **Solution**: Check file path and ensure file exists

2. **Missing Columns**
   ```
   ⚠️  Missing SNP columns: 10 (['ISAGFC17', 'ISAGFC35']...)
   ```
   **Solution**: Missing columns are handled automatically (-1 encoding)

3. **Invalid Genotypes**
   ```
   📊 Valid genotypes: 85/93 (91.4%)
   ```
   **Solution**: Invalid entries converted to missing; check if acceptable

4. **Low Confidence Predictions**
   ```
   🔴 Low confidence (25.3%)
   ```
   **Solution**: May indicate mixed breed, poor data quality, or rare variant

### Data Quality Guidelines
- **Target coverage**: >90% valid genotypes recommended
- **Missing data**: <20% missing SNPs acceptable
- **Sample quality**: High-quality DNA extractions preferred
- **Genotype calling**: Use consistent calling algorithms

## Integration Examples

### Python Integration
```python
import subprocess
import json

def predict_from_excel(excel_file):
    """Wrapper for Excel prediction"""
    result = subprocess.run([
        'python', 'predict_from_excel.py', excel_file
    ], capture_output=True, text=True)
    
    if result.returncode == 0:
        # Parse output for programmatic use
        return result.stdout
    else:
        return None

# Use in your script
results = predict_from_excel('my_cats.xlsx')
```

### Batch Processing
```bash
#!/bin/bash
for file in *.xlsx; do
    echo "Processing $file..."
    python predict_from_excel.py "$file" --output "${file%.xlsx}_results.txt"
done
```

## Model Information
- **Version**: 1.0.0
- **Training Data**: 2,016 samples across 7 breeds
- **Algorithm**: Random Forest (300 trees)
- **Cross-validation**: 5-fold stratified
- **Expected accuracy**: 90.58%

## File Output Format
When using `--output`, results are saved as:
```
Cat Breed Classification Results
==================================================
Input File: sample.xlsx
Analysis Date: 2025-09-06 14:52:34
Model: Cat Breed Classifier v1.0

Sample 1:
  Predicted Breed: Ragdoll
  Confidence: 90.3%
  Quality: Very High

Summary:
  Total samples: 1
  Average confidence: 90.3%
```

## System Requirements
- Python 3.6+ with pandas
- Java 8+ (for WEKA)
- 2GB+ RAM recommended
- WEKA JAR file in same directory

## Support
For technical issues:
1. Verify Excel file format matches requirements
2. Check that all required files are present (model, WEKA JAR)
3. Ensure sufficient system memory for large files
4. Validate SNP column names match ISAG panel
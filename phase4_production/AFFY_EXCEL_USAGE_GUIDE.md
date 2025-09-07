# Affy SNP ID Excel-to-Prediction Pipeline - Usage Guide

## Overview
The `predict_from_affy_excel.py` script provides a complete pipeline for predicting cat breeds directly from Excel files containing Affy SNP ID genotype data. It automatically maps Affy SNP IDs to ISAG SNP IDs, performs biological encoding conversion, and provides breed classification with confidence scoring - all without requiring external reference files.

## Key Features
- **Embedded Affy-to-ISAG mapping**: No external reference files needed for deployment
- **Automatic SNP detection**: Finds Affy SNP ID columns automatically
- **Complete biological encoding**: Converts genotypes using ISAG reference panel
- **Real-time prediction**: Fast breed classification with confidence scoring
- **Deployment-ready**: Self-contained script with embedded mappings

## Quick Start

### Basic Usage
```bash
# Predict breeds from Affy Excel file
python predict_from_affy_excel.py sample_affy.xlsx

# Save results to file
python predict_from_affy_excel.py sample_affy.xlsx --output results.txt

# Show help
python predict_from_affy_excel.py --help
```

### Example Output
```
🧬 CAT BREED CLASSIFICATION RESULTS (Affy SNP Input)
======================================================================
📁 Input File: try_sample_affy_id.xlsx
📊 Model: Cat Breed Classifier v1.0 (90.58% accuracy)
🔬 Input Method: Affy SNP IDs → ISAG SNP IDs
📈 SNP Mapping: 93 Affy SNP IDs mapped
======================================================================

Sample 1:
   🏆 Predicted Breed: Ragdoll
   📊 Confidence: 90.3%
   🎯 Confidence Level: 🟢 Very High
   💡 Interpretation: Excellent prediction quality

📈 PREDICTION SUMMARY:
   • Total samples processed: 1
   • Average confidence: 90.3%
   • Affy SNP IDs successfully used: 93
```

## Excel File Requirements

### File Format
- **Format**: Excel (.xlsx files)
- **Samples**: Rows represent individual cat samples
- **SNPs**: Columns represent Affy SNP markers

### Column Requirements
- **Affy SNP ID columns** with names like: `Affx-535157362`, `Affx-1288305263`, etc.
- **93 supported Affy SNP IDs** that map to ISAG panel
- **Column order**: No specific order required (script finds columns by name)

### Genotype Format
- **Two-letter codes**: AT, GC, TT, CC, etc.
- **Missing values**: Empty cells, "??", or blank entries
- **Example**: Affx-535157362 column might contain: CT, AA, GG, ??, TT

### Sample Excel Structure
```
| Affx-535157362 | Affx-1288305263 | Affx-535151870 | ... | Affx-535150634 |
|----------------|-----------------|----------------|-----|----------------|
|       CT       |       AG        |       AA       | ... |       TT       |
|       AA       |       GG        |       ??       | ... |       CC       |
```

## Affy SNP ID to ISAG Mapping

### Embedded Mapping System
The script contains **93 embedded Affy SNP ID mappings** to ISAG SNP IDs:

**Example Mappings:**
```
Affx-535157362  → ISAGFC01
Affx-1288305263 → ISAGFC02
Affx-535151870  → ISAGFC03
Affx-535157357  → ISAGFC04
Affx-1288305264 → ISAGFC05
...
```

### Coverage Information
- **Total mappings**: 93 Affy SNP IDs → 93 ISAG SNP IDs
- **Complete coverage**: All ISAG panel SNPs supported
- **No external files**: Mappings embedded in script for deployment
- **Automatic detection**: Script finds matching columns automatically

## Processing Pipeline

### Step-by-Step Process
1. **Excel Loading**: Read .xlsx file and detect Affy SNP ID columns
2. **Affy Detection**: Find columns matching `Affx-XXXXXXX` pattern
3. **ISAG Mapping**: Map detected Affy IDs to ISAG SNP IDs
4. **Biological Encoding**: Convert genotypes using ISAG reference panel
5. **ARFF Generation**: Create WEKA-compatible format file
6. **Model Prediction**: Run Random Forest classifier
7. **Results Display**: Parse and format predictions with confidence

### Technical Details
- **Automatic column detection**: Uses regex pattern matching
- **Reference panel integration**: Loads ISAG panel for biological encoding
- **Missing data handling**: Automatically manages incomplete data
- **Performance**: <1 second processing time per sample

## Command Line Options

### Required Arguments
- `excel_file`: Path to Excel file with Affy SNP ID data

### Optional Arguments
- `--output`, `-o`: Save results to text file
- `--help`: Show detailed help message

### Usage Examples
```bash
# Basic prediction
python predict_from_affy_excel.py cats_affy.xlsx

# Save results to specific file
python predict_from_affy_excel.py cats_affy.xlsx -o breed_results.txt

# Process multiple samples in one Excel file
python predict_from_affy_excel.py batch_affy_samples.xlsx --output batch_results.txt
```

## Supported Affy SNP IDs

### Full List of 93 Mapped Affy SNP IDs
The script supports exactly these Affy SNP IDs:

**A Series (ISAGFC01-ISAGFC10):**
```
Affx-535157362  → ISAGFC01    Affx-1288305263 → ISAGFC02
Affx-535151870  → ISAGFC03    Affx-535157357  → ISAGFC04  
Affx-1288305264 → ISAGFC05    Affx-535157359  → ISAGFC06
Affx-1288305265 → ISAGFC07    Affx-535157360  → ISAGFC08
Affx-535157361  → ISAGFC09    Affx-1017004495 → ISAGFC10
```

**B Series (ISAGFC11-ISAGFC20):**
```
Affx-1288305266 → ISAGFC11    Affx-535157366  → ISAGFC12
Affx-535157367  → ISAGFC13    Affx-535152421  → ISAGFC14
Affx-1017801567 → ISAGFC15    Affx-535158719  → ISAGFC16
Affx-535152115  → ISAGFC18    Affx-535150087  → ISAGFC19
Affx-535152311  → ISAGFC20
```

**[Additional series continue through ISAGFC98...]**

### Pattern Recognition
The script automatically recognizes columns with names matching:
- Pattern: `Affx-[0-9]+` (case-insensitive)
- Examples: `Affx-535157362`, `AFFX-1288305263`, `affx-535151870`

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
- **Affy SNP mapping** shows how many SNPs were successfully used

## Deployment Advantages

### Self-Contained Design
- **No external reference files**: Affy-to-ISAG mappings embedded in script
- **Deployment simplicity**: Just copy script + model files
- **Version control**: Mappings versioned with script code
- **Portability**: Runs anywhere with Python + Java + WEKA

### Files Required for Deployment
```
Minimal deployment package:
├── predict_from_affy_excel.py          # Main script (embedded mappings)
├── cat_breed_classifier_v1.0.model    # Trained model
├── weka.jar                           # WEKA toolkit
└── ISAG_reference_panel.xlsx          # Reference panel (optional*)
```

*Reference panel optional - script includes fallback encoding if not available

## Troubleshooting

### Common Issues

1. **No Affy SNP ID columns found**
   ```
   ❌ No Affy SNP ID columns found (expected format: Affx-XXXXXXX)
   ```
   **Solution**: Ensure column names match `Affx-XXXXXXX` pattern exactly

2. **No mappings found**
   ```
   ❌ No Affy SNP IDs could be mapped to ISAG panel
   ```
   **Solution**: Check that Affy SNP IDs match the 93 supported IDs

3. **Low mapping coverage**
   ```
   ⚠️  Only 20/93 Affy SNP IDs mapped
   ```
   **Solution**: Acceptable but may reduce prediction accuracy

4. **File format errors**
   ```
   ❌ Error loading Affy Excel file
   ```
   **Solution**: Ensure .xlsx format and valid Excel structure

### Data Quality Guidelines
- **Target coverage**: All 93 Affy SNP IDs recommended for best accuracy
- **Minimum coverage**: >50 SNPs acceptable for basic predictions
- **Missing data**: <20% missing genotypes per sample preferred
- **Genotype format**: Consistent two-letter coding (AT, GC, etc.)

## Comparison with Other Input Methods

### Input Method Comparison
| Method | Script | Mapping | Coverage | Deployment |
|---------|--------|---------|-----------|------------|
| **ISAG SNP IDs** | predict_cat_breed.py | Direct | 100% | Standard |
| **Excel ISAG** | predict_from_excel.py | Reference file | 100% | + Excel file |
| **Affy Excel** | predict_from_affy_excel.py | Embedded | 100% | Self-contained |

### When to Use Affy Excel Method
- **Commercial array data**: When working with Affymetrix array output
- **Deployment simplicity**: When embedded mappings preferred
- **Standard formats**: When Excel input is most convenient
- **Cross-platform validation**: When comparing against commercial arrays

## Integration Examples

### Python Integration
```python
import subprocess

def predict_from_affy_excel(excel_file):
    """Wrapper for Affy Excel prediction"""
    result = subprocess.run([
        'python', 'predict_from_affy_excel.py', excel_file
    ], capture_output=True, text=True)
    
    if result.returncode == 0:
        return result.stdout
    else:
        return None

# Use in your script
results = predict_from_affy_excel('my_affy_cats.xlsx')
```

### Batch Processing
```bash
#!/bin/bash
for file in *_affy.xlsx; do
    echo "Processing $file..."
    python predict_from_affy_excel.py "$file" --output "${file%.xlsx}_results.txt"
done
```

## Model Information
- **Version**: 1.0.0
- **Training Data**: 2,016 samples across 7 breeds
- **Algorithm**: Random Forest (300 trees)
- **Expected accuracy**: 90.58%
- **Affy SNP support**: 93 commercial array markers

## Support
For technical issues:
1. Verify Excel file contains Affy SNP ID columns (Affx-XXXXXXX format)
2. Check that column names exactly match supported Affy SNP IDs
3. Ensure genotype format uses two-letter codes
4. Validate system requirements (Java 8+, Python 3.6+, WEKA)

## Summary
The Affy Excel prediction pipeline provides seamless integration with commercial Affymetrix array data, offering embedded mappings and self-contained deployment for maximum convenience and reliability in production environments.
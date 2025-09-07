# Cat Breed Classifier - Production Deployment Package

## Overview
Production-ready cat breed classification model using genomic SNP data. Trained with Random Forest on 2,016 samples across 7 cat breeds using ISAG reference panel biological encoding.

## Model Specifications
- **Version**: 1.0.0
- **Algorithm**: Random Forest (300 trees, K=15 features per split)
- **Performance**: 90.58% accuracy (5-fold cross-validation)
- **Training Data**: 2,016 samples, 7 breeds
- **Features**: 93 biologically-encoded SNP markers (ISAGFC01-ISAGFC98)

## Supported Breeds
1. Bengal Cat
2. British Shorthair  
3. Maine Coon
4. Norwegian Forest Cat
5. Ragdoll
6. Sphynx Cat
7. Thai Cat

## Quick Start

### System Requirements
- Java 8 or higher
- Python 3.6+ (for interface)
- 2GB+ RAM recommended

### Usage
```bash
# Show model information
python predict_cat_breed.py --info

# Predict breed for sample(s)
python predict_cat_breed.py input_sample.arff
```

### Input Format
- **File Type**: ARFF format
- **Required Attributes**: 93 SNP markers (ISAGFC01-ISAGFC98)
- **Encoding**: Biological (0=Ref/Ref, 1=Ref/Alt, 2=Alt/Alt, -1=Missing)

### Output Format
```
🧬 CAT BREED CLASSIFICATION RESULTS
==================================================
Sample 1:
   🏆 Predicted Breed: Maine Coon
   📊 Confidence: 98.7%
   🎯 Confidence Level: 🟢 Very High
```

## Files Included
- `cat_breed_classifier_v1.0.model` - Trained WEKA model (22MB)
- `predict_cat_breed.py` - Prediction interface
- `weka.jar` - WEKA toolkit (required for predictions)
- `README.md` - This documentation

## Confidence Levels
- 🟢 **Very High**: ≥90% confidence
- 🟡 **High**: 70-89% confidence  
- 🟠 **Moderate**: 50-69% confidence
- 🔴 **Low**: <50% confidence

## Model Performance
- **Cross-validation**: 90.58% accuracy
- **Kappa statistic**: 0.856 (almost perfect agreement)
- **Training time**: ~8 seconds
- **Prediction time**: <1 second per sample

## Technical Details

### Biological SNP Encoding
Based on ISAG reference panel Ref/Alt allele definitions:
- **0**: Homozygous reference (Ref/Ref)
- **1**: Heterozygous (Ref/Alt)
- **2**: Homozygous alternative (Alt/Alt)
- **-1**: Missing genotype data

### Feature Set
93 SNP markers from ISAG feline panel:
- ISAGFC01 through ISAGFC98 (excluding ISAGFC06, 15, 44, 83, 87)
- Selected based on quality control metrics
- Biologically validated for cat breed discrimination

### Model Training
- **Algorithm**: Random Forest with FilteredClassifier
- **Parameter optimization**: Grid search on trees (100-1000) and K (5-25)
- **Cross-validation**: 5-fold stratified validation
- **Missing value handling**: Preserved as -1 (biological interpretation)

## Troubleshooting

### Common Issues
1. **Java not found**: Install Java 8+ and ensure it's in PATH
2. **Memory errors**: Increase heap size with `-Xmx4G` if needed
3. **File format errors**: Ensure ARFF format with 93 SNP attributes
4. **Missing attributes**: Verify all ISAGFC01-ISAGFC98 present (excluding gaps)

### Error Messages
- `❌ Input file not found`: Check file path and existence
- `❌ Prediction failed`: Verify ARFF format and attribute names
- `❌ Model not found`: Ensure model file is in same directory

## Citation
If using this model in research, please cite:
- Training dataset: ISAG feline reference panel
- Algorithm: Breiman, L. (2001). Random Forests. Machine Learning 45:5-32
- Implementation: WEKA Machine Learning Workbench

Generated: September 6, 2025
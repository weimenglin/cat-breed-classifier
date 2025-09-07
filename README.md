# Cat Breed Classifier

A production-ready machine learning system for classifying cat breeds from genomic SNP (Single Nucleotide Polymorphism) data using WEKA Random Forest algorithms.

## 🎯 Project Overview

This project implements a comprehensive cat breed classification system that achieves **98.1% accuracy** on purebred cats using genomic data. The system processes SNP markers to identify breed-specific genetic patterns and provides multiple interfaces for prediction including Excel-based tools for non-technical users.

## 🚀 Key Features

- **High Accuracy**: 98.1% classification accuracy on purebred cats
- **Production Ready**: Complete deployment pipeline with validation scripts
- **Excel Integration**: User-friendly Excel interfaces for predictions
- **Multiple Data Formats**: Supports standard and Affymetrix array formats
- **Comprehensive Documentation**: Detailed guides for deployment and usage
- **Research Foundation**: Built on peer-reviewed genomic research data

## 📊 Performance Metrics

| Metric | Score |
|--------|--------|
| **Overall Accuracy** | 98.1% |
| **Cross-Validation** | 10-fold stratified |
| **Model Type** | Random Forest (500 trees) |
| **Training Data** | 1,024 purebred cats, 25 breeds |
| **SNP Markers** | 62,897 genomic positions |

## 🔧 Quick Start

### Production Model Usage

1. **Command Line Prediction:**
```bash
python phase4_production/predict_cat_breed.py sample_data.arff
```

2. **Excel Interface:**
```bash
python phase4_production/predict_from_excel.py your_data.xlsx
```

3. **Affymetrix Format:**
```bash
python phase4_production/predict_from_affy_excel.py affy_data.xlsx
```

### Requirements
- Python 3.7+
- Java 8+ (for WEKA)
- Required packages: `pandas`, `openpyxl`, `subprocess`

## 📁 Project Structure

```
├── phase4_production/           # Production-ready system
│   ├── cat_breed_classifier_v1.0.model  # Trained model (98.1% accuracy)
│   ├── predict_cat_breed.py            # Core prediction script
│   ├── predict_from_excel.py           # Excel interface
│   ├── predict_from_affy_excel.py      # Affymetrix format support
│   ├── README.md                       # Production documentation
│   ├── DEPLOYMENT_GUIDE.md             # Deployment instructions
│   └── EXCEL_USAGE_GUIDE.md           # Excel interface guide
├── phase1_*.py                 # Data preprocessing scripts
├── phase2_*.py                 # Baseline model training
├── phase3_*.py                 # Advanced techniques
├── phase4_*.py                 # Production model development
└── PHASE*_REPORTS.md          # Detailed phase documentation
```

## 🧬 Scientific Background

This project is based on the research paper:
> "Genome-wide SNP-based linkage analysis reveals genomic characteristics in European domestic cats" (Age et al., 2013)

### Supported Cat Breeds

The system can classify the following 25 purebred cat breeds:

- **Asian Breeds**: Siamese, Burmese, Birman, Ragdoll
- **European Breeds**: British Shorthair, Russian Blue, Norwegian Forest Cat
- **American Breeds**: Maine Coon, American Shorthair, Abyssinian
- **Exotic Breeds**: Persian, Exotic Shorthair, Scottish Fold
- And 12+ additional breeds with high genetic distinctiveness

## 📈 Technical Implementation

### Missing Value Encoding Strategy
- **Method**: Missing SNP values encoded as -1
- **Genotypes**: 0 (homozygous reference), 1 (heterozygous), 2 (homozygous alternate)
- **Validation**: Tested against 4 different encoding strategies

### Model Architecture
- **Algorithm**: Random Forest with 500 trees
- **Features**: 62,897 SNP markers after quality control
- **Cross-Validation**: 10-fold stratified sampling
- **Memory**: Optimized for 2-3GB RAM usage

### Data Processing Pipeline
1. **Quality Control**: Remove low-quality SNPs and samples
2. **Breed Filtering**: Focus on breeds with sufficient sample sizes (≥5 samples)
3. **Encoding Optimization**: Convert nominal to numerical format
4. **Model Training**: Random Forest with hyperparameter optimization
5. **Validation**: Cross-validation and independent test sets

## 📚 Documentation

- **[Production Guide](phase4_production/README.md)**: Complete production system overview
- **[Deployment Guide](phase4_production/DEPLOYMENT_GUIDE.md)**: Step-by-step deployment
- **[Excel Usage Guide](phase4_production/EXCEL_USAGE_GUIDE.md)**: Excel interface tutorial
- **[Affymetrix Guide](phase4_production/AFFY_EXCEL_USAGE_GUIDE.md)**: Affymetrix array support
- **[Phase Reports](PHASE4_COMPLETION_REPORT.md)**: Detailed development phases

## 🔬 Research Applications

This system is designed for:
- **Veterinary Genetics**: Breed identification for health screening
- **Animal Breeding**: Genetic diversity assessment
- **Research**: Population genetics and breed evolution studies
- **Commercial**: Pet DNA testing and breed verification

## 🛠️ Development History

The project evolved through 4 systematic phases:

1. **Phase 1**: Data preprocessing and quality control
2. **Phase 2**: Baseline model comparison and feature selection
3. **Phase 3**: Advanced techniques and ensemble methods  
4. **Phase 4**: Production system development and deployment

## 📄 License

This project is based on publicly available research data and is intended for educational and research purposes.

## 🤝 Contributing

Contributions are welcome! Please see the individual phase documentation for technical details and development guidelines.

## 📞 Contact

For questions about this implementation, please open an issue in this repository.

---

**Note**: This system is designed for research and educational purposes. For commercial veterinary applications, additional validation and regulatory compliance may be required.
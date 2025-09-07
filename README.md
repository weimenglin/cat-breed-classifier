# Cat Breed Classifier

A production-ready machine learning system for classifying cat breeds from genomic SNP (Single Nucleotide Polymorphism) data using WEKA Random Forest algorithms.

## 🎯 Project Overview

This project implements a production-ready cat breed classification system that achieves **90.58% accuracy** using standardized ISAG genomic markers. The system processes 93 biologically-validated SNP markers to identify breed-specific genetic patterns and provides multiple interfaces for prediction including Excel-based tools for non-technical users.

## 🚀 Key Features

- **Production Ready**: 90.58% accuracy with standardized ISAG markers
- **Veterinary Standard**: Uses ISAG reference panel for consistent results
- **Excel Integration**: User-friendly Excel interfaces for predictions
- **Multiple Data Formats**: Supports standard and Affymetrix array formats
- **Comprehensive Documentation**: Detailed guides for deployment and usage
- **Standardized Markers**: Built on ISAG feline genomic panel

## 📊 Performance Metrics

| Metric | Score |
|--------|--------|
| **Overall Accuracy** | 90.58% |
| **Cross-Validation** | 5-fold stratified |
| **Model Type** | Random Forest (300 trees) |
| **Training Data** | 2,016 purebred cats, 7 breeds |
| **SNP Markers** | 93 ISAG standardized markers |

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

The production system can classify the following 7 purebred cat breeds:

1. **Bengal Cat** - Distinctive spotted/marbled patterns
2. **British Shorthair** - Classic European breed
3. **Maine Coon** - Large American longhair breed
4. **Norwegian Forest Cat** - Scandinavian forest breed
5. **Ragdoll** - Large, docile breed with color-point patterns
6. **Sphynx Cat** - Hairless breed with unique genetic markers
7. **Thai Cat** - Traditional Siamese-type breed

## 📈 Technical Implementation

### Missing Value Encoding Strategy
- **Method**: Missing SNP values encoded as -1
- **Genotypes**: 0 (homozygous reference), 1 (heterozygous), 2 (homozygous alternate)
- **Validation**: Tested against 4 different encoding strategies

### Model Architecture
- **Algorithm**: Random Forest with 300 trees
- **Features**: 93 ISAG standardized SNP markers (ISAGFC01-ISAGFC98)
- **Cross-Validation**: 5-fold stratified sampling
- **Memory**: Optimized for 2GB RAM usage

### Data Processing Pipeline
1. **ISAG Panel Selection**: Use standardized 93 SNP markers
2. **Biological Encoding**: Apply reference/alternate allele mapping
3. **Breed Standardization**: Focus on 7 genetically distinct breeds
4. **Model Training**: Random Forest with optimized parameters
5. **Validation**: 5-fold cross-validation with stratified sampling

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
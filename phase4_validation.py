#!/usr/bin/env python3
"""
Phase 4: Final Validation & Deployment Preparation
Creates holdout test set and implements advanced validation strategies.
"""

import random
import numpy as np
from pathlib import Path
from collections import Counter, defaultdict
import math

def read_arff_data(filepath):
    """Read ARFF file and extract header and data"""
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    data_start = None
    for i, line in enumerate(lines):
        if line.strip().upper() == '@DATA':
            data_start = i + 1
            break
    
    if data_start is None:
        raise ValueError("@DATA section not found in ARFF file")
    
    header_lines = lines[:data_start]
    data_lines = [line.strip() for line in lines[data_start:] if line.strip()]
    
    return header_lines, data_lines

def get_breed_distribution(data_lines):
    """Get distribution of instances per breed"""
    breed_counts = Counter()
    breed_instances = defaultdict(list)
    
    for i, line in enumerate(data_lines):
        if line.strip():
            breed = line.split(',')[-1].strip().strip("'\"")
            breed_counts[breed] += 1
            breed_instances[breed].append(i)
    
    return breed_counts, breed_instances

def create_stratified_holdout_split(data_lines, test_ratio=0.2, seed=42):
    """Create stratified train/test split preserving class proportions"""
    random.seed(seed)
    
    breed_counts, breed_instances = get_breed_distribution(data_lines)
    
    train_indices = []
    test_indices = []
    
    print(f"Creating {test_ratio:.0%} holdout test set with stratification...")
    print("=" * 60)
    
    for breed, instances in breed_instances.items():
        count = len(instances)
        test_size = max(1, int(count * test_ratio))  # At least 1 instance for test
        
        # Randomly sample test instances
        random.shuffle(instances)
        breed_test = instances[:test_size]
        breed_train = instances[test_size:]
        
        test_indices.extend(breed_test)
        train_indices.extend(breed_train)
        
        print(f"{breed:25} Total:{count:3d} Train:{len(breed_train):3d} Test:{test_size:2d}")
    
    print("=" * 60)
    print(f"Total instances: {len(data_lines)}")
    print(f"Training set: {len(train_indices)} ({100*len(train_indices)/len(data_lines):.1f}%)")
    print(f"Test set: {len(test_indices)} ({100*len(test_indices)/len(data_lines):.1f}%)")
    
    return sorted(train_indices), sorted(test_indices)

def create_holdout_datasets(input_file, output_train, output_test, test_ratio=0.2):
    """Create stratified train/test split datasets"""
    
    # Read original data
    header_lines, data_lines = read_arff_data(input_file)
    
    # Create stratified split
    train_indices, test_indices = create_stratified_holdout_split(data_lines, test_ratio)
    
    # Create training set
    train_data = [data_lines[i] for i in train_indices]
    with open(output_train, 'w', encoding='utf-8') as f:
        f.writelines(header_lines)
        f.write('\n'.join(train_data))
    
    # Create test set
    test_data = [data_lines[i] for i in test_indices]
    with open(output_test, 'w', encoding='utf-8') as f:
        f.writelines(header_lines)
        f.write('\n'.join(test_data))
    
    print(f"\nCreated datasets:")
    print(f"Training: {output_train} ({len(train_data)} instances)")
    print(f"Test: {output_test} ({len(test_data)} instances)")
    
    return len(train_data), len(test_data)

def create_leave_one_breed_out_datasets(input_file, output_dir):
    """Create leave-one-breed-out validation datasets"""
    
    # Read original data
    header_lines, data_lines = read_arff_data(input_file)
    breed_counts, breed_instances = get_breed_distribution(data_lines)
    
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)
    
    print(f"\nCreating Leave-One-Breed-Out datasets...")
    print("=" * 60)
    
    created_datasets = []
    
    for breed in sorted(breed_counts.keys()):
        if breed_counts[breed] < 3:  # Skip breeds with too few instances
            print(f"Skipping {breed:25} (only {breed_counts[breed]} instances)")
            continue
        
        # Create training set (all breeds except current one)
        train_indices = []
        for other_breed, instances in breed_instances.items():
            if other_breed != breed:
                train_indices.extend(instances)
        
        # Test set is the current breed
        test_indices = breed_instances[breed]
        
        # Create filenames
        breed_safe = breed.replace(' ', '_').replace("'", "")
        train_file = output_path / f"lobo_train_without_{breed_safe}.arff"
        test_file = output_path / f"lobo_test_{breed_safe}.arff"
        
        # Write training set
        train_data = [data_lines[i] for i in sorted(train_indices)]
        with open(train_file, 'w', encoding='utf-8') as f:
            f.writelines(header_lines)
            f.write('\n'.join(train_data))
        
        # Write test set
        test_data = [data_lines[i] for i in test_indices]
        with open(test_file, 'w', encoding='utf-8') as f:
            f.writelines(header_lines)
            f.write('\n'.join(test_data))
        
        created_datasets.append((breed, train_file, test_file, len(train_data), len(test_data)))
        print(f"Created LOBO for {breed:25} Train:{len(train_data):4d} Test:{len(test_data):2d}")
    
    print("=" * 60)
    print(f"Total LOBO datasets created: {len(created_datasets)}")
    
    return created_datasets

def analyze_class_balance_impact(data_lines):
    """Analyze the impact of class imbalance on model performance"""
    
    breed_counts, _ = get_breed_distribution(data_lines)
    
    print("\nClass Imbalance Analysis:")
    print("=" * 50)
    
    counts = list(breed_counts.values())
    total_instances = sum(counts)
    
    print(f"Total instances: {total_instances}")
    print(f"Number of classes: {len(breed_counts)}")
    print(f"Min instances: {min(counts)}")
    print(f"Max instances: {max(counts)}")
    print(f"Mean instances: {np.mean(counts):.1f}")
    print(f"Median instances: {np.median(counts):.1f}")
    print(f"Std instances: {np.std(counts):.1f}")
    print(f"Imbalance ratio: {max(counts)/min(counts):.1f}:1")
    
    # Categorize breeds by sample size
    tiny = sum(1 for c in counts if c <= 10)
    small = sum(1 for c in counts if 11 <= c <= 30)
    medium = sum(1 for c in counts if 31 <= c <= 100)
    large = sum(1 for c in counts if c > 100)
    
    print(f"\nBreed size distribution:")
    print(f"Tiny (≤10): {tiny} breeds")
    print(f"Small (11-30): {small} breeds") 
    print(f"Medium (31-100): {medium} breeds")
    print(f"Large (>100): {large} breeds")
    
    # Expected performance by class size
    print(f"\nExpected challenges:")
    if tiny > 0:
        print(f"- {tiny} breeds may have poor recall (insufficient training)")
    if large > 2:
        print(f"- {large} breeds may dominate predictions (class imbalance)")
    
    return breed_counts

def main():
    print("=" * 80)
    print("PHASE 4: FINAL VALIDATION & DEPLOYMENT PREPARATION")
    print("=" * 80)
    
    # Use our best performing dataset
    input_file = "cat_breed_snp_v1_missing_neg1_purebred_fixed.arff"
    
    if not Path(input_file).exists():
        print(f"Error: Input file not found: {input_file}")
        return
    
    print(f"Using optimal dataset: {input_file}")
    
    # Analyze class balance impact
    header_lines, data_lines = read_arff_data(input_file)
    breed_counts = analyze_class_balance_impact(data_lines)
    
    # Create holdout test set (80/20 split)
    print(f"\n" + "=" * 50)
    print("CREATING HOLDOUT TEST SET")
    print("=" * 50)
    
    train_file = "phase4_validation/cat_breed_train_80.arff"
    test_file = "phase4_validation/cat_breed_test_20.arff"
    
    train_size, test_size = create_holdout_datasets(
        input_file, train_file, test_file, test_ratio=0.2
    )
    
    # Create Leave-One-Breed-Out datasets
    print(f"\n" + "=" * 50)
    print("CREATING LEAVE-ONE-BREED-OUT VALIDATION")
    print("=" * 50)
    
    lobo_datasets = create_leave_one_breed_out_datasets(
        input_file, "phase4_validation/lobo"
    )
    
    # Generate validation summary
    print(f"\n" + "=" * 80)
    print("PHASE 4 DATASET CREATION SUMMARY")
    print("=" * 80)
    
    print(f"Original dataset: {len(data_lines)} instances, {len(breed_counts)} breeds")
    print(f"Holdout split: {train_size} train + {test_size} test")
    print(f"LOBO datasets: {len(lobo_datasets)} breed-specific validations")
    
    print(f"\nValidation strategy ready for:")
    print(f"1. Final unbiased performance evaluation (holdout test)")
    print(f"2. Breed-specific generalization testing (LOBO)")
    print(f"3. Production model training (80% training set)")
    print(f"4. Statistical significance testing")
    
    print(f"\nNext steps:")
    print(f"- Train final model on {train_file}")
    print(f"- Evaluate on {test_file} for unbiased performance")
    print(f"- Run LOBO validation for breed generalization")
    print(f"- Generate confusion matrices and error analysis")
    
    print(f"\n✓ Phase 4 dataset preparation completed successfully!")

if __name__ == "__main__":
    main()
#!/bin/bash

# Cache Performance Analysis Automation Script
# Author: Om Tank

ALGORITHMS=("quicksort" "radix")
ARRAY_SIZES=(1024 2048 4096)
BLOCK_SIZES=(32 64 128)
ASSOCIATIVITIES=(1 2 4 8)

RESULTS_DIR="results"
DATA_DIR="data/cachegrind_outputs"

mkdir -p $RESULTS_DIR
mkdir -p $DATA_DIR

echo "=== Cache Performance Analysis Experiment ==="
echo "Starting at: $(date)"

# Block Size Analysis
echo "Phase 1: Block Size Impact Analysis"
for algorithm in "${ALGORITHMS[@]}"; do
    for size in "${ARRAY_SIZES[@]}"; do
        for block_size in "${BLOCK_SIZES[@]}"; do
            echo "Testing $algorithm, size=$size, block_size=$block_size"
            
            output_file="${DATA_DIR}/${algorithm}_size${size}_block${block_size}.out"
            
            valgrind --tool=cachegrind \
                     --D1=32768,1,$block_size \
                     --cachegrind-out-file=$output_file \
                     ./test_harness $algorithm $size > /dev/null 2>&1
            
            # Extract miss rate
            miss_rate=$(cg_annotate $output_file | grep "D1  miss rate:" | awk '{print $4}')
            echo "$algorithm,$size,$block_size,1,$miss_rate" >> ${RESULTS_DIR}/block_size_results.csv
        done
    done
done

# Associativity Analysis  
echo "Phase 2: Associativity Impact Analysis"
for algorithm in "${ALGORITHMS[@]}"; do
    for size in "${ARRAY_SIZES[@]}"; do
        for assoc in "${ASSOCIATIVITIES[@]}"; do
            echo "Testing $algorithm, size=$size, associativity=$assoc"
            
            output_file="${DATA_DIR}/${algorithm}_size${size}_assoc${assoc}.out"
            
            valgrind --tool=cachegrind \
                     --D1=32768,$assoc,128 \
                     --cachegrind-out-file=$output_file \
                     ./test_harness $algorithm $size > /dev/null 2>&1
            
            # Extract miss rate
            miss_rate=$(cg_annotate $output_file | grep "D1  miss rate:" | awk '{print $4}')
            echo "$algorithm,$size,128,$assoc,$miss_rate" >> ${RESULTS_DIR}/associativity_results.csv
        done
    done
done

echo "Experiments completed at: $(date)"
echo "Results saved to: $RESULTS_DIR"

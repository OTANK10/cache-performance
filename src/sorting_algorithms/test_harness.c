#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include "quicksort.h"
#include "radix_sort.h"

#define MAX_SIZE 4096

typedef enum {
    QUICKSORT,
    RADIX_SORT
} algorithm_t;

typedef struct {
    int size;
    algorithm_t algorithm;
    char* description;
} test_config_t;

void generate_random_array(int arr[], int size, int seed) {
    srand(seed);
    for (int i = 0; i < size; i++) {
        arr[i] = rand() % 10000;  // Values 0-9999
    }
}

void copy_array(int src[], int dest[], int size) {
    for (int i = 0; i < size; i++) {
        dest[i] = src[i];
    }
}

int verify_sorted(int arr[], int size) {
    for (int i = 1; i < size; i++) {
        if (arr[i] < arr[i-1]) {
            return 0;  // Not sorted
        }
    }
    return 1;  // Sorted
}

void run_test(test_config_t config) {
    int original[MAX_SIZE];
    int test_array[MAX_SIZE];
    
    printf("Testing %s with array size %d\n", 
           config.description, config.size);
    
    // Generate test data
    generate_random_array(original, config.size, 42);
    copy_array(original, test_array, config.size);
    
    // Run sorting algorithm
    clock_t start = clock();
    
    switch (config.algorithm) {
        case QUICKSORT:
            quicksort(test_array, 0, config.size - 1);
            break;
        case RADIX_SORT:
            radixSort(test_array, config.size);
            break;
    }
    
    clock_t end = clock();
    double cpu_time = ((double)(end - start)) / CLOCKS_PER_SEC;
    
    // Verify correctness
    if (verify_sorted(test_array, config.size)) {
        printf("✓ Sort completed successfully in %.6f seconds\n", cpu_time);
    } else {
        printf("✗ Sort failed - array not properly sorted\n");
    }
}

int main(int argc, char* argv[]) {
    if (argc != 3) {
        printf("Usage: %s <algorithm> <size>\n", argv[0]);
        printf("Algorithms: quicksort, radix\n");
        printf("Sizes: 1024, 2048, 4096\n");
        return 1;
    }
    
    test_config_t config;
    config.size = atoi(argv[2]);
    
    if (strcmp(argv[1], "quicksort") == 0) {
        config.algorithm = QUICKSORT;
        config.description = "Quicksort";
    } else if (strcmp(argv[1], "radix") == 0) {
        config.algorithm = RADIX_SORT;
        config.description = "Radix Sort";
    } else {
        printf("Unknown algorithm: %s\n", argv[1]);
        return 1;
    }
    
    run_test(config);
    return 0;
}

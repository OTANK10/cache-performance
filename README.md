# Cache Performance Analysis: Sorting Algorithms Under Different Memory Hierarchies

* Project Overview

This project provides an in-depth analysis of cache performance for two fundamentally different sorting algorithms: Quicksort and Radix Sort. Using Valgrind's Cachegrind tool, the study examines how cache organization parameters (block size and associativity) impact algorithm performance across varying data sizes.

# Experimental Design  

* Algorithms Analyzed  

* Quicksort

Type: Comparison-based, in-place sorting  

Cache Characteristics:  

High spatial locality during partitioning  
Recursive nature creates varied access patterns  
Benefits from larger block sizes due to sequential access  

Time Complexity: O(n log n) average, O(n²) worst-case  

* Radix Sort  

Type: Non-comparative, digit-based sorting  

Cache Characteristics:  

Indirect memory access patterns  
Multiple passes over data  
Higher cache miss rates due to scattered accesses  


Time Complexity: O(d × n) where d = number of digits  

* Cache Configuration Parameters  

Block Size Analysis

Sizes Tested: 32, 64, 128 bytes  
Purpose: Understand spatial locality impact  
Fixed Parameter: 1-way associativity  

* Associativity Analysis  

Configurations: 1-way, 2-way, 4-way, 8-way  
Purpose: Analyze conflict miss reduction  
Fixed Parameter: 128-byte block size  

* Array Sizes  

Small: 1024 elements (4 KB)  
Medium: 2048 elements (8 KB)  
Large: 4096 elements (16 KB)  

# Key Findings  

Block Size Impact  

Quicksort Performance:  

✅ 32-byte blocks: Highest miss rates (1.5-3.2%)  
✅ 64-byte blocks: Optimal performance (0.7-1.8% miss rate)  
✅ 128-byte blocks: Diminishing returns (1.1-1.6% miss rate)  

Radix Sort Performance:  

❌ All block sizes: Higher miss rates than Quicksort  
❌ Scattered access patterns: Limited benefit from larger blocks  
❌ Indirect memory references: Poor spatial locality utilization  

Associativity Impact  

Critical Insights:  

1-way to 2-way: Dramatic miss rate reduction (up to 50%)  
Beyond 4-way: Minimal performance improvements  
Larger arrays: Better utilization of higher associativity  
Algorithm dependency: Quicksort shows greater sensitivity  

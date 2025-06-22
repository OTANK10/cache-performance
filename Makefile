# Cache Performance Analysis Makefile
# Author: Om Tank

CC = gcc
CFLAGS = -Wall -Wextra -std=c99 -O2
DEBUGFLAGS = -g -DDEBUG
SRCDIR = src/sorting_algorithms
OBJDIR = build
BINDIR = bin

# Source files
SOURCES = $(SRCDIR)/test_harness.c $(SRCDIR)/quicksort.c $(SRCDIR)/radix_sort.c
OBJECTS = $(SOURCES:$(SRCDIR)/%.c=$(OBJDIR)/%.o)
TARGET = $(BINDIR)/test_harness

# Default target
all: directories $(TARGET)

# Create necessary directories
directories:
	@mkdir -p $(OBJDIR) $(BINDIR) results/graphs results/reports data/cachegrind_outputs

# Build main executable
$(TARGET): $(OBJECTS)
	$(CC) $(OBJECTS) -o $@

# Compile object files
$(OBJDIR)/%.o: $(SRCDIR)/%.c
	$(CC) $(CFLAGS) -c $< -o $@

# Debug build
debug: CFLAGS += $(DEBUGFLAGS)
debug: $(TARGET)

# Run experiments
experiments: $(TARGET)
	chmod +x benchmarking/run_experiments.sh
	./benchmarking/run_experiments.sh

# Analyze results
analyze: experiments
	python3 src/analysis_tools/cache_analyzer.py

# Generate performance graphs
graphs:
	python3 src/analysis_tools/visualization.py

# Clean build artifacts
clean:
	rm -rf $(OBJDIR) $(BINDIR)
	rm -f data/cachegrind_outputs/*.out
	rm -f results/*.csv

# Clean all generated files
distclean: clean
	rm -rf results/graphs/* results/reports/*

# Install dependencies (Ubuntu/Debian)
install-deps:
	sudo apt-get update
	sudo apt-get install valgrind python3 python3-pip
	pip3 install pandas matplotlib seaborn numpy scipy

# Validate results
validate:
	@echo "Validating experimental results..."
	@python3 tools/validation_suite.py

# Help target
help:
	@echo "Available targets:"
	@echo "  all          - Build all binaries"
	@echo "  debug        - Build with debug symbols"
	@echo "  experiments  - Run cache performance experiments"
	@echo "  analyze      - Analyze experimental results"
	@echo "  graphs       - Generate performance visualizations"
	@echo "  clean        - Remove build artifacts"
	@echo "  distclean    - Remove all generated files"
	@echo "  install-deps - Install required dependencies"
	@echo "  validate     - Validate experimental results"

.PHONY: all directories debug experiments analyze graphs clean distclean install-deps validate help

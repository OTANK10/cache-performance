import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

class CachePerformanceAnalyzer:
    def __init__(self, data_path):
        self.data = pd.read_csv(data_path)
        self.setup_plotting()
    
    def setup_plotting(self):
        plt.style.use('seaborn-v0_8')
        sns.set_palette("husl")
        plt.rcParams['figure.figsize'] = (12, 8)
        plt.rcParams['font.size'] = 12
    
    def analyze_block_size_impact(self):
        """Analyze how block size affects cache performance"""
        fig, axes = plt.subplots(1, 2, figsize=(15, 6))
        
        algorithms = self.data['algorithm'].unique()
        
        for i, algorithm in enumerate(algorithms):
            algo_data = self.data[self.data['algorithm'] == algorithm]
            
            for size in algo_data['array_size'].unique():
                size_data = algo_data[algo_data['array_size'] == size]
                axes[i].plot(size_data['block_size'], 
                           size_data['miss_rate'], 
                           marker='o', label=f'Size {size}')
            
            axes[i].set_title(f'{algorithm.title()} - Block Size Impact')
            axes[i].set_xlabel('Block Size (bytes)')
            axes[i].set_ylabel('Cache Miss Rate (%)')
            axes[i].legend()
            axes[i].grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig('results/graphs/block_size_impact.png', dpi=300, bbox_inches='tight')
        plt.show()
    
    def analyze_associativity_impact(self):
        """Analyze how associativity affects cache performance"""
        fig, axes = plt.subplots(1, 2, figsize=(15, 6))
        
        algorithms = self.data['algorithm'].unique()
        
        for i, algorithm in enumerate(algorithms):
            algo_data = self.data[self.data['algorithm'] == algorithm]
            
            for size in algo_data['array_size'].unique():
                size_data = algo_data[algo_data['array_size'] == size]
                axes[i].plot(size_data['associativity'], 
                           size_data['miss_rate'], 
                           marker='s', label=f'Size {size}')
            
            axes[i].set_title(f'{algorithm.title()} - Associativity Impact')
            axes[i].set_xlabel('Associativity (ways)')
            axes[i].set_ylabel('Cache Miss Rate (%)')
            axes[i].legend()
            axes[i].grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig('results/graphs/associativity_impact.png', dpi=300, bbox_inches='tight')
        plt.show()
    
    def compare_algorithms(self):
        """Direct comparison between algorithms"""
        pivot_data = self.data.pivot_table(
            values='miss_rate', 
            index=['array_size', 'block_size'], 
            columns='algorithm'
        )
        
        plt.figure(figsize=(12, 8))
        pivot_data.plot(kind='bar', width=0.8)
        plt.title('Algorithm Comparison: Cache Miss Rates')
        plt.xlabel('Array Size & Block Size')
        plt.ylabel('Cache Miss Rate (%)')
        plt.legend(title='Algorithm')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig('results/graphs/algorithm_comparison.png', dpi=300, bbox_inches='tight')
        plt.show()
    
    def statistical_analysis(self):
        """Perform statistical analysis of performance differences"""
        results = {}
        
        for metric in ['block_size', 'associativity']:
            quicksort_data = self.data[self.data['algorithm'] == 'quicksort']['miss_rate']
            radix_data = self.data[self.data['algorithm'] == 'radix']['miss_rate']
            
            # Welch's t-test (unequal variances)
            t_stat, p_value = stats.ttest_ind(quicksort_data, radix_data, equal_var=False)
            
            results[metric] = {
                'quicksort_mean': quicksort_data.mean(),
                'radix_mean': radix_data.mean(),
                'difference': quicksort_data.mean() - radix_data.mean(),
                't_statistic': t_stat,
                'p_value': p_value,
                'significant': p_value < 0.05
            }
        
        return results
    
    def generate_report(self):
        """Generate comprehensive performance report"""
        report = []
        report.append("# Cache Performance Analysis Report\n")
        
        # Summary statistics
        summary = self.data.groupby(['algorithm', 'array_size']).agg({
            'miss_rate': ['mean', 'std', 'min', 'max']
        }).round(3)
        
        report.append("## Summary Statistics\n")
        report.append(summary.to_string())
        report.append("\n\n")
        
        # Best configurations
        best_configs = self.data.loc[self.data.groupby('algorithm')['miss_rate'].idxmin()]
        report.append("## Optimal Configurations\n")
        for _, config in best_configs.iterrows():
            report.append(f"**{config['algorithm'].title()}**: ")
            report.append(f"Block Size = {config['block_size']} bytes, ")
            report.append(f"Associativity = {config['associativity']}-way, ")
            report.append(f"Miss Rate = {config['miss_rate']:.3f}%\n")
        
        # Statistical analysis
        stats_results = self.statistical_analysis()
        report.append("\n## Statistical Analysis\n")
        for metric, results in stats_results.items():
            report.append(f"**{metric.title()} Impact**:\n")
            report.append(f"- Quicksort Mean: {results['quicksort_mean']:.3f}%\n")
            report.append(f"- Radix Sort Mean: {results['radix_mean']:.3f}%\n")
            report.append(f"- Statistical Significance: {results['significant']}\n")
        
        # Save report
        with open('results/reports/performance_analysis.md', 'w') as f:
            f.write(''.join(report))
        
        return ''.join(report)

# Usage example
if __name__ == "__main__":
    # Analyze block size results
    analyzer = CachePerformanceAnalyzer('results/block_size_results.csv')
    analyzer.analyze_block_size_impact()
    analyzer.compare_algorithms()
    
    # Generate comprehensive report
    report = analyzer.generate_report()
    print("Analysis complete. Report saved to results/reports/")

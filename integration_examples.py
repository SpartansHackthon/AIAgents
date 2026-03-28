"""
Integration Guide: Connecting Multi-Agent Log Analyzer with Existing Systems

This file demonstrates how to integrate the multi-agent log analyzer with:
1. Existing hate speech detector
2. Custom error handling
3. Production applications
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

from agents.hate_speech_detector import HateSpeechDetector
from agents.multi_agent_orchestrator import MultiAgentOrchestrator


class IntegratedErrorMonitoringSystem:
    """Combines hate speech detection with log analysis."""
    
    def __init__(self):
        """Initialize both the hate speech detector and log analyzer."""
        self.hate_detector = HateSpeechDetector()
        self.log_analyzer = MultiAgentOrchestrator()
    
    def monitor_user_input_and_logs(self, user_input: str, log_file: str = None) -> dict:
        """
        Monitor both user input for hate speech and analyze logs for errors.
        
        Args:
            user_input: User message to check for hate speech
            log_file: Optional log file to analyze
            
        Returns:
            Combined analysis result
        """
        result = {
            'user_input_analysis': None,
            'log_analysis': None,
            'timestamp': None
        }
        
        # Check for hate speech
        print("[SYSTEM] Checking user input for hate speech...")
        try:
            hate_result = self.hate_detector.detect(user_input)
            result['user_input_analysis'] = hate_result
            print(f"  ✓ Hate speech check: {hate_result}")
        except Exception as e:
            print(f"  ⚠ Hate speech check failed: {str(e)}")
        
        # Analyze logs if provided
        if log_file and os.path.exists(log_file):
            print(f"[SYSTEM] Analyzing log file: {log_file}")
            try:
                log_report = self.log_analyzer.analyze_and_solve(log_file)
                result['log_analysis'] = log_report
                result['timestamp'] = log_report['metadata']['timestamp']
                print(f"  ✓ Log analysis complete")
            except Exception as e:
                print(f"  ⚠ Log analysis failed: {str(e)}")
        
        return result


class ProductionLogAnalyzer:
    """Production-ready log analyzer for continuous monitoring."""
    
    def __init__(self, log_directory: str, output_directory: str = './reports'):
        """
        Initialize production analyzer.
        
        Args:
            log_directory: Directory containing log files to monitor
            output_directory: Directory to store analysis reports
        """
        self.log_directory = log_directory
        self.output_directory = output_directory
        self.orchestrator = MultiAgentOrchestrator()
        
        # Create output directory if it doesn't exist
        os.makedirs(output_directory, exist_ok=True)
    
    def analyze_new_logs(self) -> dict:
        """
        Analyze all new log files in the directory.
        
        Returns:
            Dictionary mapping file to analysis report
        """
        results = {}
        
        if not os.path.exists(self.log_directory):
            print(f"❌ Log directory not found: {self.log_directory}")
            return results
        
        log_files = [f for f in os.listdir(self.log_directory) if f.endswith('.log')]
        
        print(f"\n📊 Analyzing {len(log_files)} log files from {self.log_directory}")
        
        for log_file in log_files:
            log_path = os.path.join(self.log_directory, log_file)
            
            try:
                print(f"\n  Analyzing: {log_file}...")
                report = self.orchestrator.analyze_and_solve(log_path)
                results[log_file] = report
                
                # Export report
                report_file = os.path.join(
                    self.output_directory,
                    f"{log_file}_analysis.json"
                )
                self.orchestrator.export_report(report, report_file)
                
                # Print executive summary
                summary = report['executive_summary']
                print(f"    Critical: {summary['critical_issues']} | "
                      f"High: {summary['high_priority_issues']} | "
                      f"Action: {summary['recommended_action']}")
            
            except Exception as e:
                print(f"    ❌ Error analyzing {log_file}: {str(e)}")
                results[log_file] = {'error': str(e)}
        
        return results
    
    def get_critical_issues_summary(self, results: dict) -> dict:
        """
        Generate summary of all critical issues across logs.
        
        Args:
            results: Analysis results from analyze_new_logs
            
        Returns:
            Summary of critical issues
        """
        critical_issues = []
        high_issues = []
        
        for log_file, report in results.items():
            if 'error' in report:
                continue
            
            summary = report.get('executive_summary', {})
            
            # Collect critical errors
            if summary.get('critical_issues', 0) > 0:
                solutions = report.get('solutions', {})
                for sol in solutions.get('all_solutions', []):
                    if sol.get('severity') == 'Critical':
                        critical_issues.append({
                            'file': log_file,
                            'category': sol.get('error_category'),
                            'component': sol.get('affected_component'),
                            'action': sol.get('immediate_actions', [])[0]
                        })
            
            # Collect high priority errors
            if summary.get('high_priority_issues', 0) > 0:
                solutions = report.get('solutions', {})
                for sol in solutions.get('all_solutions', []):
                    if sol.get('severity') == 'High':
                        high_issues.append({
                            'file': log_file,
                            'category': sol.get('error_category'),
                            'component': sol.get('affected_component')
                        })
        
        return {
            'critical_issues': critical_issues,
            'high_priority_issues': high_issues,
            'require_immediate_action': len(critical_issues) > 0
        }


class ErrorRecoveryOrchestrator:
    """Analyzes errors and suggests recovery strategies."""
    
    def __init__(self):
        """Initialize the recovery orchestrator."""
        self.analyzer = MultiAgentOrchestrator()
    
    def suggest_recovery_steps(self, error_message: str) -> dict:
        """
        Suggest recovery steps for a critical error.
        
        Args:
            error_message: The error message
            
        Returns:
            Recovery strategy and steps
        """
        # Analyze the error
        analysis_result = self.analyzer.analyze_single_error(error_message)
        
        solution = analysis_result['solution']
        analysis = analysis_result['analysis']
        
        return {
            'error': error_message,
            'severity': analysis['severity'],
            'category': analysis['error_category'],
            'component': analysis['affected_component'],
            'recovery_steps': {
                'immediate': solution['immediate_actions'],
                'detailed': solution['detailed_solutions'],
                'prevention': solution['prevention_strategy']
            },
            'risk_assessment': analysis['recurrence_risk'],
            'expert_opinion': solution.get('ai_enhanced_solution')
        }


# Example Usage Functions

def example_1_basic_integration():
    """Example: Basic integration with existing system."""
    print("\n" + "=" * 80)
    print("EXAMPLE 1: Basic Integration")
    print("=" * 80)
    
    system = IntegratedErrorMonitoringSystem()
    
    # Monitor user input and logs
    result = system.monitor_user_input_and_logs(
        user_input="This is a normal message",
        log_file="example_logs.log"
    )
    
    print("\n✅ Integration complete")
    if result['user_input_analysis']:
        print(f"  Hate speech detected: {result['user_input_analysis']['is_hate_speech']}")
    if result['log_analysis']:
        print(f"  Log errors found: {result['log_analysis']['log_summary']['error_count']}")


def example_2_production_monitoring():
    """Example: Production-scale log monitoring."""
    print("\n" + "=" * 80)
    print("EXAMPLE 2: Production Monitoring")
    print("=" * 80)
    
    # Assuming you have a logs directory
    analyzer = ProductionLogAnalyzer(
        log_directory="./logs",
        output_directory="./reports"
    )
    
    # Analyze all logs
    results = analyzer.analyze_new_logs()
    
    # Get summary
    summary = analyzer.get_critical_issues_summary(results)
    
    print("\n📋 CRITICAL ISSUES SUMMARY:")
    print(f"  Critical: {len(summary['critical_issues'])}")
    print(f"  High Priority: {len(summary['high_priority_issues'])}")
    print(f"  Immediate Action Required: {summary['require_immediate_action']}")


def example_3_error_recovery():
    """Example: Error recovery and troubleshooting."""
    print("\n" + "=" * 80)
    print("EXAMPLE 3: Error Recovery Strategy")
    print("=" * 80)
    
    orchestrator = ErrorRecoveryOrchestrator()
    
    # Get recovery strategy for a critical error
    recovery = orchestrator.suggest_recovery_steps(
        "OutOfMemoryError: Java heap space - unable to allocate 512MB"
    )
    
    print(f"\n🚨 RECOVERY STRATEGY FOR:")
    print(f"   {recovery['error']}")
    print(f"\n📊 Analysis:")
    print(f"   Severity: {recovery['severity']}")
    print(f"   Category: {recovery['category']}")
    print(f"   Component: {recovery['component']}")
    
    print(f"\n🔧 Recovery Steps:")
    print(f"   Immediate Actions:")
    for i, step in enumerate(recovery['recovery_steps']['immediate'], 1):
        print(f"     {i}. {step}")
    
    print(f"\n🛡️ Prevention Strategy:")
    print(f"   {recovery['recovery_steps']['prevention']}")


def example_4_custom_pipeline():
    """Example: Custom analysis pipeline."""
    print("\n" + "=" * 80)
    print("EXAMPLE 4: Custom Pipeline")
    print("=" * 80)
    
    log_path = "example_logs.log"
    orchestrator = MultiAgentOrchestrator()
    
    # Custom pipeline with selective reporting
    report = orchestrator.analyze_and_solve(log_path)
    
    # Filter only critical issues
    solutions = report['solutions']['all_solutions']
    critical_only = [s for s in solutions if s['severity'] == 'Critical']
    
    print(f"\n🔴 CRITICAL ISSUES ONLY: {len(critical_only)}")
    for i, issue in enumerate(critical_only, 1):
        print(f"\n  #{i} - {issue['error_category']}")
        print(f"      Component: {issue['affected_component']}")
        print(f"      First Action: {issue['immediate_actions'][0]}")


# Main execution

if __name__ == '__main__':
    print("\n🚀 INTEGRATION EXAMPLES - Multi-Agent Log Analyzer")
    print("=" * 80)
    
    try:
        # Basic integration
        if os.path.exists("example_logs.log"):
            example_1_basic_integration()
        else:
            print("\n⚠️  Skipping Example 1: example_logs.log not found")
        
        # Error recovery
        example_3_error_recovery()
        
        # Custom pipeline
        if os.path.exists("example_logs.log"):
            example_4_custom_pipeline()
        else:
            print("\n⚠️  Skipping Example 4: example_logs.log not found")
        
        # Note about production monitoring
        print("\n" + "=" * 80)
        print("ℹ️  Example 2 (Production Monitoring) requires a './logs' directory")
        print("    Create one and add .log files to test this example")
        print("=" * 80)
    
    except Exception as e:
        print(f"\n❌ Error running examples: {str(e)}")
    
    print("\n✅ All examples completed!\n")

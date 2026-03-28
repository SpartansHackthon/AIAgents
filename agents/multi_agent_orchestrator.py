"""Multi-Agent Orchestrator

This orchestrator coordinates multiple agents (LogReader, ErrorAnalyzer, 
SolutionProvider) to provide end-to-end error analysis and solution.

Usage:
    from agents.multi_agent_orchestrator import MultiAgentOrchestrator
    
    orchestrator = MultiAgentOrchestrator()
    result = orchestrator.analyze_and_solve('path/to/logfile.log')
"""

import json
from typing import Dict, Any, List, Optional
from datetime import datetime

from agents.log_reader_agent import LogReaderAgent
from agents.error_analyzer_agent import ErrorAnalyzerAgent
from agents.solution_provider_agent import SolutionProviderAgent


class MultiAgentOrchestrator:
    """Orchestrates multiple agents for complete error analysis and solutions."""
    
    def __init__(self):
        """Initialize all agents."""
        self.log_reader = LogReaderAgent()
        self.error_analyzer = ErrorAnalyzerAgent()
        self.solution_provider = SolutionProviderAgent()
    
    def analyze_and_solve(self, log_file_path: str) -> Dict[str, Any]:
        """
        Complete pipeline: Read logs -> Analyze errors -> Provide solutions.
        
        Args:
            log_file_path: Path to log file
            
        Returns:
            Comprehensive analysis and solutions
        """
        print(f"\n[ORCHESTRATOR] Starting analysis pipeline for: {log_file_path}")
        
        # Step 1: Read logs
        print("[STEP 1/3] Reading logs...")
        log_summary = self.log_reader.get_error_summary(log_file_path)
        print(f"  ✓ Found {log_summary['error_count']} errors and {log_summary['warning_count']} warnings")
        
        # Step 2: Analyze errors
        print("[STEP 2/3] Analyzing errors...")
        error_analyses = self.error_analyzer.batch_analyze(log_summary['errors'])
        analysis_summary = self.error_analyzer.get_analysis_summary(log_summary['errors'])
        print(f"  ✓ Analyzed {len(error_analyses)} errors")
        
        # Step 3: Provide solutions
        print("[STEP 3/3] Generating solutions...")
        solutions_report = self.solution_provider.get_solutions_report(error_analyses)
        print(f"  ✓ Generated solutions for {len(solutions_report['all_solutions'])} errors")
        
        # Compile final report
        final_report = {
            'metadata': {
                'timestamp': datetime.now().isoformat(),
                'log_file': log_file_path,
                'pipeline_status': 'COMPLETED'
            },
            'log_summary': log_summary,
            'error_analysis': {
                'summary': analysis_summary,
                'detailed_analyses': error_analyses
            },
            'solutions': solutions_report,
            'executive_summary': self._generate_executive_summary(
                log_summary, analysis_summary, solutions_report
            )
        }
        
        return final_report
    
    def analyze_single_error(self, error_message: str) -> Dict[str, Any]:
        """
        Analyze a single error message without file.
        
        Args:
            error_message: Error message to analyze
            
        Returns:
            Analysis and solution for the error
        """
        # Create error dict from message
        error = {
            'line_number': 1,
            'message': error_message,
            'type': 'Error',
            'timestamp': datetime.now().isoformat(),
            'context': {'before': [], 'error': error_message, 'after': []}
        }
        
        # Analyze
        analysis = self.error_analyzer.analyze_error(error)
        
        # Solve
        solution = self.solution_provider.provide_solution(analysis)
        
        return {
            'error': error,
            'analysis': analysis,
            'solution': solution,
            'timestamp': datetime.now().isoformat()
        }
    
    def _generate_executive_summary(self, log_summary: Dict[str, Any],
                                    analysis_summary: Dict[str, Any],
                                    solutions_report: Dict[str, Any]) -> Dict[str, Any]:
        """Generate executive summary of the analysis."""
        critical_count = solutions_report['all_solutions'].__len__() if 'all_solutions' in solutions_report else 0
        
        # Count critical issues
        critical = sum(1 for s in solutions_report.get('all_solutions', []) 
                      if s.get('severity') == 'Critical')
        high = sum(1 for s in solutions_report.get('all_solutions', []) 
                  if s.get('severity') == 'High')
        
        return {
            'total_errors': log_summary['error_count'],
            'total_warnings': log_summary['warning_count'],
            'critical_issues': critical,
            'high_priority_issues': high,
            'error_categories': analysis_summary.get('error_category_distribution', {}),
            'affected_components': analysis_summary.get('affected_components', []),
            'recommended_action': self._recommend_action(critical, high)
        }
    
    def _recommend_action(self, critical: int, high: int) -> str:
        """Generate action recommendation based on issue counts."""
        if critical > 0:
            return "🔴 CRITICAL: Immediate attention required. System may be down."
        elif high > 0:
            return "🟠 HIGH: Urgent action needed. System functionality may be impaired."
        elif critical + high >= 5:
            return "🟡 MEDIUM: Review and plan fixes for the next sprint."
        else:
            return "🟢 LOW: Monitor situation. Can be scheduled for upcoming maintenance."
    
    def export_report(self, report: Dict[str, Any], output_file: str) -> None:
        """
        Export report to JSON file.
        
        Args:
            report: Report dictionary from analyze_and_solve
            output_file: Path to output JSON file
        """
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(report, f, indent=2, ensure_ascii=False)
            print(f"\n✅ Report exported to: {output_file}")
        except Exception as e:
            print(f"❌ Error exporting report: {str(e)}")
    
    def print_summary(self, report: Dict[str, Any]) -> None:
        """
        Print a formatted summary of the report.
        
        Args:
            report: Report dictionary
        """
        summary = report.get('executive_summary', {})
        
        print("\n" + "=" * 80)
        print("MULTI-AGENT ERROR ANALYSIS REPORT")
        print("=" * 80)
        
        print(f"\n📊 SUMMARY:")
        print(f"   Total Errors:         {summary.get('total_errors', 0)}")
        print(f"   Total Warnings:       {summary.get('total_warnings', 0)}")
        print(f"   Critical Issues:      {summary.get('critical_issues', 0)}")
        print(f"   High Priority Issues: {summary.get('high_priority_issues', 0)}")
        
        print(f"\n⚠️  ERROR CATEGORIES:")
        for category, count in summary.get('error_categories', {}).items():
            print(f"   - {category}: {count}")
        
        print(f"\n🏗️  AFFECTED COMPONENTS:")
        for component in summary.get('affected_components', []):
            print(f"   - {component}")
        
        print(f"\n📋 RECOMMENDATION:")
        print(f"   {summary.get('recommended_action', 'No action')}")
        
        print("\n" + "=" * 80)
        print("For detailed solutions, see the full report.\n")

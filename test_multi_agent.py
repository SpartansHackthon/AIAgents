"""Test script for the Multi-Agent Log Analyzer system.

Demonstrates how to use the orchestrator to analyze logs and get solutions.
"""

import os
import sys
from dotenv import load_dotenv
from agents.multi_agent_orchestrator import MultiAgentOrchestrator
from agents.log_reader_agent import LogReaderAgent
from agents.error_analyzer_agent import ErrorAnalyzerAgent
from agents.solution_provider_agent import SolutionProviderAgent

# Load environment variables
load_dotenv()


def test_log_reader():
    """Test the LogReaderAgent."""
    print("\n" + "=" * 80)
    print("TEST 1: Log Reader Agent")
    print("=" * 80)
    
    reader = LogReaderAgent()
    
    # Test reading a log file
    log_file = 'example_logs.log'
    if not os.path.exists(log_file):
        print(f"❌ Example log file not found: {log_file}")
        return
    
    try:
        summary = reader.get_error_summary(log_file)
        
        print(f"\n✅ Log Summary:")
        print(f"   File: {summary['file']}")
        print(f"   Total Lines: {summary['total_lines']}")
        print(f"   Error Count: {summary['error_count']}")
        print(f"   Warning Count: {summary['warning_count']}")
        
        print(f"\n📋 First Error Detected:")
        if summary['errors']:
            first_error = summary['errors'][0]
            print(f"   Line {first_error['line_number']}: {first_error['message']}")
            print(f"   Type: {first_error['type']}")
    
    except Exception as e:
        print(f"❌ Error: {str(e)}")


def test_error_analyzer():
    """Test the ErrorAnalyzerAgent."""
    print("\n" + "=" * 80)
    print("TEST 2: Error Analyzer Agent")
    print("=" * 80)
    
    # Create sample error
    sample_error = {
        'line_number': 15,
        'message': 'java.sql.SQLException: Connection refused (Connection refused)',
        'type': 'Exception',
        'timestamp': '2024-03-28 10:16:42',
        'context': {
            'before': [
                'INFO Loading configuration from config.properties',
                'INFO Database connection pool initialized'
            ],
            'error': 'ERROR Failed to connect to database at localhost:5432',
            'after': [
                'ERROR java.sql.SQLException: Connection refused',
                'WARNING Retrying database connection'
            ]
        }
    }
    
    analyzer = ErrorAnalyzerAgent()
    analysis = analyzer.analyze_error(sample_error)
    
    print(f"\n✅ Error Analysis:")
    print(f"   Severity: {analysis['severity']}")
    print(f"   Category: {analysis['error_category']}")
    print(f"   Component: {analysis['affected_component']}")
    print(f"   Recurrence Risk: {analysis['recurrence_risk']}")
    
    print(f"\n🔍 Root Cause Clues:")
    for clue in analysis['root_cause_clues']:
        print(f"   - {clue}")


def test_solution_provider():
    """Test the SolutionProviderAgent."""
    print("\n" + "=" * 80)
    print("TEST 3: Solution Provider Agent")
    print("=" * 80)
    
    # Sample error analysis (from previous test)
    sample_analysis = {
        'original_error': {
            'line_number': 15,
            'message': 'java.sql.SQLException: Connection refused (Connection refused)',
            'type': 'Exception',
        },
        'severity': 'Critical',
        'error_category': 'database',
        'key_indicators': ['Error code: 5432', 'Reference: localhost'],
        'root_cause_clues': [
            'Resource not found - check file paths or URLs',
            'Database issue may have triggered this error'
        ],
        'affected_component': 'Database Layer',
        'recurrence_risk': 'HIGH - Check configuration/setup'
    }
    
    try:
        provider = SolutionProviderAgent()
        solution = provider.provide_solution(sample_analysis)
        
        print(f"\n✅ Solution Generated:")
        print(f"   Category: {solution['error_category']}")
        print(f"   Severity: {solution['severity']}")
        
        print(f"\n💡 Immediate Actions:")
        for i, action in enumerate(solution['immediate_actions'], 1):
            print(f"   {i}. {action}")
        
        print(f"\n🛡️ Prevention Strategy:")
        print(f"   {solution['prevention_strategy']}")
        
        if solution['ai_enhanced_solution']:
            print(f"\n🤖 AI Enhanced Solution:")
            print(f"{solution['ai_enhanced_solution']}")
    
    except Exception as e:
        print(f"❌ Error: {str(e)}")


def test_orchestrator():
    """Test the MultiAgentOrchestrator."""
    print("\n" + "=" * 80)
    print("TEST 4: Multi-Agent Orchestrator (Full Pipeline)")
    print("=" * 80)
    
    log_file = 'example_logs.log'
    if not os.path.exists(log_file):
        print(f"❌ Example log file not found: {log_file}")
        return
    
    try:
        orchestrator = MultiAgentOrchestrator()
        report = orchestrator.analyze_and_solve(log_file)
        
        # Print summary
        orchestrator.print_summary(report)
        
        # Export report
        output_file = 'analysis_report.json'
        orchestrator.export_report(report, output_file)
        print(f"\n✅ Full report exported to: {output_file}")
    
    except Exception as e:
        print(f"❌ Error: {str(e)}")


def test_single_error():
    """Test analyzing a single error message."""
    print("\n" + "=" * 80)
    print("TEST 5: Single Error Analysis")
    print("=" * 80)
    
    error_message = "OutOfMemoryError: Java heap space at java.lang.OutOfMemoryError"
    
    try:
        orchestrator = MultiAgentOrchestrator()
        result = orchestrator.analyze_single_error(error_message)
        
        print(f"\n✅ Analysis Result:")
        print(f"   Severity: {result['analysis']['severity']}")
        print(f"   Category: {result['analysis']['error_category']}")
        print(f"   Component: {result['analysis']['affected_component']}")
        
        print(f"\n💡 Recommended Solutions:")
        solution = result['solution']
        for i, action in enumerate(solution['immediate_actions'], 1):
            print(f"   {i}. {action}")
    
    except Exception as e:
        print(f"❌ Error: {str(e)}")


def main():
    """Run all tests."""
    print("\n🚀 MULTI-AGENT LOG ANALYZER - Test Suite")
    print("=" * 80)
    
    test_log_reader()
    test_error_analyzer()
    test_solution_provider()
    test_orchestrator()
    test_single_error()
    
    print("\n" + "=" * 80)
    print("✅ All tests completed!")
    print("=" * 80)
    print("\n📖 Next steps:")
    print("   1. Run: python log_analyzer.py --file example_logs.log")
    print("   2. Run: python log_analyzer.py (for interactive mode)")
    print("   3. Check analysis_report.json for detailed results\n")


if __name__ == '__main__':
    main()

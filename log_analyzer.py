#!/usr/bin/env python3
"""
Main entry point for the Multi-Agent Log Analyzer system.

This script provides an interactive interface to analyze logs using a 
coordinated system of AI agents that work together to:
1. Read and parse log files
2. Analyze errors and identify patterns
3. Provide expert-level solutions

Usage:
    python log_analyzer.py                    # Interactive mode
    python log_analyzer.py --file logs.log    # Analyze specific file
    python log_analyzer.py --error "error message"  # Analyze single error
"""

import os
import sys
import argparse
import json
from dotenv import load_dotenv

from agents.multi_agent_orchestrator import MultiAgentOrchestrator

# Load environment variables
load_dotenv()


def interactive_mode():
    """Interactive mode for the analyzer."""
    print("\n" + "=" * 80)
    print("🤖 MULTI-AGENT LOG ANALYZER - Interactive Mode")
    print("=" * 80)
    
    try:
        orchestrator = MultiAgentOrchestrator()
        print("\n✅ All agents initialized successfully!\n")
    except ValueError as e:
        print(f"\n❌ Error: {e}")
        print("Please set OPENROUTER_API_KEY in your .env file")
        return 1
    
    print("Commands:")
    print("  1. 'analyze <filepath>' - Analyze a log file")
    print("  2. 'error <message>'     - Analyze a single error message")
    print("  3. 'help'                - Show help")
    print("  4. 'quit'                - Exit")
    print("-" * 80 + "\n")
    
    while True:
        try:
            user_input = input("Enter command: ").strip()
            
            if not user_input:
                continue
            
            if user_input.lower() in ['quit', 'exit', 'q']:
                print("\n👋 Goodbye!\n")
                break
            
            if user_input.lower() == 'help':
                print("\nAvailable Commands:")
                print("  analyze <filepath> - Analyze errors from a log file")
                print("  error <message>    - Analyze a single error message")
                print("  help               - Show this help message")
                print("  quit               - Exit the analyzer\n")
                continue
            
            # Parse analyze command
            if user_input.lower().startswith('analyze '):
                filepath = user_input[8:].strip()
                
                if not os.path.exists(filepath):
                    print(f"❌ File not found: {filepath}\n")
                    continue
                
                print(f"\n⏳ Analyzing log file: {filepath}")
                report = orchestrator.analyze_and_solve(filepath)
                
                # Print summary
                orchestrator.print_summary(report)
                
                # Ask to save
                save_choice = input("Save detailed report to file? (yes/no): ").strip().lower()
                if save_choice in ['yes', 'y']:
                    output_file = filepath.replace('.log', '_analysis.json')
                    orchestrator.export_report(report, output_file)
                
            # Parse error command
            elif user_input.lower().startswith('error '):
                error_msg = user_input[6:].strip()
                
                print(f"\n⏳ Analyzing error message...")
                result = orchestrator.analyze_single_error(error_msg)
                
                # Print analysis
                print("\n" + "=" * 80)
                print("ERROR ANALYSIS RESULT")
                print("=" * 80)
                print(f"\n📝 Error Message:\n{result['error']['message']}")
                
                print(f"\n🔍 Analysis:")
                print(f"   Severity:        {result['analysis']['severity']}")
                print(f"   Category:        {result['analysis']['error_category']}")
                print(f"   Component:       {result['analysis']['affected_component']}")
                print(f"   Root Cause Clues: {', '.join(result['analysis']['root_cause_clues'])}")
                
                print(f"\n💡 Solution:")
                solution = result['solution']
                print(f"   Immediate Actions:")
                for i, action in enumerate(solution['immediate_actions'], 1):
                    print(f"     {i}. {action}")
                
                if solution['ai_enhanced_solution']:
                    print(f"\n   AI Enhanced Solution:")
                    print(f"   {solution['ai_enhanced_solution']}")
                
                print("\n" + "=" * 80 + "\n")
            
            else:
                print("❌ Unknown command. Type 'help' for available commands.\n")
        
        except KeyboardInterrupt:
            print("\n\n👋 Analyzer stopped.")
            break
        except Exception as e:
            print(f"❌ Error: {str(e)}\n")


def file_mode(filepath: str):
    """Analyze a file directly."""
    if not os.path.exists(filepath):
        print(f"❌ File not found: {filepath}")
        return 1
    
    try:
        orchestrator = MultiAgentOrchestrator()
    except ValueError as e:
        print(f"❌ Error: {e}")
        print("Please set OPENROUTER_API_KEY in your .env file")
        return 1
    
    print(f"\n🔍 Analyzing: {filepath}")
    report = orchestrator.analyze_and_solve(filepath)
    orchestrator.print_summary(report)
    
    # Export report
    output_file = filepath.replace('.log', '_analysis.json')
    orchestrator.export_report(report, output_file)
    
    return 0


def error_mode(error_message: str):
    """Analyze a single error message."""
    try:
        orchestrator = MultiAgentOrchestrator()
    except ValueError as e:
        print(f"❌ Error: {e}")
        print("Please set OPENROUTER_API_KEY in your .env file")
        return 1
    
    print(f"\n🔍 Analyzing error: {error_message}\n")
    result = orchestrator.analyze_single_error(error_message)
    
    # Print result
    print("=" * 80)
    print("ANALYSIS RESULT")
    print("=" * 80)
    print(f"\nError: {result['error']['message']}")
    print(f"\nSeverity: {result['analysis']['severity']}")
    print(f"Category: {result['analysis']['error_category']}")
    print(f"Component: {result['analysis']['affected_component']}")
    print(f"\nImmediate Actions:")
    for i, action in enumerate(result['solution']['immediate_actions'], 1):
        print(f"  {i}. {action}")
    print("\n" + "=" * 80)
    
    return 0


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description='Multi-Agent Log Analyzer - Analyze logs and get expert solutions'
    )
    parser.add_argument('--file', '-f', help='Analyze a specific log file')
    parser.add_argument('--error', '-e', help='Analyze a single error message')
    
    args = parser.parse_args()
    
    if args.file:
        return file_mode(args.file)
    elif args.error:
        return error_mode(args.error)
    else:
        return interactive_mode() or 0


if __name__ == '__main__':
    sys.exit(main())

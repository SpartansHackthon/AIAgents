"""Solution Provider Agent

This agent provides expert-level solutions for errors based on 10+ years
of engineering experience. It uses AI to generate context-aware solutions.

Usage:
    from agents.solution_provider_agent import SolutionProviderAgent
    
    provider = SolutionProviderAgent()
    solution = provider.provide_solution(error_analysis)
"""

import os
import requests
from typing import Dict, Any, List
from datetime import datetime


class SolutionProviderAgent:
    """Provides expert solutions for errors using AI."""
    
    def __init__(self):
        """Initialize the solution provider with AI API."""
        self.api_key = os.getenv('OPENROUTER_API_KEY')
        if not self.api_key:
            raise ValueError("OPENROUTER_API_KEY not found in environment variables")
        
        self.api_url = "https://openrouter.ai/api/v1/chat/completions"
        self.model = "gpt-3.5-turbo"
        
        # Expert knowledge base - patterns from 10+ years experience
        self.expert_patterns = {
            'connection': {
                'solutions': [
                    'Check network connectivity and firewall rules',
                    'Verify service endpoints and DNS resolution',
                    'Review connection pooling and timeout settings',
                    'Check for port conflicts or service availability',
                    'Validate SSL/TLS certificate configuration'
                ],
                'prevention': 'Implement circuit breaker pattern and health checks'
            },
            'database': {
                'solutions': [
                    'Check database connection parameters (host, port, credentials)',
                    'Verify database service is running and accessible',
                    'Review SQL query for syntax errors or inefficiency',
                    'Check table/column existence and permissions',
                    'Monitor database resource utilization (connections, memory)'
                ],
                'prevention': 'Use connection pooling and implement query optimization'
            },
            'authentication': {
                'solutions': [
                    'Verify API keys/tokens are valid and not expired',
                    'Check user roles and permissions in the system',
                    'Validate authentication headers and format',
                    'Review token expiration and refresh logic',
                    'Check for IP whitelist or rate limiting blocks'
                ],
                'prevention': 'Implement token rotation and audit logging'
            },
            'parsing': {
                'solutions': [
                    'Validate input data format (JSON/XML structure)',
                    'Check for encoding issues or special characters',
                    'Verify schema matches expected structure',
                    'Handle edge cases like null values or empty strings',
                    'Use strict mode parsing with detailed error messages'
                ],
                'prevention': 'Use schema validation and comprehensive test coverage'
            },
            'resource': {
                'solutions': [
                    'Monitor memory usage and check for memory leaks',
                    'Review application log levels and file rotation',
                    'Check system disk space and cleanup old logs',
                    'Monitor CPU usage and optimize hot paths',
                    'Implement garbage collection tuning if applicable'
                ],
                'prevention': 'Use resource monitoring and set up alerting'
            },
            'file': {
                'solutions': [
                    'Verify file path is correct and file exists',
                    'Check file permissions (read/write/execute)',
                    'Ensure directory structure exists',
                    'Handle special characters in file paths',
                    'Check for disk space and file system health'
                ],
                'prevention': 'Use absolute paths, validate before access'
            },
            'performance': {
                'solutions': [
                    'Profile application to identify bottlenecks',
                    'Optimize database queries and add appropriate indexes',
                    'Implement caching strategy (Redis, Memcached)',
                    'Review network latency and batch operations',
                    'Consider async processing for long-running tasks'
                ],
                'prevention': 'Set performance baselines and continuous monitoring'
            },
            'dependency': {
                'solutions': [
                    'Check dependency version compatibility',
                    'Verify all dependencies are installed correctly',
                    'Review dependency changelogs for breaking changes',
                    'Run dependency audit for security vulnerabilities',
                    'Check Python version compatibility'
                ],
                'prevention': 'Use version pinning and regular dependency updates'
            }
        }
    
    def provide_solution(self, error_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """
        Provide expert solution for an error.
        
        Args:
            error_analysis: Analysis from ErrorAnalyzerAgent
            
        Returns:
            Solution dictionary with multiple approaches
        """
        category = error_analysis.get('error_category', 'UNKNOWN')
        severity = error_analysis.get('severity', 'Medium')
        message = error_analysis.get('original_error', {}).get('message', '')
        
        # Get expert knowledge base solution
        expert_solution = self.expert_patterns.get(
            category.lower(),
            self.expert_patterns.get('UNKNOWN', {})
        )
        
        # Build solution with multiple layers
        solution = {
            'timestamp': datetime.now().isoformat(),
            'error_category': category,
            'severity': severity,
            'immediate_actions': expert_solution.get('solutions', [])[:3],
            'detailed_solutions': expert_solution.get('solutions', []),
            'prevention_strategy': expert_solution.get('prevention', ''),
            'affected_component': error_analysis.get('affected_component', 'Unknown'),
            'root_cause_clues': error_analysis.get('root_cause_clues', []),
            'recurrence_risk': error_analysis.get('recurrence_risk', 'Medium'),
            'ai_enhanced_solution': None  # Will be populated if AI call succeeds
        }
        
        # Try to get AI-enhanced solution
        try:
            ai_solution = self._get_ai_enhanced_solution(error_analysis, solution)
            if ai_solution:
                solution['ai_enhanced_solution'] = ai_solution
        except Exception as e:
            solution['ai_enhanced_solution'] = f"AI service unavailable: {str(e)}"
        
        return solution
    
    def _get_ai_enhanced_solution(self, error_analysis: Dict[str, Any], 
                                  base_solution: Dict[str, Any]) -> str:
        """
        Get AI-enhanced solution using OpenRouter API.
        
        Args:
            error_analysis: Error analysis from analyzer agent
            base_solution: Base solution from expert patterns
            
        Returns:
            AI-generated solution string
        """
        message = error_analysis.get('original_error', {}).get('message', '')
        category = error_analysis.get('error_category', '')
        
        prompt = f"""As a senior software engineer with 10+ years of experience, 
        analyze this error and provide the most efficient solution:

Error Message: {message}
Error Category: {category}
Severity: {error_analysis.get('severity', 'Unknown')}
Affected Component: {error_analysis.get('affected_component', 'Unknown')}
Root Cause Clues: {', '.join(error_analysis.get('root_cause_clues', []))}

Please provide:
1. Most likely root cause
2. Step-by-step solution
3. How to prevent this in the future
4. Code/configuration examples if applicable

Be concise and practical."""

        try:
            response = requests.post(
                self.api_url,
                headers={
                    'Authorization': f'Bearer {self.api_key}',
                    'Content-Type': 'application/json'
                },
                json={
                    'model': self.model,
                    'messages': [
                        {
                            'role': 'system',
                            'content': 'You are a senior software engineer with 10+ years of experience providing practical solutions to production errors.'
                        },
                        {
                            'role': 'user',
                            'content': prompt
                        }
                    ],
                    'temperature': 0.7,
                    'max_tokens': 500
                },
                timeout=30
            )
            
            if response.status_code == 200:
                return response.json()['choices'][0]['message']['content']
            else:
                return None
        except Exception as e:
            raise Exception(f"Error calling AI API: {str(e)}")
    
    def batch_provide_solutions(self, error_analyses: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Provide solutions for multiple errors.
        
        Args:
            error_analyses: List of error analyses
            
        Returns:
            List of solutions
        """
        return [self.provide_solution(analysis) for analysis in error_analyses]
    
    def get_solutions_report(self, error_analyses: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Generate a comprehensive report of all solutions.
        
        Args:
            error_analyses: List of error analyses
            
        Returns:
            Comprehensive report
        """
        solutions = self.batch_provide_solutions(error_analyses)
        
        # Organize by severity
        by_severity = {}
        by_category = {}
        
        for solution in solutions:
            severity = solution['severity']
            category = solution['error_category']
            
            if severity not in by_severity:
                by_severity[severity] = []
            by_severity[severity].append(solution)
            
            if category not in by_category:
                by_category[category] = []
            by_category[category].append(solution)
        
        return {
            'generated_at': datetime.now().isoformat(),
            'total_solutions': len(solutions),
            'by_severity': by_severity,
            'by_category': by_category,
            'all_solutions': solutions,
            'high_priority_items': [s for s in solutions if s['severity'] in ['Critical', 'High']]
        }

"""Error Analyzer Agent

This agent analyzes errors from logs and extracts patterns, severity,
and actionable information.

Usage:
    from agents.error_analyzer_agent import ErrorAnalyzerAgent
    
    analyzer = ErrorAnalyzerAgent()
    analysis = analyzer.analyze_error(error_dict)
"""

import re
from typing import List, Dict, Any, Tuple
from enum import Enum


class ErrorSeverity(Enum):
    """Error severity levels."""
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"
    CRITICAL = "Critical"


class ErrorAnalyzerAgent:
    """Analyzes errors to extract patterns and determine severity."""
    
    def __init__(self):
        """Initialize the error analyzer."""
        self.severity_keywords = {
            'CRITICAL': ['fatal', 'crash', 'panic', 'outage', 'critical', 'blocked'],
            'HIGH': ['error', 'exception', 'failed', 'timeout', 'refused', 'denied'],
            'MEDIUM': ['warn', 'incomplete', 'retry', 'degraded'],
            'LOW': ['info', 'debug', 'notice', 'deprecated']
        }
        
        self.common_error_types = {
            'connection': r'(connection|timeout|network|socket|refused)',
            'database': r'(database|sql|query|transaction|constraint)',
            'authentication': r'(auth|permission|forbidden|unauthorized|401|403)',
            'parsing': r'(parse|json|xml|format|invalid)',
            'resource': r'(memory|disk|cpu|heap|out of)',
            'file': r'(file|path|directory|not found|404)',
            'performance': r'(slow|latency|timeout|throughput)',
            'dependency': r'(import|module|package|library|dependency)',
        }
    
    def analyze_error(self, error: Dict[str, Any]) -> Dict[str, Any]:
        """
        Comprehensive analysis of an error.
        
        Args:
            error: Error dictionary from LogReaderAgent
            
        Returns:
            Detailed analysis dictionary
        """
        message = error.get('message', '').lower()
        
        return {
            'original_error': error,
            'severity': self._determine_severity(message),
            'error_category': self._categorize_error(message),
            'key_indicators': self._extract_key_indicators(error),
            'root_cause_clues': self._identify_root_cause_clues(error),
            'affected_component': self._identify_component(message),
            'recurrence_risk': self._assess_recurrence_risk(message)
        }
    
    def _determine_severity(self, message: str) -> str:
        """Determine error severity."""
        for severity, keywords in self.severity_keywords.items():
            for keyword in keywords:
                if keyword in message:
                    return severity
        return ErrorSeverity.MEDIUM.value
    
    def _categorize_error(self, message: str) -> str:
        """Categorize the error type."""
        for category, pattern in self.common_error_types.items():
            if re.search(pattern, message):
                return category.upper()
        return "UNKNOWN"
    
    def _extract_key_indicators(self, error: Dict[str, Any]) -> List[str]:
        """Extract key indicators from error."""
        indicators = []
        message = error.get('message', '').lower()
        
        # Extract numbers (often error codes)
        numbers = re.findall(r'\b\d{3,}\b', message)
        if numbers:
            indicators.extend([f"Error code: {num}" for num in numbers[:3]])
        
        # Extract quoted strings
        quoted = re.findall(r'"([^"]*)"', message)
        if quoted:
            indicators.extend([f"Reference: {q}" for q in quoted[:2]])
        
        return indicators
    
    def _identify_root_cause_clues(self, error: Dict[str, Any]) -> List[str]:
        """Identify clues for root cause analysis."""
        clues = []
        context = error.get('context', {})
        message = error.get('message', '')
        
        # Check for missing resources
        if any(x in message.lower() for x in ['not found', '404', 'missing']):
            clues.append("Resource not found - check file paths or URLs")
        
        # Check for permission issues
        if any(x in message.lower() for x in ['permission', 'denied', '403', 'access']):
            clues.append("Permission issue - verify user/role privileges")
        
        # Check for timeout
        if 'timeout' in message.lower():
            clues.append("Timeout detected - check service responsiveness")
        
        # Check previous lines for setup/config issues
        before_lines = context.get('before', [])
        if any('config' in line.lower() for line in before_lines):
            clues.append("Configuration issue may have triggered this error")
        
        return clues
    
    def _identify_component(self, message: str) -> str:
        """Identify the affected component."""
        message_lower = message.lower()
        
        if any(x in message_lower for x in ['database', 'db', 'sql']):
            return "Database Layer"
        elif any(x in message_lower for x in ['api', 'http', 'request', 'response']):
            return "API/Network Layer"
        elif any(x in message_lower for x in ['file', 'disk', 'io', 'storage']):
            return "File System"
        elif any(x in message_lower for x in ['auth', 'permission', 'user', 'token']):
            return "Authentication/Authorization"
        elif any(x in message_lower for x in ['memory', 'heap', 'gc', 'cpu']):
            return "System Resources"
        else:
            return "Application Logic"
    
    def _assess_recurrence_risk(self, message: str) -> str:
        """Assess likelihood of error recurring."""
        message_lower = message.lower()
        
        # High recurrence risk
        if any(x in message_lower for x in ['config', 'environment', 'setup', 'initialization']):
            return "HIGH - Check configuration/setup"
        
        # Medium recurrence risk
        if any(x in message_lower for x in ['timeout', 'retry', 'transient', 'temporary']):
            return "MEDIUM - May happen again under load"
        
        # Low recurrence risk
        if any(x in message_lower for x in ['one-time', 'specific user', 'unique']):
            return "LOW - Unlikely to recur"
        
        return "MEDIUM - Standard assumption"
    
    def batch_analyze(self, errors: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Analyze multiple errors at once.
        
        Args:
            errors: List of error dictionaries
            
        Returns:
            List of analyzed errors
        """
        return [self.analyze_error(error) for error in errors]
    
    def get_analysis_summary(self, errors: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Get summary of all error analyses.
        
        Args:
            errors: List of error dictionaries
            
        Returns:
            Summary statistics
        """
        analyses = self.batch_analyze(errors)
        
        severities = {}
        categories = {}
        components = set()
        
        for analysis in analyses:
            severity = analysis['severity']
            category = analysis['error_category']
            component = analysis['affected_component']
            
            severities[severity] = severities.get(severity, 0) + 1
            categories[category] = categories.get(category, 0) + 1
            components.add(component)
        
        return {
            'total_errors': len(analyses),
            'severity_distribution': severities,
            'error_category_distribution': categories,
            'affected_components': list(components),
            'detailed_analyses': analyses,
            'critical_count': severities.get('Critical', 0),
            'high_count': severities.get('High', 0)
        }

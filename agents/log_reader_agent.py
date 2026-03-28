"""Log Reader Agent

This agent reads and parses log files, extracting error information,
timestamps, and relevant context.

Usage:
    from agents.log_reader_agent import LogReaderAgent
    
    reader = LogReaderAgent()
    logs = reader.read_log_file('path/to/logfile.log')
    errors = reader.extract_errors(logs)
"""

import os
import re
from typing import List, Dict, Any, Optional
from datetime import datetime
import json


class LogReaderAgent:
    """Reads and parses log files to extract errors and context."""
    
    def __init__(self):
        """Initialize the log reader agent."""
        self.supported_formats = ['.log', '.txt', '.json']
        self.error_patterns = {
            'error': r'(?i)(error|exception|failed|failure|fatal)',
            'warning': r'(?i)(warning|warn)',
            'traceback': r'(?i)(traceback|stack trace)',
            'timestamp': r'(\d{4}-\d{2}-\d{2}|\d{2}:\d{2}:\d{2})',
        }
    
    def read_log_file(self, file_path: str) -> List[str]:
        """
        Read a log file and return its contents as a list of lines.
        
        Args:
            file_path: Path to the log file
            
        Returns:
            List of log lines
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Log file not found: {file_path}")
        
        file_ext = os.path.splitext(file_path)[1].lower()
        if file_ext not in self.supported_formats:
            raise ValueError(f"Unsupported file format: {file_ext}")
        
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                lines = f.readlines()
            return lines
        except Exception as e:
            raise Exception(f"Error reading log file: {str(e)}")
    
    def extract_errors(self, logs: List[str]) -> List[Dict[str, Any]]:
        """
        Extract error entries from logs.
        
        Args:
            logs: List of log lines
            
        Returns:
            List of error dictionaries with context
        """
        errors = []
        
        for idx, line in enumerate(logs):
            if re.search(self.error_patterns['error'], line):
                error_entry = {
                    'line_number': idx + 1,
                    'message': line.strip(),
                    'type': self._identify_error_type(line),
                    'timestamp': self._extract_timestamp(line),
                    'context': self._get_context(logs, idx)
                }
                errors.append(error_entry)
        
        return errors
    
    def _identify_error_type(self, line: str) -> str:
        """Identify the type of error."""
        if 'exception' in line.lower():
            return 'Exception'
        elif 'fatal' in line.lower():
            return 'Fatal'
        elif 'traceback' in line.lower():
            return 'Traceback'
        else:
            return 'Error'
    
    def _extract_timestamp(self, line: str) -> Optional[str]:
        """Extract timestamp from log line."""
        match = re.search(self.error_patterns['timestamp'], line)
        return match.group(0) if match else None
    
    def _get_context(self, logs: List[str], error_idx: int, context_lines: int = 2) -> Dict[str, Any]:
        """Get context around the error line."""
        start = max(0, error_idx - context_lines)
        end = min(len(logs), error_idx + context_lines + 1)
        
        return {
            'before': [logs[i].strip() for i in range(start, error_idx)],
            'error': logs[error_idx].strip(),
            'after': [logs[i].strip() for i in range(error_idx + 1, end)]
        }
    
    def extract_warnings(self, logs: List[str]) -> List[Dict[str, Any]]:
        """
        Extract warning entries from logs.
        
        Args:
            logs: List of log lines
            
        Returns:
            List of warning dictionaries
        """
        warnings = []
        
        for idx, line in enumerate(logs):
            if re.search(self.error_patterns['warning'], line) and \
               not re.search(self.error_patterns['error'], line):
                warning_entry = {
                    'line_number': idx + 1,
                    'message': line.strip(),
                    'timestamp': self._extract_timestamp(line),
                }
                warnings.append(warning_entry)
        
        return warnings
    
    def get_error_summary(self, log_file_path: str) -> Dict[str, Any]:
        """
        Get a comprehensive summary of errors and warnings in a log file.
        
        Args:
            log_file_path: Path to the log file
            
        Returns:
            Dictionary containing summary statistics and detailed errors
        """
        logs = self.read_log_file(log_file_path)
        errors = self.extract_errors(logs)
        warnings = self.extract_warnings(logs)
        
        return {
            'file': log_file_path,
            'total_lines': len(logs),
            'error_count': len(errors),
            'warning_count': len(warnings),
            'errors': errors,
            'warnings': warnings,
            'most_recent_error': errors[-1] if errors else None
        }

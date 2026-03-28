s# Multi-Agent Log Analyzer - Quick Start Guide

## 5-Minute Setup

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Set Up API Key
Create `.env` file in the project root:
```
OPENROUTER_API_KEY=your_key_here
```

Get free API key at: https://openrouter.ai

### 3. Run Interactive Mode
```bash
python log_analyzer.py
```

## Common Use Cases

### 📋 Analyze Your Log File
```bash
python log_analyzer.py --file your_logs.log
```

Output:
- Summary of errors found
- Error categories and severity
- Affected components
- Recommended actions

### 🔍 Understand a Single Error
```bash
python log_analyzer.py --error "Database connection timeout"
```

Returns:
- Error severity and category
- Root cause analysis
- Step-by-step solutions
- Prevention tips

### 🧪 Test the System
```bash
python test_multi_agent.py
```

## What Each Agent Does

| Agent | Purpose | Output |
|-------|---------|--------|
| **LogReaderAgent** | Reads log files and extracts errors with context | List of errors with line numbers |
| **ErrorAnalyzerAgent** | Analyzes error patterns and determines severity | Detailed analysis with severity, category, component |
| **SolutionProviderAgent** | Provides expert solutions based on 10+ years experience | Immediate actions, detailed solutions, prevention |
| **Orchestrator** | Coordinates all agents for complete pipeline | Final comprehensive report |

## Example Workflow

### In Python Code
```python
from agents.multi_agent_orchestrator import MultiAgentOrchestrator

# Initialize orchestrator
orchestrator = MultiAgentOrchestrator()

# Analyze log file
report = orchestrator.analyze_and_solve('app.log')

# Print summary
orchestrator.print_summary(report)

# Save detailed report
orchestrator.export_report(report, 'analysis.json')
```

### From Command Line
```bash
# Interactive analysis
python log_analyzer.py

# Quick file analysis
python log_analyzer.py --file application.log

# Single error analysis
python log_analyzer.py --error "Connection refused"
```

## Understanding the Output

### Executive Summary
```
📊 SUMMARY:
   Total Errors:         5
   Total Warnings:       3
   Critical Issues:      1
   High Priority Issues: 1

⚠️  ERROR CATEGORIES:
   - CONNECTION: 2
   - DATABASE: 1
   - RESOURCE: 2

🏗️  AFFECTED COMPONENTS:
   - Database Layer
   - API/Network Layer
   - System Resources

📋 RECOMMENDATION:
   🔴 CRITICAL: Immediate attention required.
```

### Per-Error Solution
```
💡 Solution:
   Immediate Actions:
     1. Check database connection parameters
     2. Verify database service is running
     3. Review connection retry logic

🛡️ Prevention Strategy:
   Use connection pooling and implement query optimization

🔄 Root Cause Clues:
   - Resource not found - check configuration
   - Configuration issue may have triggered this error
```

## Example Log File Format

The system works with standard log formats:

```
[2024-03-28 10:15:23] INFO Starting application
[2024-03-28 10:15:25] INFO Configuration loaded
[2024-03-28 10:16:42] ERROR Failed to connect to database at localhost:5432
[2024-03-28 10:16:42] ERROR java.sql.SQLException: Connection refused
[2024-03-28 10:16:43] WARNING Retrying connection attempt 1/3
```

## Supported Error Types

The system automatically recognizes and handles:

- **Connection Errors** - Network, timeouts, refused connections
- **Database Errors** - SQL errors, connection pool issues
- **Authentication Errors** - Permission denied, invalid tokens
- **File System Errors** - File not found, permission issues
- **Resource Errors** - Memory, CPU, disk space
- **Parsing Errors** - JSON/XML format issues
- **Performance Issues** - Slow operations, timeouts
- **Dependency Errors** - Import/module issues

## Sample Output File

When you save a report, you get detailed JSON:

```json
{
  "metadata": {
    "timestamp": "2024-03-28T10:20:00",
    "log_file": "app.log",
    "pipeline_status": "COMPLETED"
  },
  "executive_summary": {
    "total_errors": 5,
    "critical_issues": 1,
    "recommended_action": "🔴 CRITICAL: Immediate attention required"
  },
  "solutions": {
    "high_priority_items": [
      {
        "severity": "Critical",
        "error_category": "CONNECTION",
        "immediate_actions": [
          "Check network connectivity",
          "Verify service endpoints",
          "Review firewall rules"
        ]
      }
    ]
  }
}
```

## Tips & Tricks

### 💡 Better Results
1. **Use consistent log format** - Timestamps and ERROR keywords help
2. **Provide context** - Include stack traces in logs
3. **Save reports** - Export JSON for archival and tracking
4. **Run regularly** - Monitor logs in production

### ⚡ Speed Up Analysis
```bash
# Analyze multiple files
for file in logs/*.log; do
  python log_analyzer.py --file "$file"
done
```

### 📊 Create Automation
```python
import os
from agents.multi_agent_orchestrator import MultiAgentOrchestrator

orchestrator = MultiAgentOrchestrator()

# Analyze all logs in directory
log_dir = 'logs/'
for log_file in os.listdir(log_dir):
    if log_file.endswith('.log'):
        report = orchestrator.analyze_and_solve(f'{log_dir}{log_file}')
        orchestrator.export_report(report, f'{log_file}_analysis.json')
```

## Troubleshooting

### ❌ "OPENROUTER_API_KEY not found"
```bash
# Make sure .env file exists
cat .env
# Should show: OPENROUTER_API_KEY=your_key_here
```

### ❌ "File not found"
```bash
# Use full path or check the file exists
python log_analyzer.py --file C:/full/path/to/logs.log
```

### ❌ "No errors detected"
```bash
# Ensure logs contain ERROR, EXCEPTION, or FAILED keywords
# Check log file format matches standard patterns
# View test file: cat example_logs.log
```

## Next Steps

1. ✅ Try with `example_logs.log` first
2. ✅ Analyze your own log files
3. ✅ Integrate into your monitoring pipeline
4. ✅ Customize error patterns for your application
5. ✅ Set up automated daily analysis

## Resources

- 📖 Full documentation: `README_MULTI_AGENT.md`
- 🧪 Test suite: `test_multi_agent.py`
- 📝 Example log: `example_logs.log`
- 🤖 Source code: `agents/`

---

Ready to analyze logs intelligently! 🚀

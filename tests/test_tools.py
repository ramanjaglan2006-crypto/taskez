import pytest
from taskez.tools.web_search import WebSearchTool
from taskez.tools.code_executor import CodeCalculatorTool
from taskez.tools.github_tool import GitHubAnalyzerTool
from taskez.tools.report_generator import ReportGeneratorTool

def test_web_search_tool():
    tool = WebSearchTool()
    res = tool.execute(query="Python programming language")
    assert res.success is True
    assert res.output["results_count"] > 0

def test_code_calculator_tool():
    tool = CodeCalculatorTool()
    res = tool.execute(expression="100 - (15 + 25) + sum([10, 20])")
    assert res.success is True
    assert res.output["result"] == 90

def test_code_calculator_security_check():
    tool = CodeCalculatorTool()
    res = tool.execute(expression="import os; os.system('ls')")
    assert res.success is False
    assert "Forbidden statement" in res.error

def test_github_analyzer_tool():
    tool = GitHubAnalyzerTool()
    res = tool.execute(repo_url="https://github.com/fastapi/fastapi")
    assert res.success is True
    assert "quality_score" in res.output

def test_report_generator_tool():
    tool = ReportGeneratorTool()
    sections = [{"heading": "Summary", "content": "Test content", "bullets": ["Point A", "Point B"]}]
    res = tool.execute(title="Test Title", goal="Test Goal", key_sections=sections)
    assert res.success is True
    assert "Test Title" in res.output["markdown_report"]

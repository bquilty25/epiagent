"""Tests for GitIngest wrapper functionality."""

import asyncio
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from epiagent.tools.gitingest_wrapper import (
    GitIngestResult,
    batch_ingest_repositories,
    batch_ingest_repositories_async,
    ingest_repository,
    ingest_repository_async,
)


class TestGitIngestResult:
    """Test GitIngestResult data class."""
    
    def test_gitingest_result_creation(self):
        """Test creating a GitIngestResult instance."""
        result = GitIngestResult(
            summary="Repository: test/repo\nFiles analyzed: 5\nEstimated tokens: 1.2k",
            tree="Directory structure:\n└── test-repo/\n    └── README.md",
            content="================================================\nFILE: README.md\n================================================\n# Test",
            repository_url="https://github.com/test/repo",
            files_analyzed=5,
            estimated_tokens=1200,
        )
        
        assert result.repository_url == "https://github.com/test/repo"
        assert result.files_analyzed == 5
        assert result.estimated_tokens == 1200
    
    def test_to_dict(self):
        """Test converting GitIngestResult to dictionary."""
        result = GitIngestResult(
            summary="Repository: test/repo",
            tree="Directory structure:",
            content="File content",
            repository_url="https://github.com/test/repo",
            files_analyzed=1,
            estimated_tokens=100,
        )
        
        data = result.to_dict()
        assert data["repository_url"] == "https://github.com/test/repo"
        assert data["files_analyzed"] == 1
        assert data["estimated_tokens"] == 100
        assert "summary" in data
        assert "tree" in data
        assert "content" in data
    
    def test_get_full_context(self):
        """Test getting full formatted context."""
        result = GitIngestResult(
            summary="Repository: test/repo",
            tree="Directory structure:",
            content="File content",
            repository_url="https://github.com/test/repo",
            files_analyzed=1,
            estimated_tokens=100,
        )
        
        context = result.get_full_context()
        assert "Repository: test/repo" in context
        assert "Directory structure:" in context
        assert "File content" in context


class TestIngestRepository:
    """Test ingest_repository function."""
    
    @patch('epiagent.tools.gitingest_wrapper.ingest')
    def test_ingest_repository_success(self, mock_ingest):
        """Test successful repository ingestion."""
        # Mock gitingest response
        mock_ingest.return_value = (
            "Repository: test/repo\nFiles analyzed: 3\nEstimated tokens: 1.5k",
            "Directory structure:\n└── test-repo/\n    └── README.md",
            "================================================\nFILE: README.md\n================================================\n# Test",
        )
        
        result = ingest_repository("https://github.com/test/repo")
        
        assert result.status == "success"
        assert result.data is not None
        assert result.data["repository_url"] == "https://github.com/test/repo"
        assert result.data["files_analyzed"] == 3
        assert result.data["estimated_tokens"] == 1500
        mock_ingest.assert_called_once_with("https://github.com/test/repo")
    
    @patch('epiagent.tools.gitingest_wrapper.ingest')
    def test_ingest_repository_with_parameters(self, mock_ingest):
        """Test repository ingestion with filtering parameters."""
        mock_ingest.return_value = ("", "", "")
        
        ingest_repository(
            "https://github.com/test/repo",
            include_patterns=["*.py", "*.md"],
            exclude_patterns=["*.log"],
            max_file_size=1024,
            branch="main",
            token="ghp_token",
        )
        
        mock_ingest.assert_called_once_with(
            "https://github.com/test/repo",
            include_patterns=["*.py", "*.md"],
            exclude_patterns=["*.log"],
            max_file_size=1024,
            branch="main",
            token="ghp_token",
        )
    
    @patch('epiagent.tools.gitingest_wrapper.ingest')
    def test_ingest_repository_with_output_path(self, mock_ingest, tmp_path):
        """Test repository ingestion with output file."""
        mock_ingest.return_value = (
            "Repository: test/repo\nFiles analyzed: 1\nEstimated tokens: 100",
            "Directory structure:",
            "File content",
        )
        
        output_file = tmp_path / "test_digest.txt"
        result = ingest_repository(
            "https://github.com/test/repo",
            output_path=output_file,
        )
        
        assert result.status == "success"
        assert result.artifact_path == output_file
        assert output_file.exists()
        assert "Repository: test/repo" in output_file.read_text()
    
    @patch('epiagent.tools.gitingest_wrapper.ingest')
    def test_ingest_repository_error(self, mock_ingest):
        """Test repository ingestion error handling."""
        mock_ingest.side_effect = Exception("Network error")
        
        result = ingest_repository("https://github.com/test/repo")
        
        assert result.status == "error"
        assert "Network error" in result.message
        assert result.data is None


class TestIngestRepositoryAsync:
    """Test ingest_repository_async function."""
    
    @pytest.mark.asyncio
    @patch('epiagent.tools.gitingest_wrapper.ingest_async')
    async def test_ingest_repository_async_success(self, mock_ingest_async):
        """Test successful async repository ingestion."""
        mock_ingest_async.return_value = (
            "Repository: test/repo\nFiles analyzed: 2\nEstimated tokens: 800",
            "Directory structure:",
            "File content",
        )
        
        result = await ingest_repository_async("https://github.com/test/repo")
        
        assert result.status == "success"
        assert result.data is not None
        assert result.data["files_analyzed"] == 2
        assert result.data["estimated_tokens"] == 800
        mock_ingest_async.assert_called_once_with("https://github.com/test/repo")
    
    @pytest.mark.asyncio
    @patch('epiagent.tools.gitingest_wrapper.ingest_async')
    async def test_ingest_repository_async_error(self, mock_ingest_async):
        """Test async repository ingestion error handling."""
        mock_ingest_async.side_effect = Exception("Async error")
        
        result = await ingest_repository_async("https://github.com/test/repo")
        
        assert result.status == "error"
        assert "Async error" in result.message


class TestBatchIngestRepositories:
    """Test batch_ingest_repositories function."""
    
    @patch('epiagent.tools.gitingest_wrapper.ingest')
    def test_batch_ingest_success(self, mock_ingest):
        """Test successful batch ingestion."""
        mock_ingest.return_value = (
            "Repository: test/repo\nFiles analyzed: 1\nEstimated tokens: 100",
            "Directory structure:",
            "File content",
        )
        
        urls = [
            "https://github.com/test/repo1",
            "https://github.com/test/repo2",
        ]
        
        result = batch_ingest_repositories(urls)
        
        assert result.status == "success"
        assert result.data["total_repositories"] == 2
        assert result.data["successful_count"] == 2
        assert result.data["error_count"] == 0
        assert len(result.data["successful_ingests"]) == 2
        assert len(result.data["errors"]) == 0
    
    @patch('epiagent.tools.gitingest_wrapper.ingest')
    def test_batch_ingest_with_errors(self, mock_ingest):
        """Test batch ingestion with some errors."""
        def side_effect(url):
            if "error" in url:
                raise Exception("Test error")
            return ("", "", "")
        
        mock_ingest.side_effect = side_effect
        
        urls = [
            "https://github.com/test/repo1",
            "https://github.com/test/error-repo",
        ]
        
        result = batch_ingest_repositories(urls)
        
        assert result.status == "partial"
        assert result.data["total_repositories"] == 2
        assert result.data["successful_count"] == 1
        assert result.data["error_count"] == 1
        assert len(result.data["successful_ingests"]) == 1
        assert len(result.data["errors"]) == 1
    
    @patch('epiagent.tools.gitingest_wrapper.ingest')
    def test_batch_ingest_with_output_dir(self, mock_ingest, tmp_path):
        """Test batch ingestion with output directory."""
        mock_ingest.return_value = (
            "Repository: test/repo\nFiles analyzed: 1\nEstimated tokens: 100",
            "Directory structure:",
            "File content",
        )
        
        urls = ["https://github.com/test/repo1"]
        result = batch_ingest_repositories(urls, output_dir=tmp_path)
        
        assert result.status == "success"
        # Check that output file was created
        output_files = list(tmp_path.glob("*_digest.txt"))
        assert len(output_files) == 1


class TestBatchIngestRepositoriesAsync:
    """Test batch_ingest_repositories_async function."""
    
    @pytest.mark.asyncio
    @patch('epiagent.tools.gitingest_wrapper.ingest_async')
    async def test_batch_ingest_async_success(self, mock_ingest_async):
        """Test successful async batch ingestion."""
        mock_ingest_async.return_value = (
            "Repository: test/repo\nFiles analyzed: 1\nEstimated tokens: 100",
            "Directory structure:",
            "File content",
        )
        
        urls = [
            "https://github.com/test/repo1",
            "https://github.com/test/repo2",
        ]
        
        result = await batch_ingest_repositories_async(urls)
        
        assert result.status == "success"
        assert result.data["total_repositories"] == 2
        assert result.data["successful_count"] == 2
        assert result.data["error_count"] == 0
    
    @pytest.mark.asyncio
    @patch('epiagent.tools.gitingest_wrapper.ingest_async')
    async def test_batch_ingest_async_with_concurrency_limit(self, mock_ingest_async):
        """Test async batch ingestion with concurrency control."""
        mock_ingest_async.return_value = ("", "", "")
        
        urls = ["https://github.com/test/repo"] * 10
        result = await batch_ingest_repositories_async(urls, max_concurrent=3)
        
        assert result.status == "success"
        assert result.data["total_repositories"] == 10
        assert result.data["successful_count"] == 10


class TestImportError:
    """Test import error handling when gitingest is not available."""
    
    @patch('epiagent.tools.gitingest_wrapper.ingest', None)
    def test_import_error_without_gitingest(self):
        """Test that ImportError is raised when gitingest is not available."""
        import sys
        import importlib
        from epiagent.tools import gitingest_wrapper
        
        with patch.dict('sys.modules', {'gitingest': None}):
            with pytest.raises(ImportError, match="gitingest is required"):
                importlib.reload(gitingest_wrapper)
        
        # Restore module for other tests
        importlib.reload(gitingest_wrapper)

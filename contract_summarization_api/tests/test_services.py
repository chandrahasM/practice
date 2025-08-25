import pytest
from app.services import ContractSummarizationService
from app.models import ContractInput, ContractSummary


class TestContractSummarizationService:
    """Test cases for ContractSummarizationService."""
    
    def test_extract_summary_first_sentence(self):
        """Test summary extraction when first sentence is short."""
        text = "This is the first sentence. This is the second sentence."
        summary = ContractSummarizationService.extract_summary(text)
        assert summary == "This is the first sentence."
    
    def test_extract_summary_long_first_sentence(self):
        """Test summary extraction when first sentence is longer than 25 words."""
        text = "This is a very long first sentence that contains more than twenty-five words and should be truncated appropriately to maintain readability and conciseness in the summary output. This is the second sentence."
        summary = ContractSummarizationService.extract_summary(text)
        # Should be truncated to first 25 words + "..."
        expected_words = text.split('.')[0].split()[:25]
        expected_summary = ' '.join(expected_words) + '...'
        assert summary == expected_summary
    
    def test_extract_summary_no_sentence_ending(self):
        """Test summary extraction when text has no sentence endings."""
        text = "This text has no sentence endings so it should be truncated to first 25 words"
        summary = ContractSummarizationService.extract_summary(text)
        words = text.split()
        if len(words) <= 25:
            assert summary == text
        else:
            expected_summary = ' '.join(words[:25]) + '...'
            assert summary == expected_summary
    
    def test_extract_summary_exclamation_mark(self):
        """Test summary extraction with exclamation mark ending."""
        text = "This is exciting! This is the second sentence."
        summary = ContractSummarizationService.extract_summary(text)
        assert summary == "This is exciting!"
    
    def test_extract_summary_question_mark(self):
        """Test summary extraction with question mark ending."""
        text = "What is this contract about? This explains the details."
        summary = ContractSummarizationService.extract_summary(text)
        assert summary == "What is this contract about?"
    
    def test_extract_summary_multiple_sentence_endings(self):
        """Test summary extraction with multiple sentence endings, should pick the first."""
        text = "First sentence. Second sentence! Third sentence?"
        summary = ContractSummarizationService.extract_summary(text)
        assert summary == "First sentence."
    
    def test_extract_summary_empty_text(self):
        """Test summary extraction with empty text."""
        text = ""
        summary = ContractSummarizationService.extract_summary(text)
        assert summary == ""
    
    def test_extract_summary_whitespace_only(self):
        """Test summary extraction with whitespace-only text."""
        text = "   \n\t   "
        summary = ContractSummarizationService.extract_summary(text)
        assert summary == ""
    
    def test_extract_summary_single_word(self):
        """Test summary extraction with single word."""
        text = "Agreement"
        summary = ContractSummarizationService.extract_summary(text)
        assert summary == "Agreement"
    
    def test_extract_summary_exactly_25_words(self):
        """Test summary extraction with exactly 25 words."""
        words = [f"word{i}" for i in range(25)]
        text = " ".join(words) + ". Additional text here."
        summary = ContractSummarizationService.extract_summary(text)
        expected_summary = " ".join(words) + "."
        assert summary == expected_summary
    
    def test_extract_summary_26_words(self):
        """Test summary extraction with 26 words."""
        words = [f"word{i}" for i in range(26)]
        text = " ".join(words) + ". Additional text here."
        summary = ContractSummarizationService.extract_summary(text)
        expected_summary = " ".join(words[:25]) + "..."
        assert summary == expected_summary


class TestSummarizeContracts:
    """Test cases for batch contract summarization."""
    
    def test_summarize_single_contract(self):
        """Test summarizing a single contract."""
        contracts = [
            ContractInput(
                contract_id="CONTRACT_001",
                text="This is a single contract to summarize."
            )
        ]
        
        summaries = ContractSummarizationService.summarize_contracts(contracts)
        
        assert len(summaries) == 1
        assert summaries[0].contract_id == "CONTRACT_001"
        assert summaries[0].summary == "This is a single contract to summarize."
    
    def test_summarize_multiple_contracts(self):
        """Test summarizing multiple contracts."""
        contracts = [
            ContractInput(
                contract_id="CONTRACT_001",
                text="First contract text."
            ),
            ContractInput(
                contract_id="CONTRACT_002",
                text="Second contract text."
            ),
            ContractInput(
                contract_id="CONTRACT_003",
                text="Third contract text."
            )
        ]
        
        summaries = ContractSummarizationService.summarize_contracts(contracts)
        
        assert len(summaries) == 3
        assert summaries[0].contract_id == "CONTRACT_001"
        assert summaries[1].contract_id == "CONTRACT_002"
        assert summaries[2].contract_id == "CONTRACT_003"
        assert summaries[0].summary == "First contract text."
        assert summaries[1].summary == "Second contract text."
        assert summaries[2].summary == "Third contract text."
    
    def test_summarize_contracts_with_errors(self):
        """Test that processing continues even if individual contracts fail."""
        contracts = [
            ContractInput(
                contract_id="CONTRACT_001",
                text="Valid contract text."
            ),
            ContractInput(
                contract_id="CONTRACT_002",
                text="Another valid contract."
            )
        ]
        
        # Mock a failure scenario by temporarily modifying the service
        original_extract = ContractSummarizationService.extract_summary
        
        def mock_extract_with_failure(text):
            if "Another valid contract" in text:
                raise Exception("Simulated processing error")
            return original_extract(text)
        
        ContractSummarizationService.extract_summary = mock_extract_with_failure
        
        try:
            summaries = ContractSummarizationService.summarize_contracts(contracts)
            
            assert len(summaries) == 2
            assert summaries[0].contract_id == "CONTRACT_001"
            assert summaries[0].summary == "Valid contract text."
            assert summaries[1].contract_id == "CONTRACT_002"
            assert "Error processing contract" in summaries[1].summary
        finally:
            # Restore original method
            ContractSummarizationService.extract_summary = original_extract


class TestValidationMethods:
    """Test cases for validation methods."""
    
    def test_validate_contract_data_valid(self):
        """Test validation with valid contract data."""
        contracts = [
            ContractInput(
                contract_id="CONTRACT_001",
                text="Valid contract text."
            ),
            ContractInput(
                contract_id="CONTRACT_002",
                text="Another valid contract."
            )
        ]
        
        is_valid = ContractSummarizationService.validate_contract_data(contracts)
        assert is_valid is True
    
    def test_validate_contract_data_empty_list(self):
        """Test validation with empty contracts list."""
        contracts = []
        
        is_valid = ContractSummarizationService.validate_contract_data(contracts)
        assert is_valid is False
    
    def test_validate_contract_data_none_list(self):
        """Test validation with None contracts list."""
        contracts = None
        
        is_valid = ContractSummarizationService.validate_contract_data(contracts)
        assert is_valid is False
    
    def test_validate_contract_data_empty_contract_id(self):
        """Test validation with empty contract ID."""
        contracts = [
            ContractInput(
                contract_id="",
                text="Valid contract text."
            )
        ]
        
        is_valid = ContractSummarizationService.validate_contract_data(contracts)
        assert is_valid is False
    
    def test_validate_contract_data_empty_text(self):
        """Test validation with empty contract text."""
        contracts = [
            ContractInput(
                contract_id="CONTRACT_001",
                text=""
            )
        ]
        
        is_valid = ContractSummarizationService.validate_contract_data(contracts)
        assert is_valid is False


class TestEdgeCases:
    """Test cases for edge cases and boundary conditions."""
    
    def test_extract_summary_very_long_text(self):
        """Test summary extraction with very long text."""
        # Create text with 1000 words
        words = [f"word{i}" for i in range(1000)]
        text = " ".join(words) + ". End of text."
        
        summary = ContractSummarizationService.extract_summary(text)
        
        # Should be truncated to first 25 words + "..."
        expected_words = text.split('.')[0].split()[:25]
        expected_summary = ' '.join(expected_words) + '...'
        assert summary == expected_summary
    
    def test_extract_summary_special_characters(self):
        """Test summary extraction with special characters."""
        text = "Contract with special chars: @#$%^&*()_+-=[]{}|;':\",./<>?`~"
        summary = ContractSummarizationService.extract_summary(text)
        
        # Should handle special characters gracefully
        assert len(summary) > 0
        assert "Contract with special chars" in summary
    
    def test_extract_summary_unicode_text(self):
        """Test summary extraction with unicode text."""
        text = "Contrat en français avec des caractères spéciaux: é, à, ç, ñ, ü"
        summary = ContractSummarizationService.extract_summary(text)
        
        # Should handle unicode characters
        assert len(summary) > 0
        assert "Contrat en français" in summary
    
    def test_extract_summary_newlines_and_tabs(self):
        """Test summary extraction with newlines and tabs."""
        text = "First line.\nSecond line.\tThird line."
        summary = ContractSummarizationService.extract_summary(text)
        
        # Should extract first sentence correctly
        assert summary == "First line."

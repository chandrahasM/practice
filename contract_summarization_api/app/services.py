import logging
from typing import List
from .models import ContractInput, ContractSummary
import time

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ContractSummarizationService:
    """Service class for contract summarization business logic."""
    
    @staticmethod
    def extract_summary(text: str) -> str:
        """
        Extract a summary from contract text.
        
        This simulates AI summarization by extracting the first sentence
        or the first 25 words, whichever comes first.
        
        Args:
            text (str): The contract text to summarize
            
        Returns:
            str: The extracted summary
        """
        if not text:
            return ""
        
        # Find the first sentence (ends with ., !, or ?)
        sentence_endings = ['.', '!', '?']
        first_sentence_end = -1
        
        for ending in sentence_endings:
            pos = text.find(ending)
            if pos != -1 and (first_sentence_end == -1 or pos < first_sentence_end):
                first_sentence_end = pos
        
        if first_sentence_end != -1:
            # Extract first sentence
            first_sentence = text[:first_sentence_end + 1].strip()
            # Limit to first 25 words if sentence is too long
            words = first_sentence.split()
            if len(words) <= 25:
                return first_sentence
            else:
                return ' '.join(words[:25]) + '...'
        else:
            # No sentence ending found, extract first 25 words
            words = text.split()
            if len(words) <= 25:
                return text.strip()
            else:
                return ' '.join(words[:25]) + '...'
    
    @staticmethod
    def summarize_contracts(contracts: List[ContractInput]) -> List[ContractSummary]:
        """
        Summarize multiple contracts.
        
        Args:
            contracts (List[ContractInput]): List of contracts to summarize
            
        Returns:
            List[ContractSummary]: List of contract summaries
        """
        start_time = time.time()
        logger.info(f"Processing {len(contracts)} contracts")
        
        summaries = []
        for contract in contracts:
            try:
                summary_text = ContractSummarizationService.extract_summary(contract.text)
                summary = ContractSummary(
                    contract_id=contract.contract_id,
                    summary=summary_text
                )
                summaries.append(summary)
                
                logger.info(f"Successfully summarized contract {contract.contract_id}")
                
            except Exception as e:
                logger.error(f"Error processing contract {contract.contract_id}: {str(e)}")
                # Create a fallback summary
                fallback_summary = ContractSummary(
                    contract_id=contract.contract_id,
                    summary="Error processing contract - unable to generate summary"
                )
                summaries.append(fallback_summary)
        
        processing_time = time.time() - start_time
        logger.info(f"Completed processing {len(contracts)} contracts in {processing_time:.3f} seconds")
        
        return summaries
    
    @staticmethod
    def validate_contract_data(contracts: List[ContractInput]) -> bool:
        """
        Validate contract data before processing.
        
        Args:
            contracts (List[ContractInput]): List of contracts to validate
            
        Returns:
            bool: True if validation passes, False otherwise
        """
        if not contracts:
            return False
        
        for contract in contracts:
            if not contract.contract_id or not contract.contract_id.strip():
                return False
            if not contract.text or not contract.text.strip():
                return False
        
        return True

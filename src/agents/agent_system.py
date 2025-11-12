"""
Agent Orchestration System
Coordinates multiple agents to handle complex queries
"""

from typing import Dict, Any, List, Optional
import pandas as pd
from src.agents.base_agents import (
    BaseAgent, AgentType, AgentResponse,
    OrchestratorAgent, SQLAnalystAgent, DataAnalystAgent,
    KnowledgeExpertAgent, TranslatorAgent
)
from src.database import DatabaseManager
from src.memory import MemoryManager
from src.logger import get_logger

logger = get_logger(__name__)


class AgentSystem:
    """
    Coordinates multiple specialized agents to handle user queries
    """
    
    def __init__(self, db_manager: DatabaseManager, memory_manager: MemoryManager):
        self.db_manager = db_manager
        self.memory_manager = memory_manager
        
        # Initialize agents
        self.agents: Dict[AgentType, BaseAgent] = {
            AgentType.ORCHESTRATOR: OrchestratorAgent(),
            AgentType.SQL_ANALYST: SQLAnalystAgent(db_manager),
            AgentType.DATA_ANALYST: DataAnalystAgent(),
            AgentType.KNOWLEDGE_EXPERT: KnowledgeExpertAgent(),
            AgentType.TRANSLATOR: TranslatorAgent(),
        }
        
        logger.info(f"Agent system initialized with {len(self.agents)} agents")
    
    def process_query(self, user_query: str) -> Dict[str, Any]:
        """
        Process user query through the agent system
        
        Args:
            user_query: User's natural language query
            
        Returns:
            Dictionary with response and metadata
        """
        logger.info(f"Processing query: {user_query[:100]}")
        
        # Add user message to memory
        self.memory_manager.add_message('user', user_query)
        
        try:
            # Determine query intent and route to appropriate agents
            intent = self._classify_query(user_query)
            
            # Execute appropriate workflow
            if intent == 'data_query':
                response = self._handle_data_query(user_query)
            elif intent == 'translation':
                response = self._handle_translation(user_query)
            elif intent == 'knowledge':
                response = self._handle_knowledge_query(user_query)
            else:
                response = self._handle_general_query(user_query)
            
            # Add assistant response to memory
            self.memory_manager.add_message('assistant', response['answer'])
            
            return response
            
        except Exception as e:
            logger.error(f"Error processing query: {e}")
            error_response = {
                'answer': f"I encountered an error processing your query: {str(e)}",
                'metadata': {'error': str(e)},
                'success': False
            }
            self.memory_manager.add_message('assistant', error_response['answer'])
            return error_response
    
    def _classify_query(self, query: str) -> str:
        """Classify the type of query"""
        query_lower = query.lower()
        
        # Simple keyword-based classification
        translation_keywords = ['translate', 'translation', 'in portuguese', 'in english', 'in spanish']
        if any(keyword in query_lower for keyword in translation_keywords):
            return 'translation'
        
        knowledge_keywords = ['what is', 'define', 'explain', 'tell me about', 'how does']
        if any(keyword in query_lower for keyword in knowledge_keywords) and \
           not any(word in query_lower for word in ['data', 'orders', 'customers', 'products', 'sales']):
            return 'knowledge'
        
        # Default to data query if it mentions data-related terms
        data_keywords = ['orders', 'customers', 'products', 'sales', 'revenue', 'category', 'seller']
        if any(keyword in query_lower for keyword in data_keywords):
            return 'data_query'
        
        return 'general'
    
    def _handle_data_query(self, query: str) -> Dict[str, Any]:
        """Handle data-related queries"""
        logger.info("Handling data query")
        
        # Step 1: Generate and execute SQL
        sql_response = self.agents[AgentType.SQL_ANALYST].execute(query)
        
        if not sql_response.success:
            return {
                'answer': f"I couldn't generate a valid SQL query. Error: {sql_response.error}",
                'metadata': {'error': sql_response.error},
                'success': False
            }
        
        result_df = sql_response.metadata.get('result')
        sql_query = sql_response.metadata.get('sql_query')
        
        if result_df is None or result_df.empty:
            return {
                'answer': "The query executed successfully but returned no results.",
                'sql_query': sql_query,
                'data': None,
                'metadata': {},
                'success': True
            }
        
        # Step 2: Analyze results
        analysis_response = self.agents[AgentType.DATA_ANALYST].execute(
            query,
            context={'result_df': result_df, 'sql_query': sql_query}
        )
        
        analysis = analysis_response.content if analysis_response.success else "Analysis not available."
        
        # Format response
        answer_parts = [
            f"**Analysis:**\n{analysis}",
            f"\n**Query Details:**",
            f"- Returned {len(result_df)} rows",
            f"- SQL Query: `{sql_query}`"
        ]
        
        return {
            'answer': '\n'.join(answer_parts),
            'sql_query': sql_query,
            'data': result_df,
            'analysis': analysis,
            'metadata': {
                'row_count': len(result_df),
                'columns': result_df.columns.tolist()
            },
            'success': True
        }
    
    def _handle_translation(self, query: str) -> Dict[str, Any]:
        """Handle translation requests"""
        logger.info("Handling translation query")
        
        # Extract target language and text from query
        # This is simplified - could be more sophisticated
        target_lang = 'English'
        if 'portuguese' in query.lower():
            target_lang = 'Portuguese'
        elif 'spanish' in query.lower():
            target_lang = 'Spanish'
        
        translation_response = self.agents[AgentType.TRANSLATOR].execute(
            query,
            context={'target_language': target_lang}
        )
        
        if translation_response.success:
            return {
                'answer': translation_response.content,
                'metadata': {'target_language': target_lang},
                'success': True
            }
        else:
            return {
                'answer': f"Translation failed: {translation_response.error}",
                'metadata': {},
                'success': False
            }
    
    def _handle_knowledge_query(self, query: str) -> Dict[str, Any]:
        """Handle knowledge-based queries"""
        logger.info("Handling knowledge query")
        
        knowledge_response = self.agents[AgentType.KNOWLEDGE_EXPERT].execute(query)
        
        if knowledge_response.success:
            return {
                'answer': knowledge_response.content,
                'metadata': {},
                'success': True
            }
        else:
            return {
                'answer': f"Knowledge lookup failed: {knowledge_response.error}",
                'metadata': {},
                'success': False
            }
    
    def _handle_general_query(self, query: str) -> Dict[str, Any]:
        """Handle general queries"""
        logger.info("Handling general query")
        
        # Use knowledge expert for general queries
        return self._handle_knowledge_query(query)
    
    def get_conversation_history(self) -> List[Dict[str, str]]:
        """Get formatted conversation history"""
        messages = self.memory_manager.get_messages()
        return [
            {
                'role': msg.role,
                'content': msg.content,
                'timestamp': msg.timestamp.isoformat()
            }
            for msg in messages
        ]

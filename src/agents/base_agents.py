"""
Multi-Agent System for E-Commerce Insights
Implements specialized agents for different tasks
"""

import google.generativeai as genai
from typing import Dict, Any, List, Optional, Tuple
from enum import Enum
from dataclasses import dataclass
import time
from src.config import config
from src.logger import get_logger
from src.database import DatabaseManager
from src.memory import MemoryManager

logger = get_logger(__name__)

# Configure Gemini
genai.configure(api_key=config.llm.gemini_api_key)


class AgentType(Enum):
    """Types of specialized agents"""
    ORCHESTRATOR = "orchestrator"
    SQL_ANALYST = "sql_analyst"
    DATA_ANALYST = "data_analyst"
    KNOWLEDGE_EXPERT = "knowledge_expert"
    TRANSLATOR = "translator"
    VISUALIZER = "visualizer"


@dataclass
class AgentResponse:
    """Response from an agent"""
    agent_type: AgentType
    content: str
    metadata: Dict[str, Any]
    success: bool
    error: Optional[str] = None


class BaseAgent:
    """Base class for all agents"""
    
    def __init__(self, agent_type: AgentType, system_prompt: str):
        self.agent_type = agent_type
        self.system_prompt = system_prompt
        self.model = genai.GenerativeModel(
            model_name=config.llm.default_model,
            generation_config={
                'temperature': config.llm.temperature,
                'max_output_tokens': config.llm.max_tokens,
            }
        )
    
    def execute(self, query: str, context: Optional[Dict] = None) -> AgentResponse:
        """Execute agent task"""
        raise NotImplementedError("Subclasses must implement execute method")
    
    def _call_llm(self, prompt: str, max_retries: int = 3) -> str:
        """Call LLM with prompt and automatic retry on rate limits"""
        for attempt in range(max_retries):
            try:
                response = self.model.generate_content(prompt)
                return response.text
            except Exception as e:
                error_msg = str(e)
                
                # Check if it's a rate limit error (429)
                if "429" in error_msg or "Resource exhausted" in error_msg:
                    if attempt < max_retries - 1:
                        # Exponential backoff: 2, 4, 8 seconds
                        wait_time = 2 ** (attempt + 1)
                        logger.warning(f"Rate limit hit. Retrying in {wait_time} seconds... (Attempt {attempt + 1}/{max_retries})")
                        time.sleep(wait_time)
                        continue
                    else:
                        logger.error(f"Rate limit exceeded after {max_retries} attempts")
                        raise Exception("⏳ API rate limit exceeded. Please wait a moment and try again.")
                else:
                    # Other errors, don't retry
                    logger.error(f"LLM call failed: {e}")
                    raise
        
        raise Exception("Failed to get response from AI model")


class OrchestratorAgent(BaseAgent):
    """
    Orchestrator Agent - Routes queries to appropriate specialized agents
    """
    
    def __init__(self):
        system_prompt = """You are an intelligent orchestrator for an e-commerce analytics system.
Your job is to understand user queries and determine which specialized agents should handle them.

Available agents:
1. SQL_ANALYST - Generates and executes SQL queries on e-commerce database
2. DATA_ANALYST - Performs statistical analysis and insights on query results
3. KNOWLEDGE_EXPERT - Provides external knowledge about products, markets, trends
4. TRANSLATOR - Translates text between languages
5. VISUALIZER - Creates charts and visualizations

Analyze the user query and respond in JSON format:
{
    "primary_agent": "agent_name",
    "secondary_agents": ["agent1", "agent2"],
    "reasoning": "why these agents were chosen",
    "requires_database": true/false
}"""
        super().__init__(AgentType.ORCHESTRATOR, system_prompt)
    
    def execute(self, query: str, context: Optional[Dict] = None) -> AgentResponse:
        """Route query to appropriate agents"""
        try:
            prompt = f"{self.system_prompt}\n\nUser Query: {query}"
            response = self._call_llm(prompt)
            
            return AgentResponse(
                agent_type=self.agent_type,
                content=response,
                metadata={'query': query},
                success=True
            )
        except Exception as e:
            return AgentResponse(
                agent_type=self.agent_type,
                content="",
                metadata={},
                success=False,
                error=str(e)
            )


class SQLAnalystAgent(BaseAgent):
    """
    SQL Analyst Agent - Generates and executes SQL queries
    """
    
    def __init__(self, db_manager: DatabaseManager):
        system_prompt = """You are an expert SQL analyst specializing in e-commerce data analysis.
Your job is to generate accurate, efficient SQL queries for DuckDB based on user questions.

Guidelines:
1. Use proper JOIN operations when combining tables
2. Include appropriate WHERE clauses for filtering
3. Use aggregate functions (COUNT, SUM, AVG) for analytics
4. Format dates properly
5. Limit results to reasonable sizes
6. Add comments explaining complex queries
7. Only use SELECT statements - never modify data

Return ONLY the SQL query without any explanation or markdown formatting."""
        super().__init__(AgentType.SQL_ANALYST, system_prompt)
        self.db_manager = db_manager
    
    def execute(self, query: str, context: Optional[Dict] = None) -> AgentResponse:
        """Generate and execute SQL query"""
        try:
            # Get schema information
            schema_desc = self.db_manager.get_schema_description()
            
            prompt = f"""{self.system_prompt}

Database Schema:
{schema_desc}

User Question: {query}

Generate the SQL query:"""
            
            # Get SQL query from LLM
            sql_query = self._call_llm(prompt).strip()
            
            # Clean up the SQL query
            sql_query = sql_query.replace('```sql', '').replace('```', '').strip()
            
            logger.info(f"Generated SQL: {sql_query}")
            
            # Execute query
            result_df, error = self.db_manager.execute_query(sql_query)
            
            if error:
                return AgentResponse(
                    agent_type=self.agent_type,
                    content="",
                    metadata={'sql_query': sql_query},
                    success=False,
                    error=error
                )
            
            return AgentResponse(
                agent_type=self.agent_type,
                content=sql_query,
                metadata={
                    'sql_query': sql_query,
                    'result': result_df,
                    'row_count': len(result_df)
                },
                success=True
            )
            
        except Exception as e:
            logger.error(f"SQL Analyst error: {e}")
            return AgentResponse(
                agent_type=self.agent_type,
                content="",
                metadata={},
                success=False,
                error=str(e)
            )


class DataAnalystAgent(BaseAgent):
    """
    Data Analyst Agent - Analyzes query results and provides insights
    """
    
    def __init__(self):
        system_prompt = """You are an expert data analyst specializing in e-commerce analytics.
Your job is to analyze query results and provide clear, actionable insights.

Guidelines:
1. Identify key trends and patterns
2. Provide statistical summaries
3. Compare metrics across different dimensions
4. Highlight anomalies or interesting findings
5. Suggest follow-up questions or analyses
6. Use clear, non-technical language for business users

Be concise but thorough in your analysis."""
        super().__init__(AgentType.DATA_ANALYST, system_prompt)
    
    def execute(self, query: str, context: Optional[Dict] = None) -> AgentResponse:
        """Analyze data and provide insights"""
        try:
            result_df = context.get('result_df') if context else None
            sql_query = context.get('sql_query', '') if context else ''
            
            if result_df is None or result_df.empty:
                return AgentResponse(
                    agent_type=self.agent_type,
                    content="No data available to analyze.",
                    metadata={},
                    success=False,
                    error="No data provided"
                )
            
            # Prepare context for analysis
            data_summary = f"""
Query: {query}
SQL Query: {sql_query}

Data Shape: {result_df.shape[0]} rows, {result_df.shape[1]} columns
Columns: {', '.join(result_df.columns.tolist())}

Sample Data:
{result_df.head(10).to_string()}

Statistical Summary:
{result_df.describe().to_string() if len(result_df) > 0 else 'No numeric data'}
"""
            
            prompt = f"""{self.system_prompt}

{data_summary}

Provide your analysis and insights:"""
            
            analysis = self._call_llm(prompt)
            
            return AgentResponse(
                agent_type=self.agent_type,
                content=analysis,
                metadata={
                    'data_shape': result_df.shape,
                    'columns': result_df.columns.tolist()
                },
                success=True
            )
            
        except Exception as e:
            logger.error(f"Data Analyst error: {e}")
            return AgentResponse(
                agent_type=self.agent_type,
                content="",
                metadata={},
                success=False,
                error=str(e)
            )


class KnowledgeExpertAgent(BaseAgent):
    """
    Knowledge Expert Agent - Provides external knowledge and context
    """
    
    def __init__(self):
        system_prompt = """You are a knowledge expert in e-commerce, retail, and business analytics.
Your job is to provide additional context, industry insights, and external knowledge.

Guidelines:
1. Provide relevant industry benchmarks and standards
2. Explain e-commerce metrics and KPIs
3. Offer business context and interpretation
4. Suggest best practices
5. Provide definitions of technical terms
6. Share market trends and insights

Be informative and educational in your responses."""
        super().__init__(AgentType.KNOWLEDGE_EXPERT, system_prompt)
    
    def execute(self, query: str, context: Optional[Dict] = None) -> AgentResponse:
        """Provide knowledge and context"""
        try:
            prompt = f"""{self.system_prompt}

User Query: {query}

Provide relevant knowledge and context:"""
            
            knowledge = self._call_llm(prompt)
            
            return AgentResponse(
                agent_type=self.agent_type,
                content=knowledge,
                metadata={},
                success=True
            )
            
        except Exception as e:
            logger.error(f"Knowledge Expert error: {e}")
            return AgentResponse(
                agent_type=self.agent_type,
                content="",
                metadata={},
                success=False,
                error=str(e)
            )


class TranslatorAgent(BaseAgent):
    """
    Translator Agent - Handles language translation
    """
    
    def __init__(self):
        system_prompt = """You are a professional translator specializing in e-commerce and business terminology.
Your job is to accurately translate text while preserving meaning and context.

Guidelines:
1. Maintain professional tone
2. Preserve technical terms when appropriate
3. Adapt cultural references appropriately
4. Indicate the source and target languages
5. Handle product names and brands carefully

Provide accurate, natural-sounding translations."""
        super().__init__(AgentType.TRANSLATOR, system_prompt)
    
    def execute(self, query: str, context: Optional[Dict] = None) -> AgentResponse:
        """Translate text"""
        try:
            target_lang = context.get('target_language', 'English') if context else 'English'
            text = context.get('text', query) if context else query
            
            prompt = f"""{self.system_prompt}

Translate the following text to {target_lang}:

{text}

Translation:"""
            
            translation = self._call_llm(prompt)
            
            return AgentResponse(
                agent_type=self.agent_type,
                content=translation,
                metadata={'target_language': target_lang},
                success=True
            )
            
        except Exception as e:
            logger.error(f"Translator error: {e}")
            return AgentResponse(
                agent_type=self.agent_type,
                content="",
                metadata={},
                success=False,
                error=str(e)
            )

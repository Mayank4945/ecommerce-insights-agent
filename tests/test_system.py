"""
Test suite for the E-Commerce Insights Agent
"""

import pytest
import pandas as pd
from pathlib import Path
import sys

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.database import DatabaseManager
from src.memory import MemoryManager
from src.agents import AgentSystem, SQLAnalystAgent


class TestDatabaseManager:
    """Test database operations"""
    
    def test_database_initialization(self):
        """Test database initialization"""
        db = DatabaseManager()
        assert db.conn is not None
        assert db.db_path is not None
    
    def test_execute_query_safe(self):
        """Test safe query execution"""
        db = DatabaseManager()
        
        # Create test table
        test_df = pd.DataFrame({
            'id': [1, 2, 3],
            'name': ['A', 'B', 'C'],
            'value': [10, 20, 30]
        })
        db.conn.execute("CREATE TABLE test_table AS SELECT * FROM test_df")
        
        # Execute safe query
        result, error = db.execute_query("SELECT * FROM test_table")
        assert error is None
        assert len(result) == 3
        
        # Cleanup
        db.conn.execute("DROP TABLE test_table")
        db.close()
    
    def test_query_injection_prevention(self):
        """Test SQL injection prevention"""
        db = DatabaseManager()
        
        # Try dangerous query
        dangerous_query = "DROP TABLE customers; --"
        result, error = db.execute_query(dangerous_query)
        
        assert error is not None
        assert "dangerous" in error.lower()
        db.close()


class TestMemoryManager:
    """Test conversation memory"""
    
    def test_memory_initialization(self):
        """Test memory manager initialization"""
        memory = MemoryManager()
        assert memory.session_id is not None
        assert len(memory.messages) == 0
    
    def test_add_message(self):
        """Test adding messages"""
        memory = MemoryManager()
        
        memory.add_message('user', 'Hello')
        assert len(memory.messages) == 1
        
        memory.add_message('assistant', 'Hi there!')
        assert len(memory.messages) == 2
    
    def test_get_context(self):
        """Test getting LLM context"""
        memory = MemoryManager()
        
        memory.add_message('user', 'What is the revenue?')
        memory.add_message('assistant', 'The revenue is $1000')
        
        context = memory.get_context_for_llm()
        assert len(context) == 2
        assert context[0]['role'] == 'user'
        assert context[1]['role'] == 'assistant'
    
    def test_clear_history(self):
        """Test clearing conversation history"""
        memory = MemoryManager()
        
        memory.add_message('user', 'Test')
        assert len(memory.messages) == 1
        
        memory.clear_history()
        assert len(memory.messages) == 0


class TestAgents:
    """Test agent functionality"""
    
    @pytest.fixture
    def db_manager(self):
        """Create test database"""
        db = DatabaseManager()
        
        # Create test data
        customers_df = pd.DataFrame({
            'customer_id': ['C1', 'C2', 'C3'],
            'customer_city': ['São Paulo', 'Rio', 'São Paulo'],
            'customer_state': ['SP', 'RJ', 'SP']
        })
        
        orders_df = pd.DataFrame({
            'order_id': ['O1', 'O2', 'O3'],
            'customer_id': ['C1', 'C2', 'C3'],
            'order_status': ['delivered', 'delivered', 'shipped']
        })
        
        db.conn.execute("CREATE TABLE customers AS SELECT * FROM customers_df")
        db.conn.execute("CREATE TABLE orders AS SELECT * FROM orders_df")
        db._build_schema_info()
        
        yield db
        
        # Cleanup
        db.close()
    
    def test_sql_agent_query_generation(self, db_manager):
        """Test SQL agent query generation"""
        agent = SQLAnalystAgent(db_manager)
        
        # This would require a real API key to test
        # For now, just test that the agent initializes
        assert agent.db_manager is not None
        assert agent.agent_type.value == 'sql_analyst'


class TestDataProcessing:
    """Test data processing utilities"""
    
    def test_dataframe_creation(self):
        """Test creating dataframes"""
        df = pd.DataFrame({
            'category': ['A', 'B', 'C'],
            'revenue': [100, 200, 300]
        })
        
        assert len(df) == 3
        assert 'category' in df.columns
        assert df['revenue'].sum() == 600
    
    def test_aggregation(self):
        """Test data aggregation"""
        df = pd.DataFrame({
            'category': ['A', 'A', 'B', 'B'],
            'revenue': [100, 150, 200, 250]
        })
        
        grouped = df.groupby('category')['revenue'].sum()
        assert grouped['A'] == 250
        assert grouped['B'] == 450


class TestVisualization:
    """Test visualization generation"""
    
    def test_visualization_data_prep(self):
        """Test preparing data for visualization"""
        df = pd.DataFrame({
            'category': ['Electronics', 'Books', 'Clothing'],
            'revenue': [1000, 500, 750]
        })
        
        # Check if data is suitable for bar chart
        assert len(df) > 0
        assert 'category' in df.columns
        assert 'revenue' in df.columns
        
        # Check data types
        categorical = df.select_dtypes(include=['object']).columns
        numeric = df.select_dtypes(include=['float64', 'int64']).columns
        
        assert len(categorical) > 0
        assert len(numeric) > 0


class TestIntegration:
    """Integration tests"""
    
    def test_full_query_flow(self):
        """Test complete query flow (without API calls)"""
        # Initialize components
        db = DatabaseManager()
        memory = MemoryManager()
        
        # Create test data
        test_df = pd.DataFrame({
            'category': ['A', 'B'],
            'revenue': [100, 200]
        })
        db.conn.execute("CREATE TABLE test_products AS SELECT * FROM test_df")
        
        # Execute query
        result, error = db.execute_query("SELECT * FROM test_products")
        
        assert error is None
        assert len(result) == 2
        
        # Add to memory
        memory.add_message('user', 'Show me products')
        memory.add_message('assistant', f'Found {len(result)} products')
        
        assert len(memory.messages) == 2
        
        # Cleanup
        db.close()


# Pytest configuration
def pytest_configure(config):
    """Configure pytest"""
    config.addinivalue_line(
        "markers", "integration: mark test as integration test"
    )
    config.addinivalue_line(
        "markers", "slow: mark test as slow running"
    )


if __name__ == "__main__":
    # Run tests
    pytest.main([__file__, "-v", "--tb=short"])

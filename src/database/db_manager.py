"""
Database Manager for E-Commerce Data
Handles data loading, schema management, and SQL query execution
"""

import duckdb
import pandas as pd
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any
from datetime import datetime
from src.config import config
from src.logger import get_logger

logger = get_logger(__name__)


class DatabaseManager:
    """Manages database operations for e-commerce data"""
    
    def __init__(self, db_path: Optional[Path] = None):
        self.db_path = db_path or config.database.database_path
        self.conn = None
        self.schema_info: Dict[str, Any] = {}
        self._initialize_connection()
        
    def _initialize_connection(self):
        """Initialize database connection"""
        try:
            self.conn = duckdb.connect(str(self.db_path))
            logger.info(f"Database connection established: {self.db_path}")
        except Exception as e:
            logger.error(f"Failed to connect to database: {e}")
            raise
    
    def load_csv_data(self, data_dir: Path) -> Dict[str, int]:
        """
        Load CSV files from the Brazilian E-Commerce dataset
        
        Args:
            data_dir: Directory containing CSV files
            
        Returns:
            Dictionary with table names and row counts
        """
        logger.info(f"Loading CSV data from: {data_dir}")
        loaded_tables = {}
        
        # Expected CSV files from the Brazilian E-Commerce dataset
        csv_files = {
            'olist_customers_dataset.csv': 'customers',
            'olist_geolocation_dataset.csv': 'geolocation',
            'olist_order_items_dataset.csv': 'order_items',
            'olist_order_payments_dataset.csv': 'order_payments',
            'olist_order_reviews_dataset.csv': 'order_reviews',
            'olist_orders_dataset.csv': 'orders',
            'olist_products_dataset.csv': 'products',
            'olist_sellers_dataset.csv': 'sellers',
            'product_category_name_translation.csv': 'product_category_translation'
        }
        
        for csv_file, table_name in csv_files.items():
            csv_path = data_dir / csv_file
            if csv_path.exists():
                try:
                    df = pd.read_csv(csv_path)
                    self.conn.execute(f"DROP TABLE IF EXISTS {table_name}")
                    self.conn.execute(f"CREATE TABLE {table_name} AS SELECT * FROM df")
                    row_count = len(df)
                    loaded_tables[table_name] = row_count
                    logger.info(f"Loaded {table_name}: {row_count} rows")
                except Exception as e:
                    logger.error(f"Error loading {csv_file}: {e}")
            else:
                logger.warning(f"CSV file not found: {csv_file}")
        
        # Build schema information
        self._build_schema_info()
        
        return loaded_tables
    
    def _build_schema_info(self):
        """Build comprehensive schema information for all tables"""
        try:
            tables = self.get_table_list()
            
            for table in tables:
                # Get column information
                columns_query = f"""
                    SELECT column_name, data_type, is_nullable
                    FROM information_schema.columns
                    WHERE table_name = '{table}'
                    ORDER BY ordinal_position
                """
                columns_df = self.conn.execute(columns_query).fetchdf()
                
                # Get row count
                count_query = f"SELECT COUNT(*) as count FROM {table}"
                row_count = self.conn.execute(count_query).fetchone()[0]
                
                # Get sample data
                sample_query = f"SELECT * FROM {table} LIMIT 3"
                sample_df = self.conn.execute(sample_query).fetchdf()
                
                self.schema_info[table] = {
                    'columns': columns_df.to_dict('records'),
                    'row_count': row_count,
                    'sample_data': sample_df.to_dict('records')
                }
            
            logger.info(f"Schema information built for {len(tables)} tables")
        except Exception as e:
            logger.error(f"Error building schema info: {e}")
    
    def get_table_list(self) -> List[str]:
        """Get list of all tables in the database"""
        try:
            result = self.conn.execute("SHOW TABLES").fetchall()
            return [row[0] for row in result]
        except Exception as e:
            logger.error(f"Error getting table list: {e}")
            return []
    
    def get_schema_description(self) -> str:
        """Get a human-readable schema description for LLM context"""
        description_parts = ["# E-Commerce Database Schema\n"]
        
        for table_name, info in self.schema_info.items():
            description_parts.append(f"\n## Table: {table_name}")
            description_parts.append(f"Row count: {info['row_count']}")
            description_parts.append("\nColumns:")
            
            for col in info['columns']:
                nullable = "NULL" if col['is_nullable'] == 'YES' else "NOT NULL"
                description_parts.append(f"  - {col['column_name']} ({col['data_type']}) {nullable}")
            
            if info['sample_data']:
                description_parts.append("\nSample data:")
                description_parts.append(f"  {info['sample_data'][0]}")
        
        return "\n".join(description_parts)
    
    def execute_query(self, query: str, params: Optional[Dict] = None) -> Tuple[pd.DataFrame, Optional[str]]:
        """
        Execute a SQL query safely
        
        Args:
            query: SQL query to execute
            params: Optional query parameters
            
        Returns:
            Tuple of (DataFrame with results, error message if any)
        """
        try:
            # Basic SQL injection prevention
            dangerous_keywords = ['DROP', 'DELETE', 'TRUNCATE', 'ALTER', 'CREATE', 'INSERT', 'UPDATE']
            query_upper = query.upper()
            
            for keyword in dangerous_keywords:
                if keyword in query_upper and 'CREATE' not in query_upper.split(keyword)[0]:
                    logger.warning(f"Potentially dangerous query blocked: {query[:100]}")
                    return pd.DataFrame(), f"Query contains potentially dangerous keyword: {keyword}"
            
            # Execute query with timeout
            result = self.conn.execute(query).fetchdf()
            
            # Limit results
            if len(result) > config.database.max_query_results:
                logger.warning(f"Query returned {len(result)} rows, limiting to {config.database.max_query_results}")
                result = result.head(config.database.max_query_results)
            
            logger.info(f"Query executed successfully: {len(result)} rows returned")
            return result, None
            
        except Exception as e:
            error_msg = f"Query execution error: {str(e)}"
            logger.error(error_msg)
            return pd.DataFrame(), error_msg
    
    def get_table_stats(self, table_name: str) -> Dict[str, Any]:
        """Get statistical information about a table"""
        try:
            if table_name not in self.schema_info:
                return {}
            
            stats = {
                'table_name': table_name,
                'row_count': self.schema_info[table_name]['row_count'],
                'column_count': len(self.schema_info[table_name]['columns']),
                'columns': self.schema_info[table_name]['columns']
            }
            
            return stats
        except Exception as e:
            logger.error(f"Error getting table stats: {e}")
            return {}
    
    def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()
            logger.info("Database connection closed")

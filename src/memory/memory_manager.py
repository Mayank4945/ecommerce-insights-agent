"""
Memory Manager for Conversational Context
Handles conversation history and context management
"""

import json
from pathlib import Path
from typing import List, Dict, Any, Optional
from datetime import datetime
from collections import deque
from src.config import config
from src.logger import get_logger

logger = get_logger(__name__)


class ConversationMessage:
    """Represents a single message in the conversation"""
    
    def __init__(self, role: str, content: str, timestamp: Optional[datetime] = None, metadata: Optional[Dict] = None):
        self.role = role  # 'user', 'assistant', 'system'
        self.content = content
        self.timestamp = timestamp or datetime.now()
        self.metadata = metadata or {}
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert message to dictionary"""
        return {
            'role': self.role,
            'content': self.content,
            'timestamp': self.timestamp.isoformat(),
            'metadata': self.metadata
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ConversationMessage':
        """Create message from dictionary"""
        timestamp = datetime.fromisoformat(data['timestamp']) if 'timestamp' in data else None
        return cls(
            role=data['role'],
            content=data['content'],
            timestamp=timestamp,
            metadata=data.get('metadata', {})
        )


class MemoryManager:
    """Manages conversation history and context"""
    
    def __init__(self, session_id: Optional[str] = None):
        self.session_id = session_id or datetime.now().strftime("%Y%m%d_%H%M%S")
        self.max_history = config.memory.max_conversation_history
        self.messages: deque = deque(maxlen=self.max_history)
        self.session_metadata: Dict[str, Any] = {
            'created_at': datetime.now().isoformat(),
            'message_count': 0
        }
        
        # Load existing session if persistence is enabled
        if config.memory.enable_persistence:
            self._load_session()
    
    def add_message(self, role: str, content: str, metadata: Optional[Dict] = None):
        """Add a message to conversation history"""
        message = ConversationMessage(role, content, metadata=metadata)
        self.messages.append(message)
        self.session_metadata['message_count'] += 1
        
        logger.info(f"Added {role} message to conversation (total: {len(self.messages)})")
        
        # Persist if enabled
        if config.memory.enable_persistence:
            self._save_session()
    
    def get_messages(self, limit: Optional[int] = None) -> List[ConversationMessage]:
        """Get conversation messages"""
        messages = list(self.messages)
        if limit:
            messages = messages[-limit:]
        return messages
    
    def get_context_for_llm(self, system_prompt: Optional[str] = None) -> List[Dict[str, str]]:
        """
        Get conversation history formatted for LLM
        
        Args:
            system_prompt: Optional system prompt to include
            
        Returns:
            List of message dictionaries for LLM
        """
        context = []
        
        if system_prompt:
            context.append({
                'role': 'system',
                'content': system_prompt
            })
        
        for msg in self.messages:
            context.append({
                'role': msg.role,
                'content': msg.content
            })
        
        return context
    
    def get_conversation_summary(self) -> str:
        """Get a summary of the conversation"""
        if not self.messages:
            return "No conversation history"
        
        summary_parts = [
            f"Conversation Session: {self.session_id}",
            f"Total Messages: {len(self.messages)}",
            f"Started: {self.session_metadata['created_at']}"
        ]
        
        return "\n".join(summary_parts)
    
    def clear_history(self):
        """Clear conversation history"""
        self.messages.clear()
        self.session_metadata['message_count'] = 0
        logger.info("Conversation history cleared")
        
        if config.memory.enable_persistence:
            self._save_session()
    
    def _get_session_path(self) -> Path:
        """Get path to session file"""
        return config.memory.storage_path / f"session_{self.session_id}.json"
    
    def _save_session(self):
        """Save conversation session to disk"""
        try:
            session_data = {
                'session_id': self.session_id,
                'metadata': self.session_metadata,
                'messages': [msg.to_dict() for msg in self.messages]
            }
            
            session_path = self._get_session_path()
            with open(session_path, 'w', encoding='utf-8') as f:
                json.dump(session_data, f, indent=2, ensure_ascii=False)
            
            logger.debug(f"Session saved: {session_path}")
        except Exception as e:
            logger.error(f"Error saving session: {e}")
    
    def _load_session(self):
        """Load conversation session from disk"""
        try:
            session_path = self._get_session_path()
            if session_path.exists():
                with open(session_path, 'r', encoding='utf-8') as f:
                    session_data = json.load(f)
                
                self.session_metadata = session_data.get('metadata', {})
                
                # Load messages
                for msg_data in session_data.get('messages', []):
                    message = ConversationMessage.from_dict(msg_data)
                    self.messages.append(message)
                
                logger.info(f"Session loaded: {len(self.messages)} messages")
        except Exception as e:
            logger.warning(f"Could not load session: {e}")
    
    @staticmethod
    def list_sessions() -> List[str]:
        """List all available sessions"""
        try:
            session_files = config.memory.storage_path.glob("session_*.json")
            return [f.stem.replace('session_', '') for f in session_files]
        except Exception as e:
            logger.error(f"Error listing sessions: {e}")
            return []

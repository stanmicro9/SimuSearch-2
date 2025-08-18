import logging
import sys
from datetime import datetime
from typing import Optional

class ScientificLogger:
    """Enhanced logging for the scientific investigation system"""
    
    def __init__(self, name: str = "scientific_agents", level: str = "INFO"):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(getattr(logging, level.upper()))
        
        # Prevent duplicate handlers
        if not self.logger.handlers:
            self._setup_handlers()
    
    def _setup_handlers(self):
        """Setup logging handlers for console and file output"""
        
        # Console handler with colors
        console_handler = logging.StreamHandler(sys.stdout)
        console_formatter = ColoredFormatter(
            '%(asctime)s | %(levelname)s | %(name)s | %(message)s'
        )
        console_handler.setFormatter(console_formatter)
        console_handler.setLevel(logging.INFO)
        
        # File handler for detailed logs
        file_handler = logging.FileHandler(
            f"logs/scientific_agents_{datetime.now().strftime('%Y%m%d')}.log"
        )
        file_formatter = logging.Formatter(
            '%(asctime)s | %(levelname)s | %(name)s | %(funcName)s:%(lineno)d | %(message)s'
        )
        file_handler.setFormatter(file_formatter)
        file_handler.setLevel(logging.DEBUG)
        
        self.logger.addHandler(console_handler)
        self.logger.addHandler(file_handler)
    
    def log_agent_action(self, agent_name: str, action: str, details: Optional[str] = None):
        """Log agent actions with structured format"""
        message = f"🤖 {agent_name} | {action}"
        if details:
            message += f" | {details}"
        self.logger.info(message)
    
    def log_communication(self, from_agent: str, to_agent: str, message_type: str):
        """Log inter-agent communication"""
        self.logger.info(f"📡 {from_agent} → {to_agent} | {message_type}")
    
    def log_experiment(self, experiment_id: str, status: str, details: Optional[str] = None):
        """Log experiment execution"""
        message = f"🧪 Experiment {experiment_id} | {status}"
        if details:
            message += f" | {details}"
        self.logger.info(message)

class ColoredFormatter(logging.Formatter):
    """Colored console formatter"""
    
    COLORS = {
        'DEBUG': '\033[36m',    # Cyan
        'INFO': '\033[32m',     # Green
        'WARNING': '\033[33m',  # Yellow
        'ERROR': '\033[31m',    # Red
        'CRITICAL': '\033[35m', # Magenta
    }
    RESET = '\033[0m'
    
    def format(self, record):
        log_color = self.COLORS.get(record.levelname, self.RESET)
        record.levelname = f"{log_color}{record.levelname}{self.RESET}"
        return super().format(record)
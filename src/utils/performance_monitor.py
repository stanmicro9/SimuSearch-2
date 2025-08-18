import time
import psutil
import threading
from typing import Dict, Any, Callable
from functools import wraps
from dataclasses import dataclass

@dataclass
class PerformanceMetrics:
    """Performance metrics for agent operations"""
    execution_time: float
    memory_usage: float
    cpu_usage: float
    operation_name: str
    agent_name: str

class PerformanceMonitor:
    """Monitor system and agent performance"""
    
    def __init__(self):
        self.metrics: List[PerformanceMetrics] = []
        self.monitoring = False
        
    def start_monitoring(self):
        """Start system monitoring"""
        self.monitoring = True
        threading.Thread(target=self._monitor_system, daemon=True).start()
    
    def stop_monitoring(self):
        """Stop system monitoring"""
        self.monitoring = False
    
    def _monitor_system(self):
        """Background system monitoring"""
        while self.monitoring:
            cpu_percent = psutil.cpu_percent(interval=1)
            memory_percent = psutil.virtual_memory().percent
            
            if cpu_percent > 90 or memory_percent > 90:
                print(f"⚠️  High resource usage: CPU={cpu_percent}%, Memory={memory_percent}%")
            
            time.sleep(5)
    
    def measure_performance(self, operation_name: str, agent_name: str = "system"):
        """Decorator to measure operation performance"""
        def decorator(func: Callable) -> Callable:
            @wraps(func)
            def wrapper(*args, **kwargs):
                start_time = time.time()
                start_memory = psutil.Process().memory_info().rss / 1024 / 1024  # MB
                
                try:
                    result = func(*args, **kwargs)
                    
                    end_time = time.time()
                    end_memory = psutil.Process().memory_info().rss / 1024 / 1024  # MB
                    execution_time = end_time - start_time
                    memory_usage = end_memory - start_memory
                    cpu_usage = psutil.cpu_percent()
                    
                    metrics = PerformanceMetrics(
                        execution_time=execution_time,
                        memory_usage=memory_usage,
                        cpu_usage=cpu_usage,
                        operation_name=operation_name,
                        agent_name=agent_name
                    )
                    
                    self.metrics.append(metrics)
                    
                    if execution_time > 10:  # Log slow operations
                        print(f"⏱️  Slow operation: {operation_name} took {execution_time:.1f}s")
                    
                    return result
                    
                except Exception as e:
                    print(f"❌ Performance monitoring error in {operation_name}: {str(e)}")
                    raise
            
            return wrapper
        return decorator
    
    def get_performance_report(self) -> Dict[str, Any]:
        """Generate performance report"""
        if not self.metrics:
            return {"status": "No metrics collected"}
        
        total_time = sum(m.execution_time for m in self.metrics)
        avg_memory = sum(m.memory_usage for m in self.metrics) / len(self.metrics)
        avg_cpu = sum(m.cpu_usage for m in self.metrics) / len(self.metrics)
        
        agent_stats = {}
        for metric in self.metrics:
            agent = metric.agent_name
            if agent not in agent_stats:
                agent_stats[agent] = {"count": 0, "total_time": 0}
            agent_stats[agent]["count"] += 1
            agent_stats[agent]["total_time"] += metric.execution_time
        
        return {
            "total_execution_time": total_time,
            "average_memory_usage_mb": avg_memory,
            "average_cpu_usage": avg_cpu,
            "operations_count": len(self.metrics),
            "agent_statistics": agent_stats,
            "slowest_operations": sorted(
                self.metrics, 
                key=lambda m: m.execution_time, 
                reverse=True
            )[:5]
        }
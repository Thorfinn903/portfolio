import time
import threading

class SystemMonitor:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super(SystemMonitor, cls).__new__(cls)
                cls._instance._initialized = False
            return cls._instance

    def __init__(self):
        if self._initialized:
            return
        self._initialized = True
        
        # Metrics
        self.llm_requests_total = 0
        self.llm_failures_total = 0
        self.pipeline_requests_total = 0
        self.total_latency_ms = 0.0
        self.last_failure_reason = None
        self.last_failure_timestamp = None

    def record_request(self):
        """Records a new incoming request to the pipeline."""
        self.pipeline_requests_total += 1

    def record_llm_success(self, latency_ms: float):
        """
        Records a successful LLM call.
        
        Args:
            latency_ms (float): The time taken in milliseconds.
        """
        self.llm_requests_total += 1
        self.total_latency_ms += latency_ms

    def record_llm_failure(self, reason: str):
        """
        Records a failed LLM call.
        
        Args:
            reason (str): The error message or exception string.
        """
        self.llm_failures_total += 1
        self.last_failure_reason = reason
        self.last_failure_timestamp = time.ctime()

    def get_status(self):
        """Returns the current system health snapshot."""
        # Calculate Average Latency
        avg_latency = 0.0
        if self.llm_requests_total > 0:
            avg_latency = self.total_latency_ms / self.llm_requests_total

        # Determine Health Status
        status = "healthy"
        if self.llm_failures_total > 5:
            status = "degraded"
        
        return {
            "status": status,
            "llm_requests_total": self.llm_requests_total,
            "llm_failures_total": self.llm_failures_total,
            "avg_latency_ms": round(avg_latency, 2),
            "pipeline_requests_total": self.pipeline_requests_total,
            "last_failure": {
                "reason": self.last_failure_reason,
                "timestamp": self.last_failure_timestamp
            }
        }
class AIProductFactoryError(Exception):
    """Base application error."""


class ProviderError(AIProductFactoryError):
    """Raised when the LLM provider call fails."""


class StructuredOutputError(AIProductFactoryError):
    """Raised when structured output cannot be parsed or validated."""


class BudgetExceededError(AIProductFactoryError):
    """Raised when a budget limit is exceeded."""


class QaValidationError(AIProductFactoryError):
    """Raised when QA validation fails."""


class RuntimeConfigurationError(AIProductFactoryError):
    """Raised when runtime configuration is invalid."""

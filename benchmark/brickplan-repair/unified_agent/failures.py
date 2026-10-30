"""Errors that must never be confused with a legal but incorrect assembly."""
class InputContractError(ValueError):pass

class ProviderError(RuntimeError):
    def __init__(self,code,message,*,status=None,response=None):
        super().__init__(message);self.code=code;self.status=status;self.response=response

class GenerationError(ProviderError):pass

def terminal_for(exc):
    if isinstance(exc,InputContractError):return 'harness_error'
    if isinstance(exc,GenerationError):return 'output_truncated' if exc.code=='OUTPUT_TRUNCATED' else 'provider_output_error'
    return 'service_error'

def describe(exc):
    return dict(code=getattr(exc,'code',type(exc).__name__),type=type(exc).__name__,message=str(exc)[:400],
        httpStatus=getattr(exc,'status',None),retryable=False)

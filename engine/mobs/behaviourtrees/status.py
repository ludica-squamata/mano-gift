import sys

if 'pydevd' in sys.modules:
    Success = '(success)'
    Running = '(running)'
    Failure = '(failure)'
else:
    Success = 0
    Running = 1
    Failure = 2

__all__ = ['Success', 'Failure', 'Running']

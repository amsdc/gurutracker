class AppdataError(Exception):
    pass

class VersionMismatchError(AppdataError):
    """VersionMismatchError
    
    To be raised when the export function cannot handle exports
    from this version.
    """
    pass
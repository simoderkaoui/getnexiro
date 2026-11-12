# getnexiro project package

# Compatibility patch for Python 3.14+ Context / RequestContext copying
try:
    from django.template import RequestContext
    _orig_rc_copy = getattr(RequestContext, '__copy__', None)
    if _orig_rc_copy:
        def _safe_rc_copy(self):
            duplicate = _orig_rc_copy(self)
            duplicate.__dict__.update(self.__dict__)
            return duplicate
        RequestContext.__copy__ = _safe_rc_copy
except Exception:
    pass

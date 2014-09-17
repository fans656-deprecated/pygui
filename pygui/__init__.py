import _app
#import _widget
import _canvas

# export
__all__ = []
modules = [_canvas]
for module in modules:
    moduleName = module.__name__.split('.')[-1]
    for symbol in module.__all__:
        fmt = '{sym} = {mod}.{sym}'
        stmt = fmt.format(sym=symbol, mod=moduleName)
        exec stmt
        __all__.append(symbol)

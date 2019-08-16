import re

__all__ = ['chunkSlice', 'dsetChunk', 'dsetContentDict', 'dsetDict', 'groupDict', 'uriJoin', 'uriName']

## chunk handling
def chunkSlice(chunk, s):
    if s.start is None:
        return slice(None, s.stop*chunk, s.step)

    return slice(s.start*chunk, s.stop*chunk, s.step)

def dsetChunk(dset, row, col):
    return dset[slice(*row), slice(*col)].tolist()


## create dicts to be converted to json
dsetContentKeys = ('dtype', 'ndim', 'shape')
def dsetContentDict(dset, row=None, col=None):
    # get all metadata
    content = {k:getattr(dset, k) for k in dsetContentKeys}
    content['attrs'] = dict(*dset.attrs.item())

    # get actual data, if requested
    content['data'] = dsetChunk(dset, row, col) if row and col else None

    return content

def dsetDict(name, uri, content=None):
    return dict([
        ('type', 'dataset'),
        ('name', name),
        ('uri', uri),
        ('content', content)
    ])

def groupDict(name, uri):
    return dict([
        ('type', 'group'),
        ('name', name),
        ('uri', uri),
        ('content', None)
    ])


## uri handling
_emptyUriRe = re.compile('//')
def uriJoin(*parts):
    return _emptyUriRe.sub('/', '/'.join(parts))

def uriName(uri):
    return uri.split('/')[-1]

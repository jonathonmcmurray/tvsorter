def mineach(x,y):
    """
    Return a dictionary with min for each key
    """
    # output dictionary, intially empty
    o = {}
    # complete set of keys
    ks = set(list(x.keys()) + list(y.keys()))
    # iterate over each key
    for k in ks:
        # if in both, take the min of the two
        if k in x.keys() and k in y.keys():
            o[k] = min(x[k],y[k])
        # otherwise, take from which dict it's in
        elif k in x.keys():
            o[k] = x[k]
        else:
            o[k] = y[k]
    return o

def invert(x):
    """
    "Invert" a dictionary of dictionaries passed in i.e. swap inner & outer keys
    e.g. {"a":{"x":1,"y":2},"b":{"x":3,"y":4}} becomes {"x":{"a":1,"b":3},"y":{"a":2,"b":4}}
    """
    # dict for output
    inv={}
    # iterate over the keys of first dictionary from input
    for k in list(list(x.values())[0].keys()):
        # index into each dictionary from input to get values for this key
        inv[k] = dict([(x,y[k]) for x,y in x.items()])
    return inv

def prettydict(d,sep="|"):
    """
    Pretty print a dictionary
    """
    # pad length for keys
    pd = max(map(len,d))
    for k,v in d.items():
        # pad key to max length & format
        print(f'{k.ljust(pd)} {sep} {v}')
    return



def traverser_shortest_path(hg, source, target, direction="BOTH", max_depth=10, label=""):

    import time 

    time_before = time.time()
    res = hg.traverser_shortest_path(source, target, direction, max_depth, label)
    time_after = time.time()
    return {
        "response": res.response,
        "time": time_after - time_before
    }

def traverser_kout(hg, source, direction="BOTH", max_depth=5, label="", nearest="false"):

    import time

    time_before = time.time()
    res = hg.traverser_kout(source, direction, max_depth, label, nearest)
    time_after = time.time()

    return {
        "response": res.response,
        "time": time_after - time_before
    }

def traverser_kneighbor(hg, source, direction="BOTH", max_depth=5, label=""):

    import time

    time_before = time.time()
    res = hg.traverser_kneighbor(source, direction, max_depth, label)
    time_after = time.time()

    return {
        "response": res.response,
        "time": time_after - time_before
    }
def traverser_shortest_path(hg, source, target, direction="BOTH", max_depth=10, label=""):

    import time 

    time_before = time.time()
    res = hg.traverser_shortest_path(source, target, direction, max_depth, label)
    time_after = time.time()
    return {
        "response": (res.response, res.status_code),
        "time": time_after - time_before
    }

def traverser_kout(hg, source, direction="BOTH", max_depth=5, label="", nearest="true"):

    import time

    time_before = time.time()
    res = hg.traverser_kout(source=source, direction=direction, depth=max_depth, label=label, nearest=nearest)
    time_after = time.time()

    return {
        "response": (res.response, res.status_code),
        "time": time_after - time_before
    }

def traverser_kneighbor(hg, source, direction="BOTH", max_depth=5, label=""):

    import time

    time_before = time.time()
    res = hg.traverser_kneighbor(source, direction, max_depth, label)
    time_after = time.time()

    return {
        "response": (res.response, res.status_code),
        "time": time_after - time_before
    }
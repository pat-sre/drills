def solve(nodes, edges):
    inf = float("inf")
    dist = {u: {v: (0 if u == v else inf) for v in nodes} for u in nodes}

    for u, v, w in edges:
        if w < dist[u][v]:
            dist[u][v] = w

    for k in nodes:
        for i in nodes:
            for j in nodes:
                if dist[i][k] + dist[k][j] < dist[i][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]

    return dist

class UnionFind:
    def __init__(self, n):
        self.parent = list(range(n))
        self.size = [1] * n
        self.total_components = n

    def find(self, idx):
        if self.parent[idx] != idx:
            self.parent[idx] = self.find(self.parent[idx])
        return self.parent[idx]

    def union(self, u, v):
        root_u, root_v = self.find(u), self.find(v)
        if root_u == root_v:
            return False
        if self.size[root_u] < self.size[root_v]:
            root_u, root_v = root_v, root_u
        self.parent[root_v] = root_u
        self.size[root_u] += self.size[root_v]
        self.total_components -= 1
        return True


solve = UnionFind

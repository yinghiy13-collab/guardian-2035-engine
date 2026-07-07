import hashlib

class MerkleLedger:
    def __init__(self):
        self.leaves = []

    def add_entry(self, data: str) -> str:
        leaf_hash = hashlib.sha256(data.encode()).hexdigest()
        self.leaves.append(leaf_hash)
        return leaf_hash

    def get_root(self) -> str:
        if not self.leaves:
            return hashlib.sha256(b"empty").hexdigest()
        root = self.leaves[0]
        for leaf in self.leaves[1:]:
            root = hashlib.sha256((root + leaf).encode()).hexdigest()
        return root


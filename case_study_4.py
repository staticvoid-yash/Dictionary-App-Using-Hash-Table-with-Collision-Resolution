"""
============================================================
 Case Study: Dictionary Application using Hash Tables
 Features: Insert, Search, Delete, Collision Resolution
 Collision Techniques: Chaining, Linear/Quadratic Probing,
                       Double Hashing
============================================================
"""


# ============================================================
# TECHNIQUE 1: SEPARATE CHAINING
# ============================================================
class DictionaryChaining:
    """
    Each bucket is a list. Collisions append to same bucket.
    Simple, efficient, handles high load factors well.
    """

    def __init__(self, size=11):
        self.size = size
        self.buckets = [[] for _ in range(size)]
        self.count = 0
        self.collisions = 0

    def _hash(self, key):
        # Polynomial rolling hash (better distribution than sum)
        h = 0
        for ch in key:
            h = (h * 31 + ord(ch)) % self.size
        return h

    def insert(self, word, meaning):
        idx = self._hash(word)
        bucket = self.buckets[idx]

        for i, (k, v) in enumerate(bucket):
            if k == word:
                bucket[i] = (word, meaning)   # Update
                return
        if bucket:
            self.collisions += 1
        bucket.append((word, meaning))
        self.count += 1

    def search(self, word):
        idx = self._hash(word)
        for k, v in self.buckets[idx]:
            if k == word:
                return v
        return None

    def delete(self, word):
        idx = self._hash(word)
        bucket = self.buckets[idx]
        for i, (k, v) in enumerate(bucket):
            if k == word:
                bucket.pop(i)
                self.count -= 1
                return True
        return False

    def load_factor(self):
        return self.count / self.size

    def display(self):
        print("\n  ── Hash Table (Separate Chaining) ──")
        for i, bucket in enumerate(self.buckets):
            print(f"  [{i:>2}] " + " → ".join(f"{k}" for k, _ in bucket))


# ============================================================
# TECHNIQUE 2: LINEAR PROBING (Open Addressing)
# ============================================================
class DictionaryLinearProbing:
    """
    On collision, check next slot (i+1, i+2, ...).
    Uses tombstone marker for deletion.
    """

    DELETED = object()

    def __init__(self, size=11):
        self.size = size
        self.keys = [None] * size
        self.values = [None] * size
        self.count = 0
        self.collisions = 0
        self.tombstones = 0

    def _hash(self, key):
        return sum(ord(c) for c in key) % self.size

    def insert(self, word, meaning):
        idx = self._hash(word)
        first_tombstone = -1

        for step in range(self.size):
            pos = (idx + step) % self.size
            if self.keys[pos] is None:
                target = first_tombstone if first_tombstone != -1 else pos
                self.keys[target] = word
                self.values[target] = meaning
                self.count += 1
                if step > 0:
                    self.collisions += 1
                return
            elif self.keys[pos] is self.DELETED:
                if first_tombstone == -1:
                    first_tombstone = pos
            elif self.keys[pos] == word:
                self.values[pos] = meaning
                return
        raise Exception("Hash table full!")

    def search(self, word):
        idx = self._hash(word)
        for step in range(self.size):
            pos = (idx + step) % self.size
            if self.keys[pos] is None:
                return None
            if self.keys[pos] is self.DELETED:
                continue
            if self.keys[pos] == word:
                return self.values[pos]
        return None

    def delete(self, word):
        idx = self._hash(word)
        for step in range(self.size):
            pos = (idx + step) % self.size
            if self.keys[pos] is None:
                return False
            if self.keys[pos] is self.DELETED:
                continue
            if self.keys[pos] == word:
                self.keys[pos] = self.DELETED
                self.values[pos] = None
                self.count -= 1
                self.tombstones += 1
                return True
        return False

    def load_factor(self):
        return self.count / self.size

    def display(self):
        print("\n  ── Hash Table (Linear Probing) ──")
        for i in range(self.size):
            k = self.keys[i]
            if k is None:
                print(f"  [{i:>2}]  --")
            elif k is self.DELETED:
                print(f"  [{i:>2}]  <deleted>")
            else:
                print(f"  [{i:>2}]  {k}")


# ============================================================
# TECHNIQUE 3: QUADRATIC PROBING
# ============================================================
class DictionaryQuadraticProbing:
    """Collision: try i+1², i+2², i+3², ... avoids clustering."""

    DELETED = object()

    def __init__(self, size=11):
        self.size = size
        self.keys = [None] * size
        self.values = [None] * size
        self.count = 0
        self.collisions = 0

    def _hash(self, key):
        return sum(ord(c) for c in key) % self.size

    def insert(self, word, meaning):
        idx = self._hash(word)
        for step in range(self.size):
            pos = (idx + step * step) % self.size
            if self.keys[pos] is None or self.keys[pos] is self.DELETED:
                self.keys[pos] = word
                self.values[pos] = meaning
                self.count += 1
                if step > 0:
                    self.collisions += 1
                return
            if self.keys[pos] == word:
                self.values[pos] = meaning
                return

    def search(self, word):
        idx = self._hash(word)
        for step in range(self.size):
            pos = (idx + step * step) % self.size
            if self.keys[pos] is None:
                return None
            if self.keys[pos] == word:
                return self.values[pos]
        return None

    def delete(self, word):
        idx = self._hash(word)
        for step in range(self.size):
            pos = (idx + step * step) % self.size
            if self.keys[pos] is None:
                return False
            if self.keys[pos] == word:
                self.keys[pos] = self.DELETED
                self.values[pos] = None
                self.count -= 1
                return True
        return False

    def display(self):
        print("\n  ── Hash Table (Quadratic Probing) ──")
        for i in range(self.size):
            k = self.keys[i]
            tag = "--" if k is None else ("<del>" if k is self.DELETED else k)
            print(f"  [{i:>2}]  {tag}")


# ============================================================
# TECHNIQUE 4: DOUBLE HASHING
# ============================================================
class DictionaryDoubleHashing:
    """Uses second hash fn as step size — minimal clustering."""

    DELETED = object()

    def __init__(self, size=11):
        self.size = size
        self.keys = [None] * size
        self.values = [None] * size
        self.count = 0
        self.collisions = 0

    def _hash1(self, key):
        return sum(ord(c) for c in key) % self.size

    def _hash2(self, key):
        # Must return value in [1, size-1]
        return 1 + (sum(ord(c) for c in key) % (self.size - 1))

    def insert(self, word, meaning):
        idx = self._hash1(word)
        step_size = self._hash2(word)
        for step in range(self.size):
            pos = (idx + step * step_size) % self.size
            if self.keys[pos] is None or self.keys[pos] is self.DELETED:
                self.keys[pos] = word
                self.values[pos] = meaning
                self.count += 1
                if step > 0:
                    self.collisions += 1
                return
            if self.keys[pos] == word:
                self.values[pos] = meaning
                return

    def search(self, word):
        idx = self._hash1(word)
        step_size = self._hash2(word)
        for step in range(self.size):
            pos = (idx + step * step_size) % self.size
            if self.keys[pos] is None:
                return None
            if self.keys[pos] == word:
                return self.values[pos]
        return None

    def delete(self, word):
        idx = self._hash1(word)
        step_size = self._hash2(word)
        for step in range(self.size):
            pos = (idx + step * step_size) % self.size
            if self.keys[pos] is None:
                return False
            if self.keys[pos] == word:
                self.keys[pos] = self.DELETED
                self.values[pos] = None
                self.count -= 1
                return True
        return False

    def display(self):
        print("\n  ── Hash Table (Double Hashing) ──")
        for i in range(self.size):
            k = self.keys[i]
            tag = "--" if k is None else ("<del>" if k is self.DELETED else k)
            print(f"  [{i:>2}]  {tag}")


# ============================================================
# MAIN DICTIONARY APP (User-facing)
# ============================================================
class DictionaryApp:
    """Wraps a hash table into a user-friendly dictionary."""

    def __init__(self, technique="chaining"):
        techniques = {
            "chaining":  DictionaryChaining,
            "linear":    DictionaryLinearProbing,
            "quadratic": DictionaryQuadraticProbing,
            "double":    DictionaryDoubleHashing,
        }
        self.table = techniques[technique]()
        self.technique = technique

    def add(self, word, meaning):
        self.table.insert(word.lower(), meaning)

    def lookup(self, word):
        return self.table.search(word.lower())

    def remove(self, word):
        return self.table.delete(word.lower())

    def stats(self):
        print(f"\n  Technique     : {self.technique}")
        print(f"  Words stored  : {self.table.count}")
        print(f"  Table size    : {self.table.size}")
        print(f"  Load factor   : {self.table.load_factor():.2f}")
        print(f"  Collisions    : {self.table.collisions}")


# ============================================================
# DEMO / TEST
# ============================================================
if __name__ == "__main__":
    print("=" * 65)
    print("   DICTIONARY APPLICATION USING HASH TABLES")
    print("=" * 65)

    words = [
        ("apple",    "A round fruit with red or green skin"),
        ("banana",   "A long curved fruit with yellow skin"),
        ("cherry",   "A small round red fruit with a stone"),
        ("date",     "A sweet brown fruit of the palm tree"),
        ("elderberry","A dark purple berry used in syrups"),
        ("fig",      "A soft sweet fruit with many seeds"),
        ("grape",    "A small round fruit growing in bunches"),
        ("honeydew", "A melon with green flesh and sweet taste"),
        ("kiwi",     "A fuzzy brown fruit with green flesh"),
        ("lemon",    "A yellow citrus fruit with sour juice"),
        ("mango",    "A tropical sweet orange-yellow fruit"),
        ("nectarine","A smooth-skinned variety of peach"),
    ]

    for technique in ["chaining", "linear", "quadratic", "double"]:
        print(f"\n{'#'*65}")
        print(f"  USING TECHNIQUE: {technique.upper()}")
        print(f"{'#'*65}")

        app = DictionaryApp(technique)

        # Insert all words
        for w, m in words:
            app.add(w, m)

        app.table.display()
        app.stats()

        # Lookup
        print("\n  ── Lookups ──")
        for w in ["mango", "kiwi", "pizza"]:
            meaning = app.lookup(w)
            if meaning:
                print(f"  '{w}' → {meaning}")
            else:
                print(f"  '{w}' → NOT FOUND")

        # Delete
        print("\n  ── Deletion ──")
        print(f"  Delete 'banana': {app.remove('banana')}")
        print(f"  Lookup 'banana': {app.lookup('banana')}")
        print(f"  Delete 'pizza' (not present): {app.remove('pizza')}")
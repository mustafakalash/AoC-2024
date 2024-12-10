class Chunk:
    def __init__(self, size, id = None):
        self.id = id
        self.size = size

    def __str__(self):
        symbol = "." if self.id is None else str(self.id)
        return symbol * self.size
    
class Filesystem:
    def __init__(self, input_fn):
        self.chunks = []
        with open(input_fn) as f:
            is_file = True
            id = 0
            for size in f.read().strip():
                size = int(size)
                if size > 0: 
                    if is_file:
                        self.chunks.append(Chunk(size, id))
                        id += 1
                    else:
                        self.chunks.append(Chunk(size))

                is_file = not is_file

    def __str__(self):
        return "".join(str(chunk) for chunk in self.chunks)
    
    def checksum(self):
        chksum = 0
        i = 0
        for chunk in self.chunks:
            for i in range(i, i + chunk.size):
                if chunk.id is not None:
                    chksum += i * chunk.id
                i += 1

        return chksum
    
    def insert_chunk(self, index, chunk):
            right_chunk = self.chunks[min(index, len(self.chunks) - 1)]
            left_chunk = self.chunks[max(0, index - 1)]
            if right_chunk.id == chunk.id:
                right_chunk.size += chunk.size
            elif left_chunk.id == chunk.id:
                left_chunk.size += chunk.size
            else:
                self.chunks.insert(index, chunk)
    
    def swap(self, chunk1, chunk2, fragment):
        if self.chunks.index(chunk1) > self.chunks.index(chunk2):
            chunk1, chunk2 = chunk2, chunk1

        if not fragment:
            if chunk1.id is not None and chunk1.size > chunk2.size or \
                chunk2.id is not None and chunk2.size > chunk1.size:
                return False
            
        if chunk1.size == chunk2.size:
            chunk1.id, chunk2.id = chunk2.id, chunk1.id
        elif chunk1.size < chunk2.size:
            chunk2.size = chunk2.size - chunk1.size
            id = chunk1.id
            chunk1.id = chunk2.id
            self.insert_chunk(self.chunks.index(chunk2) + 1, Chunk(chunk1.size, id))
        else:
            chunk1.size = chunk1.size - chunk2.size
            id = chunk2.id
            chunk2.id = chunk1.id
            self.insert_chunk(self.chunks.index(chunk1), Chunk(chunk2.size, id))

        return True
    
    def compact(self, fragment = True):
        right = len(self.chunks) - 1
        while right >= 0:
            right_chunk = self.chunks[right]
            if right_chunk.id is None:
                right -= 1
                continue

            left = 0
            while left < len(self.chunks) - 1 and (self.chunks[left].id is not None or \
              (not fragment and self.chunks[left].size < right_chunk.size)):
                left += 1

            if left >= right:
                right -= 1
                continue

            left_chunk = self.chunks[left]
            self.swap(left_chunk, right_chunk, fragment)
            
        return self.checksum()

fs = Filesystem("9/input")
print(fs.compact())
fs = Filesystem("9/input")
print(fs.compact(False))
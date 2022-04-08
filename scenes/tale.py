import numpy as np


class Node:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.__next = None

    @property
    def next(self):
        return self.__next

    @next.setter
    def next(self, next):
        assert type(next) == Node
        self.__next = next


class ST:
    def __init__(self):
        self.data = None

    def put(self, key, value):
        count = 0
        if self.data == None:
            node = Node(key, value)
            self.data = node
            return 0
        else:
            node = self.data
            while node is not None:
                count += 1
                if key == node.key:  # 命中
                    node.value = value
                    return count
                else:
                    node = node.next
            node = Node(key, value)
            node.next = self.data
            self.data = node
            return count

    def get(self, key):
        count = 0
        if self.data == None:
            return None, 0
        else:
            node = self.data
            while node is not None:
                count += 1
                if key == node.key:  # 命中
                    return node.value, count
                else:
                    node = node.next
            return None, count


if __name__ == '__main__':
    st = ST()
    index = 0
    results = []
    allCount = 0
    with open('assets/tale.txt', encoding='utf-8') as f:
        data = f.read().split()
        for word in data:
            if len(word) < 8:
                continue
            c1, c2 = st.get(word)
            if c1:
                c3 = st.put(word, c1 + 1)
            else:
                c3 = st.put(word, 1)
            allCount += c3
            results.append([index, c3, allCount / (index + 1)])
            index += 1
        print(results)
        np.save('assets/results', results)
    results = np.load('assets/results.npy', allow_pickle=True)
    print(results)
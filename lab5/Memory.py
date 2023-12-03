class Memory:
    def __init__(self, name):  # memory name
        self.scope_name = name
        self.memory = {}

    def has_key(self, name):  # variable name
        return name in self.memory

    def get(self, name):  # gets from memory current value of variable <name>
        return self.memory[name]

    def put(self, name, value):  # puts into memory current value of variable <name>
        self.memory[name] = value


class MemoryStack:
    def __init__(self, memory=None):  # initialize memory stack with memory <memory>
        if memory is None:
            memory = Memory('global')
        self.stack = [memory]

    def get(self, name):  # gets from memory stack current value of variable <name>
        for i in range(len(self.stack) - 1, -1, -1):
            if self.stack[i].has_key(name):
                return self.stack[i].get(name)
        return None

    def insert(self, name, value):  # inserts into memory stack variable <name> with value <value>
        self.stack[-1].put(name, value)

    def set(self, name, value):  # sets variable <name> to value <value>
        self.stack[-1].put(name, value)

    def push(self, memory: str):  # pushes memory <memory> onto the stack
        self.stack.append(Memory(memory))

    def pop(self):  # pops the top memory from the stack
        for key in list(self.stack[-1].memory.keys()):
            for i in range(len(self.stack) - 2, -1, -1):
                if self.stack[i].has_key(key):
                    self.stack[i].put(key, self.stack[-1].get(key))
                    break

        self.stack.pop()

class stack:
    elements, stack_top = [], -1

    def __init__(self, n):
        self.elements = [None for i in range(n)]

    def push(self, x):
        self.stack_top += 1
        self.elements[self.stack_top] = x

    def pop(self):
        ret_val = None
        if self.stack_top == -1:
            ret_val = self.elements[self.stack_top + 1]
        else:
            ret_val = self.elements[self.stack_top]
            self.stack_top -= 1
        return ret_val

    def top_of_stack(self):
        return self.elements[self.stack_top]

    def size(self):
        return len(self.elements)

    def is_empty(self):
        return self.stack_top == -1

class Node:
    """Simple node with links to next and previous nodes."""
    def __init__(self, data):
        self.data = data
        self.next = None
        self.prev = None

    def __repr__(self):
        return self.data

    
class CycleDoublyLinkedList:
    """
    Circular list with doubly connected nodes.

    get_next - retrieve next node data.
    get_prev - retrieve previous node data.
    """
    def __init__(self, nodes=None):
        self.start = None
        if nodes is not None:
            self.start = Node(data=nodes[0])
            self.head = self.start
            i = 1
            while i < len(nodes):
                simple_node = Node(data=nodes[i])
                self.head.next = simple_node
                simple_node.prev = self.head
                self.head = simple_node
                i += 1
            self.head.next, self.start.prev = self.start, self.head

    def __iter__(self):
        node = self.start.next
        yield self.start
        while node is not self.start:
            yield node
            node = node.next

    def __repr__(self):
        pass
    
    def get_prev(self, target_node_data):
        if self.start is None:
            raise Exception("List is empty")

        for node in self:
            if node.data == target_node_data:
                return node.prev.data

        raise Exception(f'Node with "{target_node_data}" not found')

    def get_next(self, target_node_data):
        if self.start is None:
            raise Exception("List is empty")

        for node in self:
            if node.data == target_node_data:
                return node.next.data
        
        raise Exception(f'Node with "{target_node_data}" not found')

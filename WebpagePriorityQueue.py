class Node:
    def __init__(self, content, priority):
        """
        A node in the WebpagePriorityQueue contains a WebPageIndex object and
        it's corresponding priority value
        :param content: WebPageIndex object
        :param priority: priority value
        """
        self.web_page_index = content
        self.query_priority = priority


class WebpagePriorityQueue:
    def __init__(self, query, web_pages):
        """
        Initializes a Webpage Priority Queue
        :param query: Keyword, searched for in each web page
        :param web_pages: list of all WebPageIndex objects
        """
        self.query = query.split()  # in case it is more than 1 word
        self.web_pages = web_pages
        self.queue = []

        # determines the priority of all web pages based on keyword(s)
        for page in self.web_pages:
            priority = 0
            for key_word in self.query:
                priority += page.getCount(key_word)
            node = Node(page, priority)
            self.insert(node)

    def insert(self, node):
        """
        Inserts node into max heap priority queue
        :param node: Node with all attributes from above node class
        """
        self.queue.append(node)
        child_position = len(self.queue) - 1
        parent_position = int((child_position - 1) / 2)

        # shuffles nodes from the bottom up to be valid max heap priority queue
        while self.queue[parent_position].query_priority < \
                self.queue[child_position].query_priority:
            child = self.queue[child_position]
            self.queue[child_position] = self.queue[parent_position]
            self.queue[parent_position] = child

            child_position = parent_position
            parent_position = int((child_position - 1) / 2)

    def peek(self):
        """
        Gets web page with highest priority without removing it
        :return: WebpageIndex with highest priority in the WebpagePriorityQueue
        """
        if len(self.queue) == 0:
            return None
        else:
            return self.queue[0]

    def poll(self):
        """
        Gets highest priority web page and remove it from the max heap priority
        queue
        :return: WebpageIndex with highest priority in the WebpagePriorityQueue
        """
        if len(self.queue) == 0:  # empty queue
            return None
        elif len(self.queue) == 1:  # 1 node in queue
            highest_priority = self.queue[0]
            del self.queue[0]
            return highest_priority
        else:  # > 1 node in queue
            highest_priority = self.queue[0]  # Stores highest priority
            temp = self.queue[-1]
            del self.queue[-1]
            self.queue[0] = temp  # Inserts bottom right-most at top

            # shuffles nodes from top down to be valid max heap priority queue
            parent = self.queue[0]
            parent_position = 0

            # If statements prevent index out of bounds errors
            if ((2 * parent_position) + 1) > len(self.queue) - 1:
                left_child = Node("", 0)
                right_child = Node("", 0)
            elif ((2 * parent_position) + 2) > len(self.queue) - 1:
                left_child = self.queue[(2 * parent_position) + 1]
                right_child = Node("", 0)
            else:
                left_child = self.queue[(2 * parent_position) + 1]
                right_child = self.queue[(2 * parent_position) + 2]

            # While max heap priority queue is not valid
            while parent.query_priority < left_child.query_priority \
                    or parent.query_priority < right_child.query_priority:
                if left_child.query_priority > right_child.query_priority:
                    temp = parent
                    self.queue[parent_position] = left_child
                    self.queue[(2 * parent_position) + 1] = temp

                    parent_position = (2 * parent_position) + 1
                    parent = self.queue[parent_position]

                    # If statements prevent index out of bounds errors
                    if ((2 * parent_position) + 1) > len(self.queue) - 1:
                        left_child = Node("", 0)
                        right_child = Node("", 0)
                    elif ((2 * parent_position) + 2) > len(self.queue) - 1:
                        left_child = self.queue[(2 * parent_position) + 1]
                        right_child = Node("", 0)
                    else:
                        left_child = self.queue[(2 * parent_position) + 1]
                        right_child = self.queue[(2 * parent_position) + 2]
                else:
                    temp = parent
                    self.queue[parent_position] = right_child
                    self.queue[(2 * parent_position) + 2] = temp

                    parent_position = (2 * parent_position) + 2
                    parent = self.queue[parent_position]

                    # If statements prevent index out of bounds errors
                    if ((2 * parent_position) + 1) > len(self.queue) - 1:
                        left_child = Node("", 0)
                        right_child = Node("", 0)
                    elif ((2 * parent_position) + 2) > len(self.queue) - 1:
                        left_child = self.queue[(2 * parent_position) + 1]
                        right_child = Node("", 0)
                    else:
                        left_child = self.queue[(2 * parent_position) + 1]
                        right_child = self.queue[(2 * parent_position) + 2]

            return highest_priority.query_priority

    def reheap(self, query):
        """
        Takes a new query and makes a new max heap priority queue
        :param query: Keyword, searched for in each web page
        """
        self.query = query.split()
        self.queue = []

        # determines the priority of all web pages based on keyword(s)
        for page in self.web_pages:
            priority = 0
            for key_word in self.query:
                priority += page.getCount(key_word)
            node = Node(page, priority)
            self.insert(node)

import WebPageIndex
import WebpagePriorityQueue
import os


def readFiles(folder_path):
    """
    Makes a list of all files in a given directory
    :param folder_path: Path to get into directory of files
    :return: List of all files in a given directory
    """
    web_pages = os.listdir(folder_path)
    data = []

    for web_page in web_pages:
        page = WebPageIndex.WebPageIndex(folder_path + "/" + web_page)
        data.append(page)

    return data


def readQueries(q_file):
    """
    Makes a list of queries from a given file
    :param q_file: file that holds queries
    :return: List of queries from a given file
    """
    query_file = open(q_file)
    queries = []
    for query in query_file:
        queries.append(query.replace("\n", ""))

    return queries


def main():
    """
    Processes the priority of every web page for every query
    """
    queries = readQueries("queries (1).txt")
    wppq = WebpagePriorityQueue.WebpagePriorityQueue(queries[0],
                                                     readFiles("data"))
    limit = input("all results[-1] or limited results from 1-" + \
                  str(len(wppq.queue) - 1) + ": ")  # web pages displayed
    print("\n")
    limit = int(limit)
    for query in queries:
        repeat = limit
        wppq.reheap(query)
        print("Query: " + query)
        print("Results ↓")
        if limit == -1 or int(limit) > 8:
            repeat = len(wppq.queue)
            for i in range(repeat):
                top = wppq.peek()
                if top.query_priority == 0:
                    break
                print(top.web_page_index.path.replace("data/", "") + \
                      " | Matches: " + str(top.query_priority))
                wppq.poll()
        elif 8 >= int(limit) > -1:
            for i in range(repeat):
                print(wppq.queue[0].web_page_index.path.replace("data/", ""))
                wppq.poll()

        print("--------------------------------")


# Testing
if __name__ == '__main__':
    main()

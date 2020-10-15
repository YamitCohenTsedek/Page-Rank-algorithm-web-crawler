import requests
import lxml.html
import time
from urllib import robotparser


# A priority queue of URLs.
class UrlsPriorityQueue:
    def __init__(self):
        self.priority_queue = []

    # Return True if the priority queue is empty, otherwise - return False.
    def is_empty(self):
        return len(self.priority_queue) == 0

    # Return True if the priority queue contains dest_url, otherwise - return False.
    def contains(self, dest_url):
        for i in range(0, len(self.priority_queue)):
            if self.priority_queue[i][0] == dest_url:
                return True
        return False

    # Insert a URL to the priority queue.
    def insert(self, dest_url, priority):
        self.priority_queue.append((dest_url, priority))

    # Pop the URL with the highest priority from the priority queue and return it and its priority.
    def pop(self):
        try:
            max = 0
            # Find the URL with the highest priority.
            for i in range(len(self.priority_queue)):
                if self.priority_queue[i][1] > self.priority_queue[max][1]:
                    max = i
            dest_url, priority = self.priority_queue[max]
            # Delete the URL with the highest priority from the priority queue.
            del self.priority_queue[max]
            # Return the URL with the highest priority and its priority.
            return dest_url, priority
        # If the priority queue is empty - print an error message and exit.
        except IndexError:
            print("The priority queue is empty.")
            exit()

    # Delete the given URL from the priority queue.
    # Return a tuple that includes the URL and its priority.
    def delete(self, dest_url):
        try:
            for i in range(0, len(self.priority_queue)):
                item = self.priority_queue[i]
                if item[0] == dest_url:
                    self.priority_queue.remove(item)
                    break
            return item
        # If dest_url is not in the priority queue, print an error message and exit.
        except ValueError:
            print("dest_url is not in the priority queue")
            exit()


# Return True if dest_url was already crawled, otherwise - return False.
def was_url_crawled(dest_url, source_dest_urls):
    # If dest_url is in the source URLs of source_dest_urls, return True since it already has been crawled.
    for current_source_url, current_dest_url in source_dest_urls:
        if current_source_url == dest_url:
            return True
    # Else - return False since dest_url has been not crawled.
    return False


# Return the legal URLs from the current page (the allowed URLs by the robots' policy of Wikipedia, with no repetitions).
def find_current_page_urls(current_src_url, xpaths, source_dest_urls, robots_permissions):
    # Crawling ethics - wait at least 3 seconds between page reads.
    time.sleep(3)
    res = requests.get(current_src_url)  # HTTP GET request.
    doc = lxml.html.fromstring(res.content)  # Parse the html, returning a single document.
    # Set of the URLs found on the current page (set for no repetitions).
    current_page_urls = set()
    # Run over the legal XPath expressions.
    for xpath in xpaths:
        # Run over the results of the current XPath.
        for dest_url in doc.xpath(xpath):
            # Crawling ethics - if dest_url should not be crawled by robots policy of Wikipedia, don't crawl it.
            if not robots_permissions.can_fetch("*", dest_url):
                continue
            # Check whether the current URL starts with the absolute URL of Wikipedia.
            index = dest_url.find("https://en.wikipedia.org")
            # If the current URL doesn't start with the relative or absolute URL of Wikipedia - don't crawl it.
            if not dest_url.startswith("/wiki") and index == -1:
                continue
            # If the current URL is relative URL of Wikipedia, make it an absolute URL of Wikipedia.
            if index == -1:
                dest_url = "https://en.wikipedia.org" + dest_url
            # If the URL wasn't appeared on the current page and wasn't crawled yet, add it to current page URLs.
            if dest_url not in current_page_urls and not was_url_crawled(dest_url, source_dest_urls):
                current_page_urls.add(dest_url)
    return current_page_urls


def add_urls_to_priority_queue(current_src_url, current_page_urls, urls_priority_queue):
    # Run over the current page URLs.
    for dest_url in current_page_urls:
        if urls_priority_queue.contains(dest_url):
            # Delete the found URL from the priority queue and get its priority.
            dest_url, priority = urls_priority_queue.delete(dest_url)
            # Insert the found URL to the priority queue with a priority increased by 1.
            urls_priority_queue.insert(dest_url, priority + 1)
        # Else - insert it to the priority queue with a priority of 1.
        else:
            urls_priority_queue.insert(dest_url, 1)


# Crawl at most 100 URLs (only on Wikipedia) and return a list of lists of source & destination URLs.
def crawl_up_to_100_urls(url, xpaths, source_dest_urls, urls_priority_queue, robots_permissions):
    num_of_crawled_urls = 0
    # A flag which allows entering the loop for the first time, since at first, the priority queue is empty.
    flag = 1
    # The current page that is crawled by the crawler.
    current_src_url = url
    # Iterative implementation to the crawler in which its memory complexity is more efficient than the recursive way.
    while flag or ((not urls_priority_queue.is_empty()) and num_of_crawled_urls < 100):
        flag = 0
        current_page_urls = find_current_page_urls(current_src_url, xpaths, source_dest_urls, robots_permissions)
        # Add the source URL and the destination URL to source_dest_urls list.
        for dest_url in current_page_urls:
            source_dest_urls.append((current_src_url, dest_url))
        # Increase the number of pages that were crawled by 1.
        num_of_crawled_urls += 1
        add_urls_to_priority_queue(current_src_url, current_page_urls, urls_priority_queue)
        if not urls_priority_queue.is_empty():
            # dest_url is the current URL with the highest priority.
            dest_url, priority = urls_priority_queue.pop()
            # Update the current source URL to be the current destination URL with the highest priority.
            current_src_url = dest_url
        else:
            return source_dest_urls
    return source_dest_urls


# param url: a string containing the URL of the start page of the crawling.
# param xpaths: a list of strings representing legal XPath expressions
def crawl(url, xpaths):
    # source_dest_urls is a list of lists- each inner list will contain the full source URL and the full destination URL.
    source_dest_urls = list()
    # A priority queue for crawling the more frequent URLs first.
    urls_priority_queue = UrlsPriorityQueue()
    # Crawling ethics - we should crawl only pages that are allowed by the robots permissions of Wikipedia.
    robots_permissions = robotparser.RobotFileParser()
    robots_permissions.set_url("https://en.wikipedia.org/robots.txt")
    robots_permissions.read()
    # Crawl at most 100 URLs and return the results (source_dest_urls).
    return crawl_up_to_100_urls(url, xpaths, source_dest_urls, urls_priority_queue, robots_permissions)


def main():
    url = "https://en.wikipedia.org/wiki/Andy_Ram"
    xpaths = []
    xpaths.append('//table[contains(@class,"sortable")]/tbody/tr/td[count(../../tr/th[contains(text(),"Partner")]/preceding-sibling::*)+1=position()]/a/@href[contains(.,"/wiki")]')
    xpaths.append('//table[contains(@class,"sortable")]/tbody/tr/td[count(../../tr/th[contains(text(),"Opponent")]/preceding-sibling::*)+1=position()]/a/@href[contains(.,"/wiki")]')
    xpaths.append('//table[@class="infobox vcard"]/tbody//th[contains(text(),"Coach")]/../td//a/@href[contains(.,"/wiki")]')
    xpaths.append('//table[contains(@class,"sortable")]/tbody/tr/td[count(../../tr/th[contains(text(),"Player")]/preceding-sibling::*)+1=position()]/a/@href[contains(.,"/wiki")]')
    xpaths.append('//table[contains(@class,"sortable") or contains(@class,"wikitable")]//span[@class="flagicon"]/../a/@href[contains(.,"/wiki")]')
    print("The crawler began to crawl - it might take a while...")
    urls = crawl(url, xpaths)
    for src_dst in urls:
        print(src_dst)
    return urls


if __name__ == "__main__":
    main()
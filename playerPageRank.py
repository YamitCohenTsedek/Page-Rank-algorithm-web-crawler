import random
import crawler


# Create a dictionary whose keys are source URLs, and the values are lists of all the URLs linked to this source URL.
def create_urls_graph(listOfPairs):
    urls_graph = dict()
    for pair in listOfPairs:
        if pair[0] not in urls_graph.keys():
            urls_graph[pair[0]] = []
        urls_graph[pair[0]].append(pair[1])
    return urls_graph


# Create a set of all the URLs of the graph and return it.
def find_all_urls(listOfPairs):
    set_of_urls = set()
    for pair in listOfPairs:
        set_of_urls.add(pair[0])
        set_of_urls.add(pair[1])
    return tuple(set_of_urls)


# Random surfing - at each step, the surfer decides with probability 0.85 to follow a link
# or with probability 0.15 to jump to a random tennis player, chosen uniformly at random from all the URLs.
def random_surfing(current_src_url, urls_graph, set_of_all_urls, following_probability):
    random_num = random.randint(1, 100)
    if random_num/100 >= following_probability:
        return random.choice(set_of_all_urls)
    else:
        if current_src_url in urls_graph.keys():
            following_urls = urls_graph[current_src_url]
            return random.choice(following_urls)
        # If there are no outgoing links, jump to a random member.
        else:
            return random.choice(set_of_all_urls)


# Find the page ranks of 100,000 steps while updating urls_ranks dictionary.
def find_url_ranks(urls_graph, set_of_all_urls, current_src_url, urls_ranks):
    steps = 100000
    # At each step, the surfer decides with probability 0.85 to follow a link.
    following_probability = 0.85
    for i in range(steps):
        # Increase the number of the visits of the URL.
        if current_src_url in urls_ranks:
            urls_ranks[current_src_url] += 1
        else:
            urls_ranks[current_src_url] = 1
        # Random surfing - the surfer might follow a link or jump to a random tennis player with some probabilities.
        current_src_url = random_surfing(current_src_url, urls_graph, set_of_all_urls, following_probability)
    for url in urls_ranks.keys():
        # The page rank of each member is the number of times it was visited divided by the number of steps.
        urls_ranks[url] = urls_ranks[url] / steps
    return current_src_url


# Return a dictionary whose keys are URLs, and the values are the page ranks
# computed from 2 separate rounds of 100,000 steps.
def playerPageRank(listOfPairs):
    # A dictionary whose keys are source URLs and the values are lists of all the URLs linked to this URL.
    urls_graph = create_urls_graph(listOfPairs)
    # Create dictionaries whose keys are URLs, and their values are the page ranks for two rounds of 100,000 steps.
    first_phase_ranks = dict()
    second_phase_ranks = dict()
    # A dictionary whose keys are URLs and the values are the page ranks computed from the 2 rounds.
    total_ranks = dict()
    set_of_all_urls = find_all_urls(listOfPairs)  # A set of all the URLs in the graph.
    # The process starts from a random node.
    current_src_url = random.choice(tuple(set_of_all_urls))
    # Find the page ranks of the 100,000 first steps while updating first_phase_ranks dictionary.
    # The last URL of the first 100,000 steps is the first URL of the second 100,000 steps.
    current_src_url = find_url_ranks(urls_graph, set_of_all_urls, current_src_url, first_phase_ranks)
    # Find the page ranks of the second 100,000 steps while updating second_phase_ranks dictionary.
    find_url_ranks(urls_graph, set_of_all_urls, current_src_url, second_phase_ranks)
    # Create the dictionary of the total results.
    for url in set_of_all_urls:
        # The page rank of an unvisited page is 0.
        if url not in first_phase_ranks.keys():
            first_phase_ranks[url] = 0
        if url not in second_phase_ranks.keys():
            second_phase_ranks[url] = 0
        total_ranks[url] = (first_phase_ranks[url], second_phase_ranks[url])
    return total_ranks


def playerPageRankTest(listOfPairs):
    urls_graph = create_urls_graph(listOfPairs)
    first_phase_ranks = dict()
    second_phase_ranks = dict()
    total_ranks = dict()
    set_of_all_urls = find_all_urls(listOfPairs)
    current_src_url = random.choice(tuple(set_of_all_urls))
    current_src_url = find_url_ranks(urls_graph, set_of_all_urls, current_src_url, first_phase_ranks)
    find_url_ranks(urls_graph, set_of_all_urls, current_src_url, second_phase_ranks)
    max_rank_first_phase = 0
    url_max_rank_first_phase = None
    max_rank_second_phase = 0
    url_max_rank_second_phase = None
    for url in set_of_all_urls:
        if url not in first_phase_ranks.keys():
            first_phase_ranks[url] = 0
        if url not in second_phase_ranks.keys():
            second_phase_ranks[url] = 0
        total_ranks[url] = (first_phase_ranks[url], second_phase_ranks[url])
        if first_phase_ranks[url] > max_rank_first_phase:
            max_rank_first_phase = first_phase_ranks[url]
            url_max_rank_first_phase = url
        if second_phase_ranks[url] > max_rank_second_phase:
            max_rank_second_phase = second_phase_ranks[url]
            url_max_rank_second_phase = url
    return total_ranks, url_max_rank_first_phase, max_rank_first_phase, url_max_rank_second_phase, max_rank_second_phase


def main():
    list_of_pairs = crawler.main()
    ranks, url_max_rank_first_phase, max_rank_first_phase, url_max_rank_second_phase, max_rank_second_phase = playerPageRankTest(list_of_pairs)
    for url in ranks.keys():
        print(url, ranks[url])
    print("The page with the highest PageRank in the first phase: " + url_max_rank_first_phase + ", rank:" + str(max_rank_first_phase) + "\n"
          + "The page with the highest PageRank in the second phase: " + url_max_rank_second_phase + ", rank:" + str(max_rank_second_phase))


if __name__ == "__main__":
    main()

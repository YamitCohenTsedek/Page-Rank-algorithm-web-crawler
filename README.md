# Page-Rank-algorithm-web-crawler<br/>

## Web Crawler

File crawler.py contains the crawling function, which its signature is: def crawl(url,xpaths).<br/>
The purpose of this function is to crawl pages of tennis players on Wikipedia.<br/>
The input url is a string containing the URL of the start page (e.g., https://en.wikipedia.org/wiki/Andy_Ram).<br/>
The input xpaths is a list of strings representing legal XPath expressions.<br/>
The function uses the xpaths to extract a set of URLs from the web page.<br/>
These URLs are crawled in order of priority - we keep counts for the number of times each URL was found. URLs seen the highest number of times have the highest priority.<br/><br/>
We mind crawling ethics:<br/>
* Waiting at least 3 seconds between page reads.<br/>
* The standard for robot exclusion: robots.txt at the root of a web server - indicates which subfolders can be indexed.
#####
The crawler is implemented in an iterative method, in which its memory complexity is more efficient than the recursive way.<br/><br/>
In total, at most 100 URLs are crawled in this manner and only URLs of en.wikipedia.org. We avoid crawling the same URL twice.<br/>
The function returns a list of lists. Each inner list contains two strings: the first is the full source URL,
and the second is the full URL of a page detected in the source URL by the crawler.<br/>
For example, if /wiki/Jonathan_Erlich was extracted from the page https://en.wikipedia.org/wiki/Andy_Ram, the output will contain the list:
['https://en.wikipedia.org/wiki/Andy_Ram', https://en.wikipedia.org/wiki/Jonathan_Erlich'].<br/>
The output does not contain repeated pairs, even if some link appears on the source page more than once.<br/><br/>


## PageRank Algorithm

File playerPageRank.py contains the PageRank function which its signature is: def playerPageRank(listOfPairs).<br/>
The purpose of this function is to compute a PageRank score for tennis players on Wikipedia.<br/>
listOfPairs is a list of lists in the format of the output of crawler described above - <br/>
['https://en.wikipedia.org/wiki/Andy_Ram', https://en.wikipedia.org/wiki/Jonathan_Erlich']
The function treats each inner list [X, Y] as a link from X to Y.<br/><br/>
We use the random surfer model:<br/>
* The graph nodes are all the URLs in the input.<br/>
* We start from a random node.<br/>
* At each step, the surfer decides with probability 0.85 to follow a link or with probability 0.15 to jump to a random tennis player, chosen uniformly at random from all the URLs in the input.<br/>
* If there are no outgoing links, we jump to a random member.<br/>
* We repeat this process 200,000 steps, and record the number of times we have visited each page in the first 100,000 steps, and in the last 100,000 steps.<br/>
* The PageRank of each member is the number of times it was visited divided by the number of steps.<br/>
The function returns a dict where the keys are URLs and the values are the scores computed from the first and last 100,000 steps, e.g.: {'https://en.wikipedia.org/wiki/Andy_Ram': [0.1,0.09], 'https://en.wikipedia.org/wiki/Jonathan_Erlich': [0.05,0.06] ...}

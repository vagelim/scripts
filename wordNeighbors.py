def wordNeighbors(text, string, n):
    '''Searches for text, and retrieves n words either side of the text, which are returned separately'''
    word = r"\W*([\w]+)"
    groups = re.search(r'{}\W*{}{}'.format(word*n,string ,word*n),text).groups()
    left = list(groups[:n])
    right = list(groups[n:])
    #return groups[:n],groups[n:]
    return left,right

def find_nth(haystack, needle, n):
"""Take a string, haystack, and find the nth occurrence of the substring needle"""
    start = haystack.find(needle)
    while start >= 0 and n > 1:
        start = haystack.find(needle, start+len(needle))
        n -= 1
    return start

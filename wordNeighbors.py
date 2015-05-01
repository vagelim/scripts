def search(text, string, n):
    '''Searches for text, and retrieves n words either side of the text, which are returned separately'''
    word = r"\W*([\w]+)"
    groups = re.search(r'{}\W*{}{}'.format(word*n,string ,word*n),text).groups()
    left = list(groups[:n])
    right = list(groups[n:])
    #return groups[:n],groups[n:]
    return left,right

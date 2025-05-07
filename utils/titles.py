import internetarchive
import re

def get_titles():
    """
    Fetches the titles of items from the Internet Archive.
    """
    # Search for items uploaded by a specific user
    lst = list(internetarchive.search_items(query="uploader:(fqf1fqf@gmail.com) AND identifier:Bilibili-*"))
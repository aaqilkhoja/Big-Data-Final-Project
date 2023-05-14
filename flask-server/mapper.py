#!/usr/bin/env python
"""An advanced Mapper, using Python iterators and generators."""

import sys
import re


def read_input(input, separator='\t'):
    for line in input:
        username = line.split(separator)[0]
        tweet = separator.join(line.split(separator)[1:]).rstrip()
        tweet=re.sub('[^a-zA-Z0-9]', ' ', tweet)
        tweet=tweet.lower()
        yield username, tweet


def main(separator='\t'):
    # input comes from STDIN (standard input)
    data = read_input(sys.stdin)

    for username, tweet in data:
        out = '%s%s%s' % (tweet, separator, username)
        print(out)


# how to test locally in bash/linus: cat <input> | python mapper.py
if __name__ == "__main__":
    main()

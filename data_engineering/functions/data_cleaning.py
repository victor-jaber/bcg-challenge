# ========================================================================== #
### Auxiliary functions for cleaning and processing data
# ========================================================================== #

import re

def remove_header(text, start):
    '''
    Remove the header, that is, starts the extraction from the character 
    specified in the variable start 
    '''
    return text[start:]


def remove_end(text, end):
    '''
    Remove end of file. In general, it is the page number
    '''
    if end == 0:
        return text
    return text[:end]


def remove_unwanted_chr(text, chr):
    '''
    Replaces all occurrences of chr in the text with ' '
    '''
    for x in chr:
        text = re.sub(x, ' ', text)
    return text
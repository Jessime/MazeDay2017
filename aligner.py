"""
This is not our code. It was taken and adapted from:

http://hipersayanx.blogspot.com/2012/07/sequences-alignment-in-python.html
http://hipersayanx.blogspot.com.ar/2012/07/longest-common-subsequence-in-python.html
"""

def lcs(a, b):
    if a == [] or b == []:
        return []
 
    l = len(a) + len(b) - 1
 
    # Fill non-comparable elements with null spaces.
    sa = a + (len(b) - 1) * ['']
    sb = (len(a) - 1) * [''] + b
 
    longest = []
 
    for k in range(l):
        cur = []
 
        for c in range(l):
            if sa[c] != '' and sb[c] != '' and sa[c] == sb[c]:
                cur.append(sa[c])
            else:
                if len(cur) > len(longest):
                    longest = cur
 
                cur = []
 
        if len(cur) > len(longest):
            longest = cur
 
        if sa[len(sa) - 1] == '':
            # Shift 'a' to the right.
            sa = [''] + sa[: len(sa) - 1]
        else:
            # Shift 'b' to the left.
            sb = sb[1:] + ['']
 
    return longest
    
def findSubList(l, sub):
    if len(sub) > len(l):
        return -1
 
    for i in range(len(l) - len(sub) + 1):
        j = 0
        eq = True
 
        for s in sub:
            if l[i + j] != s:
                eq = False
 
                break
 
            j += 1
 
        if eq:
            return i
 
    return -1
 
def alignSequences(sequence1, sequence2):
    #Takes two lists
    # lcs is the Longest Common Subsequence function.
    cs = lcs(sequence1, sequence2)
 
    if cs == []:
        return sequence1 + [''] * len(sequence2) , \
               [''] * len(sequence1) + sequence2
    else:
        # Remainings non-aligned sequences in the left side.
        left1 = sequence1[: findSubList(sequence1, cs)]
        left2 = sequence2[: findSubList(sequence2, cs)]
 
        # Remainings non-aligned sequences in the right side.
        right1 = sequence1[findSubList(sequence1, cs) + len(cs):]
        right2 = sequence2[findSubList(sequence2, cs) + len(cs):]
 
        # Align the sequences in the left and right sides:
        leftAlign = alignSequences(left1, left2)
        rightAlign = alignSequences(right1, right2)
 
        return leftAlign[0] + cs + rightAlign[0], \
               leftAlign[1] + cs + rightAlign[1]
 

def align_strings(str1, str2):
    a,b = alignSequences(list(str1), list(str2))
    new_str1 = ''.join(['-' if i == '' else i for i in a])
    new_str2 = ''.join(['-' if j == '' else j for j in b])
    return new_str1, new_str2
    
if __name__ == '__main__': 
    a, b = alignSequences(list('abcdfghjqz'), list('abcdefgijkrxyz'))
    print(''.join(['-' if i == '' else i for i in a]))
    print(''.join(['-' if j == '' else j for j in b]))
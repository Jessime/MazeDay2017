# -*- coding: utf-8 -*-
"""
Created on Fri Aug 19 21:05:49 2016

@author: jessime
"""

class Dialog():

    def __init__(self):
        self.dict = self.load()

    def say(self, key, **kwargs):
        for line in self.dict[key]:
            print(line.format(**kwargs))

    def load(self):
        dialog = {}
        header = ''
        saying = []
        with open('data/dialog.txt') as infile:
            for i, line in enumerate(infile):
                if line[0] == '>':
                    if saying:
                        dialog[header] = saying
                        saying = []
                    else:
                        assert i == 0, 'There may be a header without a saying at line {}.'.format(i)
                    header = line[1:].strip()
                elif line[0] == '#':
                    pass
                else:
                    saying.append(line.strip())
            dialog[header]= saying
        return dialog


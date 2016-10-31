#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 13 23:51:49 2016

@author: jessime
"""
import argparse

from pvsz_game.plants_vs_zombies import PvsZ

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-n', '--num_lvls', default=3, type=int, help='The number of levels you want to play')
    parser.add_argument('-v', '--verbose', action='store_true', help='Print information to help with debugging.')
    parser.add_argument('-po', '--print_only', action='store_true', help='Set if you do not want to use sound-based sentences')
    parser.add_argument('-np', '--no_printing', action='store_true', help='Set if you do not want information printed to the console.')
    args = parser.parse_args()

    game = PvsZ(num_lvls=args.num_lvls, print_only=args.print_only, no_printing=args.no_printing)
    game.model.run()
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 18 20:25:36 2016

@author: JMK
"""
from .. import plants
from .. import zombies
from .. import plants_vs_zombies


def test_peashooter_shot():
    board = plants_vs_zombies.Board()
    pea_shooter = plants.PeaShooter([0, 0], board)
    zombie = zombies.Zombie(0, [0, 99], board)
    fresh_zombie = zombies.Zombie(0, [1, 99], board)
    original_health = zombie.health
    pea_shooter.produce(pea_shooter.time_til_reload)
    assert zombie.health == (original_health - pea_shooter.damage)
    assert fresh_zombie.health == original_health

def test_cherry_explode():
    board = plants_vs_zombies.Board()
    pos_ls = [[1, 10],
              [1, 11+5],
              [1, 12],
              [2, 10],
              [2, 11],
              [2, 12],
              [3, 10],
              [3, 11-5],
              [3, 12]]
    zombie_ls = [zombies.Zombie(0, p, board) for p in pos_ls]
    original_health = zombie_ls[0].health
    fresh_zombie = zombies.Zombie(0, [0,9], board)
    cherry = plants.CherryBomb([2, 11], board)
    cherry.produce(cherry.time_to_detonate)
    assert all([z.health == (original_health - cherry.damage) for z in zombie_ls])
    assert fresh_zombie.health == original_health
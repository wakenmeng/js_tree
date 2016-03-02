# -*- coding: utf-8 -*-

import sys
import os
from os.path import dirname, realpath
sys.path.append(dirname(dirname(realpath(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cto_tree.settings")

from random import randint
from time import sleep

from cto_tree.models import CTONode

def generate_test_data():
    limit = 90
    parents_num = 3
    parents = [CTONode.create(None, name='p_%d' % i) for i in range(parents_num)]
    while limit > 0:
        for p in parents:
            nodes = [CTONode.create(p.id, name='ch_%d' % chi) for chi in range(randint(1, 3))]
            for node in nodes:
                node.income(randint(500, 2000))
            parents.extend(nodes)
            limit -= 1
            if limit < 0:
                return


if __name__ == '__main__':
    generate_test_data()


import argparse
import sys
import logging
import random
import math
import reapy
from randomcolor import RandomColor


def randColorByHue(hue):
    rcg = RandomColor().generate(hue=hue, count=1)[0]
    c = rcg.lstrip('#')
    return tuple(int(c[i:i+2], 16) for i in (0, 2, 4))

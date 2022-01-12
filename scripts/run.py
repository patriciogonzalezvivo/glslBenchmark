#!/usr/bin/env python3

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import os
import sys
import json
import yaml

from benchmark import benchmark

if __name__ == '__main__':    
    if len(sys.argv) > 1:
        if sys.argv[1]:
            TEST_FILE = sys.argv[1]

    with open( TEST_FILE ) as f:
        config = yaml.load(f, Loader=yaml.FullLoader)

        data = []
        for test in config["tests"].keys():
            print(test)
            print(config["tests"][test])
            print("----------------")
            data.append( benchmark( test, config["tests"][test]["fragment"], config["tests"][test]["options"] ) )

        with open(config["output"], 'w') as outfile:
            json.dump(data, outfile)

#!/usr/bin/env python3

import subprocess
import sys


subprocess.run(['scrapy', 'runspider', sys.argv[1], '-O', sys.argv[1].replace('.py', '_result.json')])   
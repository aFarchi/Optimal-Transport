#!/usr/bin/env python 

from OT.utils.sys.argv                       import extractArgv
from OT.OTObjects1D.configuration            import Configuration
from OT.OTObjects1D.analyse.computeOperators import applyAllOperators

# Extract Arguments
arguments      = extractArgv()

try:
    configFile = arguments['CONFIG_FILE']
    config     = Configuration(configFile)
    outputDir  = config.outputDir
except:
    outputDir  = arguments['OUTPUT_DIR']

# Analyse
applyAllOperators(outputDir)

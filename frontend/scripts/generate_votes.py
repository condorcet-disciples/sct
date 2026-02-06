#!/usr/bin/env python3
"""
Generate random votes using the SCT randomization module.
Called by the Node.js backend.
"""

import sys
import os
import json
import argparse

# Add parent directory to path to import sct module
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from sct.randomization import PreferenceGenerator


def main():
    parser = argparse.ArgumentParser(description='Generate random voter preferences')
    parser.add_argument('--num-agents', type=int, default=10, help='Number of agents to generate')
    parser.add_argument('--strategy', type=str, default='biased', 
                        choices=['random', 'clustered', 'biased'],
                        help='Generation strategy')
    parser.add_argument('--seed', type=int, default=0, help='Random seed for reproducibility')
    
    args = parser.parse_args()
    
    generator = PreferenceGenerator(strategy=args.strategy)
    agents = generator.generate(
        num_agents=args.num_agents,
        num_candidates=4,
        seed=args.seed
    )
    
    # Output as JSON
    print(json.dumps(agents))


if __name__ == '__main__':
    main()

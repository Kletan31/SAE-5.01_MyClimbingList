#!/usr/bin/env python3
"""Depuis la racine : python3 scripts/check_demo_https.py --ca /chemin/rootCA.pem"""
import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from lib.demo_https import check_demo

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--ca', required=True, help='Certificat public rootCA.pem de mkcert (pas sa clé).')
args = parser.parse_args()
check_demo(args.ca)

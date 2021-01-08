#!/usr/bin/env python3
"""
Deploys support infrastructure.

Decrypts secrets from sops safely.
"""
import tempfile
import subprocess

with tempfile.NamedTemporaryFile() as f:
    subprocess.check_call([
        'sops',
        '--output', f.name,
        '--decrypt', 'secrets/support.yaml'
    ])
    subprocess.check_call([
        'helm', 'upgrade', '--install', '--wait',
        '--namespace=support', 'support', 'support/',
        '-f', f.name
    ])

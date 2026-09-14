#!/usr/bin/env python
"""
Apply cgm-local Red9 patches from manifest.json to a target Red9 tree.

Default target: sibling cgmToolsPy3/Red9 relative to this script's repo layout.
"""
from __future__ import print_function

import argparse
import json
import os
import sys


def _default_target():
    here = os.path.dirname(os.path.abspath(__file__))
    # cgmToolsDev/Patches/Red9 -> cgmToolsDev -> sibling cgmToolsPy3/Red9
    dev_root = os.path.dirname(os.path.dirname(here))
    py3_root = os.path.join(os.path.dirname(dev_root), 'cgmToolsPy3')
    return os.path.join(py3_root, 'Red9')


def _load_manifest(manifest_path):
    with open(manifest_path, 'r') as handle:
        data = json.load(handle)
    return data.get('patches', [])


def _apply_edit(target_root, edit, dry_run=False):
    rel_path = edit['file']
    find_text = edit['find']
    replace_text = edit['replace']
    expected_count = int(edit.get('count', 1))

    file_path = os.path.join(target_root, rel_path.replace('/', os.sep))
    if not os.path.isfile(file_path):
        return False, 'missing file: {0}'.format(file_path)

    with open(file_path, 'r') as handle:
        original = handle.read()

    actual_count = original.count(find_text)
    if actual_count != expected_count:
        return False, '{0}: expected {1} match(es) for find string, found {2}'.format(
            rel_path, expected_count, actual_count)

    updated = original.replace(find_text, replace_text)
    if updated == original:
        return False, '{0}: replace produced no change'.format(rel_path)

    if dry_run:
        return True, '{0}: dry-run OK ({1} replacement(s))'.format(rel_path, expected_count)

    with open(file_path, 'w') as handle:
        handle.write(updated)

    return True, '{0}: applied ({1} replacement(s))'.format(rel_path, expected_count)


def apply_patches(target_root, manifest_path, patch_id=None, dry_run=False):
    patches = _load_manifest(manifest_path)
    if patch_id:
        patches = [p for p in patches if p.get('id') == patch_id]
        if not patches:
            print('No patch with id: {0}'.format(patch_id), file=sys.stderr)
            return 1

    if not os.path.isdir(target_root):
        print('Target Red9 tree not found: {0}'.format(target_root), file=sys.stderr)
        return 1

    failures = 0
    for patch in patches:
        pid = patch.get('id', '<unknown>')
        print('[{0}] {1}'.format(pid, patch.get('summary', '')))
        for edit in patch.get('edits', []):
            ok, message = _apply_edit(target_root, edit, dry_run=dry_run)
            prefix = '  OK' if ok else '  FAIL'
            print('{0}: {1}'.format(prefix, message))
            if not ok:
                failures += 1

    if failures:
        print('\n{0} edit(s) failed.'.format(failures), file=sys.stderr)
        return 1

    mode = 'dry-run' if dry_run else 'applied'
    print('\nAll patches {0} successfully.'.format(mode))
    return 0


def main(argv=None):
    parser = argparse.ArgumentParser(description='Apply cgm-local Red9 patches from manifest.json')
    parser.add_argument(
        '--target',
        default=_default_target(),
        help='Path to Red9 tree (default: sibling cgmToolsPy3/Red9)',
    )
    parser.add_argument(
        '--manifest',
        default=os.path.join(os.path.dirname(os.path.abspath(__file__)), 'manifest.json'),
        help='Path to manifest.json',
    )
    parser.add_argument('--id', dest='patch_id', default=None, help='Apply a single patch id')
    parser.add_argument('--dry-run', action='store_true', help='Validate and report without writing')
    args = parser.parse_args(argv)

    return apply_patches(
        target_root=os.path.normpath(args.target),
        manifest_path=os.path.normpath(args.manifest),
        patch_id=args.patch_id,
        dry_run=args.dry_run,
    )


if __name__ == '__main__':
    sys.exit(main())

#!/usr/bin/env python
#
# CLI tool to upload file to GIST, list existing GISTs, or download from GIST using Github API
# Upload, List existing GISTs or Download from GIST. encodes to base64 and decodes to original file
# Modified from original by Puru Tuladhar: https://github.com/tuladhar/gistup
#
import getpass
import os
import sys
import json
import urllib.request
import argparse
import base64
import re

usage = (
    "CLI tool to transfer any file up to 25MB using Github GIST API\n"
    "Upload, List existing GISTs or Download from GIST. encodes to base64 and decodes to original file.\n\n"
    "Usage\n\n"
    "Upload:\n"
    "python gist_transfer.py -u -f path/to/file.zip -t YOUR_TOKEN\n\n"
    "List files:\n"
    "python gist_transfer.py -l -t YOUR_TOKEN\n\n"
    "Download:\n"
    "python gist_tool.py -down -g https://gist.github.com/someuser/abcdef1234567890 -t YOUR_TOKEN\n\n"
    "If the -t parameter is omitted, an input field will request the token.\n\n"
)

def parse_args():
    parser = argparse.ArgumentParser(usage=usage)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-u', '--upload', action='store_true', help='upload mode')
    group.add_argument('-l', '--list', action='store_true', help='list existing gists')
    group.add_argument('-d', '--download', action='store_true', help='download mode')
    parser.add_argument('-f', '--filename', dest='filename', help='filename for upload')
    parser.add_argument('-D', '--description', dest='description', default=None, help='optional description for upload')
    parser.add_argument('-t', '--token', dest='token', help='personal access token generated from your github account')
    parser.add_argument('--public', dest='public', action='store_true', default=False,
                        help='toggle to make this gist available publicly during upload')
    parser.add_argument('-g', '--gist', dest='gist', help='Gist URL or ID for download')
    return parser.parse_args()


def upload(token, filename, description, make_public):
    description = description if description else 'uploaded via gist_transfer.py'

    try:
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()
        is_binary = False
    except UnicodeDecodeError:
        with open(filename, 'rb') as f:
            content = base64.b64encode(f.read()).decode('utf-8')
        is_binary = True

    if is_binary:
        description += ' (base64 encoded binary file)'
        base_filename = os.path.basename(filename)
        gist_filename = base_filename + '.base64'
    else:
        gist_filename = os.path.basename(filename)

    post = json.dumps({
        'description': description,
        'public': make_public,
        'files': {
            gist_filename: {
                'content': content
            }
        }
    })
    post = str(post).encode('utf-8')
    try:
        api_url = 'https://api.github.com/gists'
        req = urllib.request.Request(url=api_url, headers={'Authorization': 'token ' + token}, data=post)
        res = urllib.request.urlopen(req)
        url = json.loads(res.read())
        print(url['html_url'])
    except Exception as upload_error:
        print(upload_error)
        sys.exit(1)


def list_gists(token):
    try:
        api_url = 'https://api.github.com/gists'
        req = urllib.request.Request(url=api_url, headers={'Authorization': 'token ' + token})
        res = urllib.request.urlopen(req)
        gists = json.loads(res.read())
        for gist in gists:
            print(f"{gist['html_url']} - {gist['description'] or 'No description'}")
    except Exception as list_error:
        print(list_error)
        sys.exit(1)


def download_gist(token, gist):
    # Extract gist_id from URL or ID
    match = re.search(r'([a-f0-9]{32})', gist)
    if match:
        gist_id = match.group(1)
    else:
        print('Invalid Gist URL or ID')
        sys.exit(1)

    api_url = f'https://api.github.com/gists/{gist_id}'
    req = urllib.request.Request(url=api_url, headers={'Authorization': 'token ' + token})
    try:
        res = urllib.request.urlopen(req)
        data = json.loads(res.read())
    except Exception as e:
        print(e)
        sys.exit(1)

    for filename, file_info in data['files'].items():
        raw_url = file_info['raw_url']
        req_raw = urllib.request.Request(raw_url)
        res_raw = urllib.request.urlopen(req_raw)
        content = res_raw.read()

        if filename.endswith('.base64'):
            try:
                content = base64.b64decode(content)
                filename = filename[:-7]  # remove .base64
            except Exception as decode_error:
                print(f'Failed to decode base64 for {filename}: {decode_error}')
                continue

        with open(filename, 'wb') as f:
            f.write(content)
        print(f'Downloaded {filename}')


def main():
    args = parse_args()
    if args.token:
        token = args.token
    else:
        token = getpass.getpass("Enter your GitHub token: ")
    if args.upload:
        filename = args.filename
        if not filename:
            print('filename is required for upload')
            sys.exit(1)
        if not os.path.exists(filename):
            print('file not found: {}'.format(filename))
            sys.exit(1)
        description = args.description
        make_public = args.public
        upload(token, filename, description, make_public)
    elif args.list:
        list_gists(token)
    elif args.download:
        if not args.gist:
            print('Gist URL or ID is required for download')
            sys.exit(1)
        download_gist(token, args.gist)
    sys.exit(0)


if __name__ == '__main__':
    main()

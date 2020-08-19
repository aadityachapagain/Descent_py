"""
Download and preprocess reddit datasets from pushshit.io
and store dataset in gcp
"""

import requests
from bs4 import BeautifulSoup
import os
from collections import defaultdict
import hashlib
import tqdm
import time
import logging
import shutil
import argparse
import bz2
import json
import lzma
import zstandard as zstd
import io
from langdetect import detect
from unmark.main import unmark
import re
import traceback 

parser = argparse.ArgumentParser(description='download reddit datasets from pushshift.io')
parser.add_argument('--dpath', type=str,
                    help= 'destination path to download datasets')
args = parser.parse_args()


logger = logging.getLogger("main")
FORMAT = '%(asctime)-15s %(name)s %(levelname)s %(message)s'
logging.basicConfig(format=FORMAT)
logger.setLevel("INFO")

data_ext = ['.bz2', '.xz','.zst']
reddit_link = "https://files.pushshift.io/reddit/submissions/"
datasets_link = defaultdict(lambda : {})
hash_link = 'https://files.pushshift.io/reddit/submissions/sha256sums.txt'

def find_url(string): 
  
    # findall() has been used  
    # with valid conditions for urls in string 
    regex = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
    url = re.findall(regex,string)       
    return [x[0] for x in url]

def preprocess_handler(dpath: str):
    logger.info(f"pre-processing {dpath}")
    if dpath.lower().endswith('.bz2'):
        read_bz2_dataset(dpath)
    elif dpath.lower().endswith('.xz'):
        read_lzma_dataset(dpath)
    elif dpath.lower().endswith('.zst'):
        read_zstandered_data(dpath)
    else:
        logger.info("File not supported ... ")

    logger.info(f"Done preprocessing {dpath} to {''.join(dpath.split('.')[:-1]) +'.txt'}")

def preprocess_text(data: dict):
    # check if sumbission is over 18 or not
    if data['over_18']:
        return False
    # convert markdown to plain text
    text = unmark(data['selftext'].strip())

    # check if there is any url or not
    if len(find_url(text)) > 0:
        return False
    if text.strip() == '':
        return False
    if len(text.strip()) <= 5:
        return False
    # check if text start with non-ASCII character
    if text.strip().lower() == '[deleted]' or text.strip().lower() == '[removed]':
        return False
    if ord(text[0]) > 128:
        return False
    # remove mulitple spaces into single space
    text = re.sub('\s+',' ',text)
    if detect(text) != 'en':
        return False
    # check if there is no spaces in text and no of characeters in it is more than 2040
    if ' ' not in text and len(text) > 2040:
        return False
    return text
    

def read_bz2_dataset(path):
    new_path = ''.join(path.split('.')[:-1]) +'.txt'
    with open(new_path, 'w') as fw:
        with bz2.open(path) as fp:
            for line in fp:
                try:
                    line = json.loads(line.decode("utf-8"))
                    line = preprocess_text(line)
                    if line:
                        fw.write(line + '\n')
                except:
                    traceback.print_exc()
                    logger.info(f'getting error at line  {line}')
                    

def read_lzma_dataset(path):
    new_path = ''.join(path.split('.')[:-1]) +'.txt'
    with open(new_path, 'w') as fw:
        with lzma.open(path) as compressed:
            for line in compressed:
                try:
                    line = json.loads(line.decode("utf-8"))
                    line = preprocess_text(line)
                    if line:
                        fw.write(line + '\n')
                except:
                    traceback.print_exc()
                    logger.info(f'getting error at line  {line}')

def read_zstandered_data(path):
    new_path = ''.join(path.split('.')[:-1]) +'.txt'
    with open(new_path, 'w') as fw:
        with open(path, 'rb') as fh:
            dctx = zstd.ZstdDecompressor()
            stream_reader = dctx.stream_reader(fh)
            text_stream = io.TextIOWrapper(stream_reader, encoding='utf-8')

            for line in text_stream:
                try:
                    line = json.loads(line)
                    line = preprocess_text(line)
                    if line:
                        fw.write(line + '\n')
                except:
                    traceback.print_exc()
                    logger.info(f'getting error at line  {line}')

def download(url, path, fname, redownload=False, num_retries=5):
    """
    Download file using `requests`.

    If ``redownload`` is set to false, then will not download tar file again if it is
    present (default ``False``).
    """
    outfile = os.path.join(path, fname)
    if not os.path.isdir(os.path.dirname(outfile)):
        os.makedirs(os.path.dirname(outfile))
    download = not os.path.isfile(outfile) or redownload
    logger.info(f"Downloading {url} to {outfile}")
    retry = num_retries
    exp_backoff = [2 ** r for r in reversed(range(retry))]

    pbar = tqdm.tqdm(unit='B', unit_scale=True, desc='Downloading {}'.format(fname))

    while download and retry > 0:
        resume_file = outfile + '.part'
        resume = os.path.isfile(resume_file)
        if resume:
            resume_pos = os.path.getsize(resume_file)
            mode = 'ab'
        else:
            resume_pos = 0
            mode = 'wb'
        response = None

        with requests.Session() as session:
            try:
                header = (
                    {'Range': 'bytes=%d-' % resume_pos, 'Accept-Encoding': 'identity'}
                    if resume
                    else {}
                )
                response = session.get(url, stream=True, timeout=5, headers=header)

                # negative reply could be 'none' or just missing
                if resume and response.headers.get('Accept-Ranges', 'none') == 'none':
                    resume_pos = 0
                    mode = 'wb'

                CHUNK_SIZE = 32768
                total_size = int(response.headers.get('Content-Length', -1))
                # server returns remaining size if resuming, so adjust total
                total_size += resume_pos
                pbar.total = total_size
                done = resume_pos

                with open(resume_file, mode) as f:
                    for chunk in response.iter_content(CHUNK_SIZE):
                        if chunk:  # filter out keep-alive new chunks
                            f.write(chunk)
                        if total_size > 0:
                            done += len(chunk)
                            if total_size < done:
                                # don't freak out if content-length was too small
                                total_size = done
                                pbar.total = total_size
                            pbar.update(len(chunk))
                    break
            except (
                requests.exceptions.ConnectionError,
                requests.exceptions.ReadTimeout,
            ):
                retry -= 1
                pbar.clear()
                if retry > 0:
                    pl = 'y' if retry == 1 else 'ies'
                    logger.debug(
                        f'Connection error, retrying. ({retry} retr{pl} left)'
                    )
                    time.sleep(exp_backoff[retry])
                else:
                    logger.error('Retried too many times, stopped retrying.')
            finally:
                if response:
                    response.close()
    if retry <= 0:
        raise RuntimeError('Connection broken too many times. Stopped retrying.')

    if download and retry > 0:
        pbar.update(done - pbar.n)
        if done < total_size:
            raise RuntimeError(
                f'Received less data than specified in Content-Length header for '
                f'{url}. There may be a download problem.'
            )
        move(resume_file, outfile)

    pbar.close()
    return outfile

def move(path1, path2):
    """
    Rename the given file.
    """
    shutil.move(path1, path2)


class DownloadableFile:
    """
    A class used to abstract any file that has to be downloaded online.

    Any task that needs to download a file needs to have a list RESOURCES
    that have objects of this class as elements.

    This class provides the following functionality:

    - Download a file from a URL / Google Drive
    - Untar the file if zipped
    - Checksum for the downloaded file
    - Send HEAD request to validate URL or Google Drive link

    An object of this class needs to be created with:

    - url <string> : URL or Google Drive id to download from
    - file_name <string> : File name that the file should be named
    - hashcode <string> : SHA256 hashcode of the downloaded file
    - zipped <boolean> : False if the file is not compressed
    - from_google <boolean> : True if the file is from Google Drive
    """

    def __init__(self, url, file_name, hashcode, zipped=True, from_google=False):
        self.url = url
        self.file_name = file_name
        self.hashcode = hashcode
        self.compressed = zipped
        self.from_google = from_google

    def checksum(self, dpath):
        """
        Checksum on a given file.

        :param dpath: path to the downloaded file.
        """
        sha256_hash = hashlib.sha256()
        with open(os.path.join(dpath, self.file_name), "rb") as f:
            for byte_block in iter(lambda: f.read(65536), b""):
                sha256_hash.update(byte_block)
            if sha256_hash.hexdigest() != self.hashcode:
                # remove_dir(dpath)
                raise AssertionError(
                    f"[ Checksum for {self.file_name} from \n{self.url}\n"
                    "does not match the expected checksum. Please try again. ]"
                )
            else:
                logger.debug("Checksum Successful")

    def download_file(self, dpath):
        out_file = download(self.url, dpath, self.file_name)

        if self.hashcode:
            self.checksum(dpath)

        # if self.compressed:
        #     extract(dpath, self.file_name)
        return out_file

def collect_hash():
    res = requests.get(hash_link)
    hashes = res.content.decode("utf-8").strip()
    for hash_to_file in hashes.split('\n'):
        hash_to_file = hash_to_file.strip().split()
        datasets_link[hash_to_file[1]]['hash'] = hash_to_file[0]

def is_recommended_link(link):
    for ext in data_ext:
        if link.endswith(ext):
            return link
    return False

def get_all_downloadable_links():
    res = requests.get(reddit_link)
    content = BeautifulSoup(res.content, 'html5lib')
    for link in content.find_all('a'):
        _link = link.get('href')
        _link = is_recommended_link(_link)
        if _link:
            _link = os.path.split(_link)[-1]
            datasets_link[_link]['link'] = os.path.join(reddit_link, _link)


if __name__ == "__main__":
    collect_hash()
    download_path = args.dpath
    get_all_downloadable_links()
    for k,v in datasets_link.items():
        if v.get('link', False):
            fd = DownloadableFile(
                v['link'], k, None
            )
            outfile = fd.download_file(args.dpath)
            preprocess_handler(outfile)



"""
data preprocesss
* convert markup to plain text checked
* Remove comments/posts from Bots checked
* Remove comments/posts from non-English checked
* remove comments/posts marked as delete or removed checked
* remove comments/posts longer than 128 BPE tokens. will do this during loading data in model using tokenizer
* remove longer than 2040 characters and doesnot contain spaces. checked
* remove Shorter than 5 character. checked
* remove comments/posts with contains a URL. checked
* remove comments/posts starts with a non-ASCII. checked 
* remove comments further than depth 7 in the thread. since we are not pretraining we might not need this
* remove child unsafe  posts and comments. checked

"""
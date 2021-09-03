from aws_setup import App, smart_setup, delete_all
from multiprocessing import Pool
import os
import os.path
from os import path
import time
from traceback import print_exc

SLEEP_MULTIPLIER = 0.1
FILE_DIR = 'files'


def process_init():
    global aws
    aws = smart_setup()

def process_message(filename):
    script_dir = os.path.dirname(os.path.realpath(__file__))
    destination = os.path.join(script_dir, FILE_DIR, filename)
    destination_processed = destination + ".proc.txt"
    try:
        print("Downloading", filename)
        aws.bucket.download_file(filename, destination)
        with open(destination) as f,  open(destination_processed, 'w') as fout:
            lines = f.readlines()
            fout.writelines(reversed(list(map(lambda l: l[::-1], lines))))
            linecount = len(lines)
            time.sleep(linecount*SLEEP_MULTIPLIER) # simulate load
        print("Uploading processed", filename)
        aws.bucket.upload_file(destination_processed, filename + ".proc.txt", ExtraArgs={'ACL':'public-read'})
        os.remove(destination)
        os.remove(destination_processed)
        return True
    except:
        print("Error when processing message", filename)
        print_exc()
        return False

def main():
    files_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), FILE_DIR)
    if not path.isdir(files_dir):
        os.mkdir(files_dir)
    aws = smart_setup()
    with Pool(processes=os.cpu_count(), initializer=process_init) as pool:
        while True:
            messages = list(aws.queue.receive_messages(
                WaitTimeSeconds=20,
                MaxNumberOfMessages=min(10,os.cpu_count()) # api can handle 10 at most
            ))
            file_list = list(map(lambda m: m.body, messages))
            if(len(messages)):
                results = pool.map(process_message, file_list)
                for i, r in enumerate(results):
                    if r:
                        messages[i].delete()


if __name__ == "__main__":
    main()
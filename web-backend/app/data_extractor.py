import multiprocessing
import time

def worker_function(uid, files):
    print("Processing files for", uid, files)

def process_files(uid, files):
    process = multiprocessing.Process(target=worker_function, args=(uid, files))
    process.start()

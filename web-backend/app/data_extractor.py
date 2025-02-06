import multiprocessing
import time

import sys
# Path to the folder you want to add
folder_path = '../../llm_agent_workflows/'
# Add the folder to sys.path if it's not already there
if folder_path not in sys.path:
    sys.path.append(folder_path)

def worker_function(uid, files):
    print("Processing files for", uid, files)
    from llm_agent_workflows.tools.evidence_handler import EvidenceHandler
    e = EvidenceHandler()
    for type, file in files.items():
        e.process_evidence(file, "", uid)
        return


def process_files(uid, files):
    process = multiprocessing.Process(target=worker_function, args=(uid, files))
    process.start()

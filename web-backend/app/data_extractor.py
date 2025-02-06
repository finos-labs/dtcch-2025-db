import multiprocessing
import time

import sys
sys.path.append('../../llm_agent_workflows/')
sys.path.append("../")
sys.path.append("../..")

def worker_function(uid, files):
    print("Processing files for", uid, files)
    from llm_agent_workflows.tools.evidence_handler import EvidenceHandler
    e = EvidenceHandler()
    for type, files in files.items():
        for file in files:
            e.process_evidence(file, "", uid)
            return


def process_files(uid, files):
    process = multiprocessing.Process(target=worker_function, args=(uid, files))
    process.start()

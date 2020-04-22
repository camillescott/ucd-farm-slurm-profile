#!/usr/bin/env python3
import re
import subprocess as sp
import shlex
import sys
import time
import logging

logger = logging.getLogger("__name__")

STATUS_ATTEMPTS = 20

jobid = sys.argv[1]

for i in range(STATUS_ATTEMPTS):

    try:
        sctrl_res = sp.check_output(
            shlex.split("scontrol -o show job {}".format(jobid))
        )
        m = re.search("JobState=(\w+)", sctrl_res.decode())
        res = {jobid: m.group(1)}
        break
    except sp.CalledProcessError as e:
        if i >= STATUS_ATTEMPTS - 1:
            print("scontrol status checks failed", file=sys.stderr)
            exit(0)
        else:
            time.sleep(1)

status = res[jobid]

if status == "BOOT_FAIL":
    print("failed")
    logger.error('{jobid} cluster error: BOOT_FAIL'.format(jobid=jobid))

elif status == "OUT_OF_MEMORY":
    print("failed")
    logger.error('{jobid} resource error: OUT_OF_MEMORY'.format(jobid=jobid))

elif status.startswith("CANCELLED"):
    print("failed")
    logger.error('{jobid} scheduling error: CANCELLED'.format(jobid=jobid))

elif status == "COMPLETED":
    logger.error('{jobid} success: COMPLETED'.format(jobid=jobid))
    print("success")

elif status == "DEADLINE":
    logger.error('{jobid} scheduling error: DEADLINE'.format(jobid=jobid))
    print("failed")

elif status == "FAILED":
    print("failed")
    logger.error('{jobid} error: FAILED'.format(jobid=jobid))

elif status == "NODE_FAIL":
    print("failed")
    logger.error('{jobid} cluster error: NODE_FAIL'.format(jobid=jobid))

elif status == "PREEMPTED":
    print("failed")
    logger.error('{jobid} scheduling error: PREEMPTED'.format(jobid=jobid))

elif status == "TIMEOUT":
    print("failed")
    logger.error('{jobid} scheduling error: TIMEOUT'.format(jobid=jobid))

# Unclear whether SUSPENDED should be treated as running or failed
elif status == "SUSPENDED":
    print("failed")
    logger.error('{jobid} scheduling error: SUSPENDED'.format(jobid=jobid))

else:
    print("running")

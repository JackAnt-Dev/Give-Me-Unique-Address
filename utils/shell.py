from utils.logger import logger
import subprocess


def execute(cmd: str, input=""):

    process = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                               stderr=subprocess.STDOUT, encoding='utf8')

    stdout, err = process.communicate(input)

    rc = process.poll()
    return stdout

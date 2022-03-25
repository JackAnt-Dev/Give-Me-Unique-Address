from utils.shell import execute
import re
from utils.logger import logger


def recover_address_by_derivation_path(change_index: int, address_index: int, word_list: list[str]) -> str:
    cmd = f'solana-keygen recover "prompt://?key={change_index}/{address_index}"'
    seedphrase = ' '.join(word_list)
    message = seedphrase
    stdout = execute(cmd, input=message)
    match = re.findall(pattern=r"`([\S]+)`", string=stdout)
    return match[0]


if __name__ == '__main__':
    word_list = [   # mnemonics for test
        "cause",
        "key",
        "cash",
        "prison",
        "guilt",
        "wrap",
        "young",
        "march",
        "hole",
        "scrub",
        "level",
        "sleep"
    ]
    for i in range(int("0x00000000", 16), int("0x80000000", 16)):
        for j in range(int("0x00000000", 16), int("0x80000000", 16)):
            addr = recover_address_by_derivation_path(i, j, word_list)
            if "cndy" == addr[:4]:
                logger.info(f"{i}, {j}, {addr}")

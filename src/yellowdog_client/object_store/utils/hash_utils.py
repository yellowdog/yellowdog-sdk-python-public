import base64
import hashlib
from typing import List, Union


class HashUtils(object):
    MD5_BYTE_SIZE = 16

    @staticmethod
    def convert_hash_to_base_64(input_hash: Union[str, bytes]) -> str:
        return base64.b64encode(input_hash).decode('utf-8')

    @staticmethod
    def convert_hash_to_base_64_url(hash_value: Union[str, bytes]) -> str:
        res = HashUtils.convert_hash_to_base_64(input_hash=hash_value)
        return res.replace("=", "").replace("/", "_").replace("+", "-")

    @staticmethod
    def convert_base_64_to_hash(base_64_input):
        res = base64.b64decode(base_64_input)
        return res

    @staticmethod
    def calculate_md5_in_base_64(input_value: Union[str, bytes]) -> str:
        if not isinstance(input_value, bytes):
            input_value = input_value.encode('utf-8')
        md5 = hashlib.md5()
        md5.update(input_value)
        digest = md5.digest()
        return HashUtils.convert_hash_to_base_64(digest)

    @staticmethod
    def calculate_md5_summary_in_base_64_url(hashes_as_base_64: List[str]) -> str:
        hash_bytes = b""
        for base_64 in hashes_as_base_64:
            hash_bytes += HashUtils.convert_base_64_to_hash(base_64_input=base_64)

        md5 = hashlib.md5()
        md5.update(hash_bytes)
        digest = md5.digest()
        return HashUtils.convert_hash_to_base_64_url(hash_value=digest)

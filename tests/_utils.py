import os
import uuid


def _get_data_dir():
    tests_module_path = os.path.dirname(__file__)
    return os.path.join(tests_module_path, "data")

def _generate_random_name(suffix='ms'):
    gen_limit = 10
    for _ in range(gen_limit):
        prefix = uuid.uuid4().hex
        msfile = f"{prefix}.{suffix}"
        if not os.path.exists(msfile):
            return msfile
    else:
        raise RuntimeError("Failed to generate random name")

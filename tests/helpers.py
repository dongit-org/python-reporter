import random
import string


def rand_alphanum(len: int) -> str:
    return "".join(
        random.choices(
            string.ascii_lowercase + string.ascii_uppercase + string.digits, k=len
        )
    )

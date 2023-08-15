"""Sentence tokenizer test."""

# Internal libraries
from onclusiveml.syndicate.datasketch import MinHash, MinHashLSH


def test_syndicate():
    shingle_set = {"functions generate hash signatures article"}
    num_perm = 128
    threshold = 0.6
    weights = (0.5, 0.5)
    m = MinHash(num_perm)
    for s in shingle_set:
        m.update(s.encode("utf8"))
    lsh = MinHashLSH(threshold, num_perm, weights)
    signature = lsh.generate_signature(m)
    assert signature == [
        "AAAAAD7VrJYAAAAAUtj2YwAAAABnUo5LAAAAAKEQ6osAAAAAGN7zAQAAAACvI05uAAAAAP5T14M=",  # noqa
        "AAAAAImeBE8AAAAArLzBiwAAAABXJtUuAAAAADuLk0EAAAAABdQyawAAAABsuvhdAAAAAA1DABQ=",  # noqa
        "AAAAAN80jQ0AAAAA4AMsTwAAAAAdQ+nJAAAAADQX7AwAAAAAOInWSgAAAADW8ezsAAAAALmkSmc=",  # noqa
        "AAAAAEdhYYkAAAAAdlWvggAAAABKailoAAAAAAIxAgoAAAAATpd/swAAAABwtMk4AAAAABkBF2c=",  # noqa
        "AAAAAMTyc2oAAAAARNwyWAAAAABz/P6bAAAAACTaVUQAAAAAMoyr9gAAAACESd6KAAAAAFgDYYc=",  # noqa
        "AAAAAFKn1w8AAAAA3LGTrAAAAAAJJ73aAAAAAAtnQgYAAAAAc4I7eAAAAAD08z7vAAAAAEWmb0M=",  # noqa
        "AAAAANYBf2oAAAAAU59svQAAAABWfyecAAAAAO+fMSoAAAAA/AEiWQAAAADi76dRAAAAACZAFWI=",  # noqa
        "AAAAAKceSGYAAAAAHHnbRwAAAACNhF50AAAAAHgsIHIAAAAALQe0tgAAAACl0hKtAAAAANjd5Gw=",  # noqa
        "AAAAAJFzk3gAAAAAMxIZewAAAABmmIwNAAAAANKJgxMAAAAAaeBdxQAAAAByhAtTAAAAAKoPEtA=",  # noqa
        "AAAAAD//H6QAAAAAR2MGtQAAAADuHvbsAAAAANOxgcsAAAAAbMURIgAAAABUGFjvAAAAAA2+Lew=",  # noqa
        "AAAAADJ0nxwAAAAAEDygXwAAAAC5rKeMAAAAAMHGBJAAAAAAVbu+HAAAAACvnHsdAAAAAPZ4r3I=",  # noqa
        "AAAAAIsaapQAAAAA4UNh0wAAAAD29SlWAAAAAKgaBv4AAAAABK518AAAAACE0OvYAAAAAPYUu7c=",  # noqa
        "AAAAAPgAVJoAAAAAR8Y3RQAAAAD1tPyTAAAAAPeLD0EAAAAAnAxBywAAAABKiF6rAAAAAGoBEXA=",  # noqa
        "AAAAAGQyfFMAAAAAGFRsIAAAAAAiQRcGAAAAADzs6CYAAAAABT6eXgAAAADBDsR/AAAAAKjSFEc=",  # noqa
        "AAAAAMsg8FIAAAAAFm7yPAAAAAA5Au8cAAAAAGYhiuUAAAAA9jbZdQAAAAB2X3QvAAAAAO+93YE=",  # noqa
        "AAAAAOrGfusAAAAA4UQsGgAAAAB9n0NhAAAAAFDZRUIAAAAAbKUEUQAAAABSgqcrAAAAANReZwE=",  # noqa
        "AAAAANrB0GcAAAAAkNMRaAAAAAA0QhyKAAAAABLE06gAAAAAzi1LqAAAAACo+jipAAAAAIUoHM4=",  # noqa
        "AAAAAHxFrisAAAAAkf5FlgAAAACQ7ru+AAAAAO4TeqUAAAAAcsOYLwAAAAAHk+gFAAAAAHSHwzQ=",  # noqa
    ]

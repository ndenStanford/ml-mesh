# Copyright (c) Meta Platforms, Inc. and affiliates.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
"""Conftest."""

# Standard Library
import os

# 3rd party libraries
import matplotlib as mpl
from pytest import Session


def pytest_sessionstart(session: Session) -> None:
    """Session starts."""
    # Set the matplotlib backend to Agg for UI-less testing
    # unless the developer manually overrides by setting
    # MPLBACKEND to something else (such as "TkAgg").
    if "MPLBACKEND" not in os.environ:
        os.environ["MPLBACKEND"] = "agg"
        # The above should be enough, but I found I needed to use:
        mpl.use("agg")

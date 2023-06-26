# -*- coding: utf-8 -*-

# Standard Library
from typing import Any, Dict, List, Type

# 3rd party libraries
from locust import HttpUser
from locust.main import load_locustfile
from pydantic import root_validator

# Internal libraries
from onclusiveml.serving.rest.serving_base_params import ServingBaseParams


class LoadTestingParams(ServingBaseParams):
    # --- load test client behaviour specification. Two options:
    # - customized classes (preferred), or
    # - reference to locustfile containing customized classes (not preferred - requires an
    #   additional 'external' file)
    user_classes: List[Type[HttpUser]] = []
    locustfile: str = "locustfile.py"
    # --- load test runner behaviour
    # size of locust client pool
    num_users: int = 1
    # per second spawn rate of clients until `num_users` is reached
    spawn_rate: float = 1
    # base url of the host
    host: str = ""
    # ?
    reset_stats: bool = False

    tags: Any = None
    exclude_tags: Any = None
    stop_timeout: Any = None
    # length of test - uses locust utilities to parse into numerical spec
    run_time: str = "20s"
    # log level of underlying locust processes
    loglevel: str = "INFO"

    @root_validator
    def validate_client_behaviour_configurations(cls, values: Dict) -> Dict:

        if not values["locustfile"] and not values["user_classes"]:

            raise ValueError(
                "Invalid client configuration: At least one of `locustfile` or "
                "`user_classes` fields must be specified."
            )

        elif values["locustfile"] and values["user_classes"]:

            raise ValueError(
                "Invalid client configuration: Only one of `locustfile` or "
                "`user_classes` fields must be specified."
            )

        elif values["locustfile"]:

            docstring, classes, shape_class = load_locustfile(values["locustfile"])
            values["user_classes"] = [classes[n] for n in classes]

        return values

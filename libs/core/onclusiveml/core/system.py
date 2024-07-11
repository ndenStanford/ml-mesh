"""Runtime setup."""

# Standard Library
import os
import platform
from importlib.util import find_spec
from typing import Dict

# 3rd party libraries
import distro

# Internal libraries
from onclusiveml.core.base.metaclasses import Singleton
from onclusiveml.core.constants import Environment, OperatingSystem, Runtime


class SystemInfo(metaclass=Singleton):
    """Provides runtime information."""

    @staticmethod
    def get_system_info() -> Dict[str, str]:
        """Information about the operating system.

        Returns:
            A dictionary containing information about the operating system.
        """
        system = platform.system()

        if system == OperatingSystem.WINDOWS:
            release, version, csd, ptype = platform.win32_ver()

            return {
                "os": "windows",
                "windows_version_release": release,
                "windows_version": version,
                "windows_version_service_pack": csd,
                "windows_version_os_type": ptype,
            }

        if system == OperatingSystem.MACOS:
            return {"os": "mac", "mac_version": platform.mac_ver()[0]}

        if system == OperatingSystem.LINUX:
            return {
                "os": "linux",
                "linux_distro": distro.id(),
                "linux_distro_like": distro.like(),
                "linux_distro_version": distro.version(),
            }
        # We don't collect data for any other system.
        return {"os": "unknown"}

    @staticmethod
    def python_version() -> str:
        """Returns the python version of the running interpreter.

        Returns:
            str: the python version
        """
        return platform.python_version()

    @staticmethod
    def in_docker() -> bool:
        """If the current python process is running in a docker container.

        Returns:
            `True` if the current python process is running in a docker
            container, `False` otherwise.
        """
        if os.path.exists("/.dockerenv") or os.path.exists("/.dockerinit"):
            return True

        try:
            with open("/proc/1/cgroup", "rt") as ifh:
                info = ifh.read()
                return "docker" in info
        except (FileNotFoundError, Exception):
            return False

    @staticmethod
    def in_kubernetes() -> bool:
        """If the current python process is running in a kubernetes pod.

        Returns:
            `True` if the current python process is running in a kubernetes
            pod, `False` otherwise.
        """
        if "KUBERNETES_SERVICE_HOST" in os.environ:
            return True

        try:
            with open("/proc/1/cgroup", "rt") as ifh:
                info = ifh.read()
                return "kubepod" in info
        except (FileNotFoundError, Exception):
            return False

    @staticmethod
    def in_notebook() -> bool:
        """If the current Python process is running in a notebook.

        Returns:
            `True` if the current Python process is running in a notebook,
            `False` otherwise.
        """
        if find_spec("IPython") is not None:
            # 3rd party libraries
            from IPython import get_ipython

            if get_ipython().__class__.__name__ in [
                "TerminalInteractiveShell",
                "ZMQInteractiveShell",
            ]:
                return True
        return False

    @staticmethod
    def in_github_actions() -> bool:
        """If the current Python process is running in GitHub Actions.

        Returns:
            `True` if the current Python process is running in GitHub
            Actions, `False` otherwise.
        """
        return "GITHUB_ACTIONS" in os.environ

    @staticmethod
    def in_wsl() -> bool:
        """If the current process is running in Windows Subsystem for Linux.

        source: https://www.scivision.dev/python-detect-wsl/

        Returns:
            `True` if the current process is running in WSL, `False` otherwise.
        """
        return "microsoft-standard" in platform.uname().release

    @staticmethod
    def environment() -> str:
        """If the current python process is running in a dev environment.

        Returns:
            `True` if the current process is running in a dev environment,
            `False` otherwise.
        """
        env = Environment.from_value(os.environ.get("ENVIRONMENT"))
        if env is None:
            return Environment.UNDEFINED
        return env


def get_runtime() -> str:
    """Returns a string representing the execution runtime.

    Returns:
        str: the execution runtime
    """
    # Order is important here
    if SystemInfo.in_kubernetes():
        return Runtime.KUBERNETES
    elif SystemInfo.in_github_actions():
        return Runtime.GITHUB_ACTION
    elif SystemInfo.in_notebook():
        return Runtime.NOTEBOOK
    elif SystemInfo.in_wsl():
        return Runtime.WSL
    else:
        return Runtime.NATIVE

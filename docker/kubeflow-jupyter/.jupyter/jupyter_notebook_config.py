"""Jupyter config."""
import errno
import os
import stat
import subprocess

from jupyter_core.paths import jupyter_data_dir

c = get_config()  # no-qa: F821
c.ServerApp.ip = "0.0.0.0"
c.ServerApp.port = 8888
c.ServerApp.open_browser = False

c.FileContentsManager.delete_to_trash = False

# generate a self-signed certificate
# NOTE: do we still need this?
if "GEN_CERT" in os.environ:
    # https://jupyter-notebook.readthedocs.io/en/stable/security.html#collaboration
    # share signatures database
    dir_name = jupyter_data_dir()
    pem_file = os.path.join(dir_name, "notebook.pem")
    try:
        os.makedirs(dir_name)
    except OSError as exc:
        if exc.errno == errno.EEXIST and os.path.isdir(dir_name):
            pass
        else:
            raise ValueError("Could not create directory")

    # Generate an openssl.cnf file to set the distinguished name
    cnf_file = os.path.join(os.getenv("CONDA_DIR", "/usr/lib"), "ssl", "openssl.cnf")
    if not os.path.isfile(cnf_file):
        with open(cnf_file, "w") as fh:
            fh.write(
                """\
[req]
distinguished_name = req_distinguished_name
[req_distinguished_name]
"""
            )

    # generate certificate if one does not exist on disk
    subprocess.check_call(
        [
            "openssl",
            "req",
            "-new",
            "-newkey=rsa:2048",
            "-days=365",
            "-nodes",
            "-x509",
            "-subj=/C=XX/ST=XX/L=XX/O=generated/CN=generated",
            f"-keyout={pem_file}",
            f"-out={pem_file}",
        ]
    )

    # restrict access to file
    os.chmod(pem_file, stat.S_IRUSR | stat.S_IWUSR)

    c.ServerApp.certfile = pem_file

# change default umask if env variable is set
if "NB_UMASK" in os.environ:
    os.umask(int(os.getenv("NB_UMASK"), 8))

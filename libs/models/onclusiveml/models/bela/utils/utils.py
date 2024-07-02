"""Utils."""


class DummyPathManager:
    """Dummy path manager for local file operations."""

    def get_local_path(self, path, *args, **kwargs):
        """Returns local path.

        Args:
            path (str): The path to be returned.

        Returns:
            str: The input path.
        """
        return path

    def open(self, path, *args, **kwargs):
        """Opens a file located at the specified path.

        Args:
            path (str): The path to the file to be opened.
            *args: Additional positional arguments passed to the 'open' function.
            **kwargs: Additional keyword arguments passed to the 'open' function.

        Returns:
            file object: A file object representing the opened file.
        """
        return open(path, *args, **kwargs)


PathManager = DummyPathManager()

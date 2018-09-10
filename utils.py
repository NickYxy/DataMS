import os


def project_path():
    utils_file = os.path.realpath(__file__)
    utils_dir = os.path.dirname(utils_file)
    root = os.path.join(utils_dir, os.pardir)
    root = os.path.abspath(root)
    return root


def path_for(*paths):
    """
    root = '/a'
    os.path.join(root, 'b', 'c.txt') -> /a/b/c.txt
    os.path.join(root, '/b', 'c.txt') -> /b/c.txt
    """
    root = project_path()
    path = os.path.join(root, *paths)
    path = os.path.abspath(path)
    return path

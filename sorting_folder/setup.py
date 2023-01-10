from setuptools import setup, find_namespace_packages
setup(
    name="sorting_files",
    version="0.0.1",
    author="GoIT_student",
    url="",
    packages=find_namespace_packages(),
    entry_points={'console_scripts': ['clean-folder=clean_folder.clean:start']}
)
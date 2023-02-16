from setuptools import setup, find_namespace_packages

setup(
    name="Apllepy_personal_assistant",
    version="0.1.5",
    author="Pupinin Igor, Valentyna Gordynska, Shevcova Tetyana, Svitelskyi Andriy",
    url="https://github.com/IgorPupynin/Project_group6",
    license="MIT",
    # classifiers=['License:: OSI Approved:: MIT License',
    #              'Operating System:: OS Independent',
    #              'Programming Language:: Python:: 3'],
    description="Apllepy-personal-assistant",
    # readme="README.md",
    packages=find_namespace_packages(),
    entry_points={'console_scripts': ['console-bot=app.menu:main']}
)

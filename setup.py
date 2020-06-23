import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()


def main():
    import igninterage as app
    setuptools.setup(
        name=app.__project__,
        version=app.__version__,
        author=app.__author__,
        author_email=app.__author_email__,
        description=app.__description__,
        long_description=long_description,
        license=app.__licence__,
        packages=['igninterage'],
        classifiers=app.__classifiers__,
        python_requires=app.__python_requires__,
        install_requires=['requests', 'selenium'],
    )


if __name__ == '__main__':
    main()

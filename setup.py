import codecs
import os

from setuptools import setup, find_packages


def read(rel_path):
    here = os.path.abspath(os.path.dirname(__file__))
    with codecs.open(os.path.join(here, rel_path), "r") as fp:
        return fp.read()


def get_meta(rel_path):
    meta = {}

    for line in read(rel_path).splitlines():
        for meta_key in [
            "author",
            "copyright",
            "description",
            "email",
            "license",
            "url",
            "version",
        ]:
            if line.startswith("__{key}__".format(key=meta_key)):
                delim = '"' if '"' in line else "'"
                meta[meta_key] = line.split(delim)[1]

    return meta


def get_requirements(rel_path):
    with open(rel_path, "r") as file:
        return file.read().strip().splitlines()


# ------------------------------------------------------------------------------

NAME = "pinttrs"
META = get_meta(os.path.join("src", "pinttr", "__init__.py"))
PACKAGES = find_packages(where="src")
LONG = open("README.md", "r", encoding="utf-8").read()

INSTALL_REQUIRES = get_requirements(os.path.join("requirements", "main.txt"))
EXTRAS_REQUIRE = {
    "docs": get_requirements(os.path.join("requirements", "docs.txt")),
    "tests": get_requirements(os.path.join("requirements", "tests.txt")),
}

if __name__ == "__main__":
    setup(
        name=NAME,
        description=META["description"],
        license=META["license"],
        url=META["url"],
        # project_urls=PROJECT_URLS,
        version=META["version"],
        author=META["author"],
        author_email=META["email"],
        maintainer=META["author"],
        maintainer_email=META["email"],
        # keywords=KEYWORDS,
        long_description=LONG,
        long_description_content_type="text/markdown",
        packages=PACKAGES,
        package_dir={"": "src"},
        python_requires=">=3.5",
        zip_safe=False,
        # classifiers=CLASSIFIERS,
        install_requires=INSTALL_REQUIRES,
        extras_require=EXTRAS_REQUIRE,
        # include_package_data=True,
        # options={"bdist_wheel": {"universal": "1"}},
    )

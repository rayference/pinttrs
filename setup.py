from setuptools import setup, find_packages

NAME = "pinttrs"
PACKAGES = find_packages(where="src")


if __name__ == "__main__":
    setup(
        name=NAME,
        # description=find_meta("description"),
        # license=find_meta("license"),
        # url=URL,
        # project_urls=PROJECT_URLS,
        # version=VERSION,
        # author=find_meta("author"),
        # author_email=find_meta("email"),
        # maintainer=find_meta("author"),
        # maintainer_email=find_meta("email"),
        # keywords=KEYWORDS,
        # long_description=LONG,
        # long_description_content_type="text/x-rst",
        packages=PACKAGES,
        package_dir={"": "src"},
        # python_requires=">=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*",
        zip_safe=False,
        # classifiers=CLASSIFIERS,
        # install_requires=INSTALL_REQUIRES,
        # extras_require=EXTRAS_REQUIRE,
        # include_package_data=True,
        # options={"bdist_wheel": {"universal": "1"}},
    )

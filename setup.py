from setuptools import setup, find_packages
import sys
import os

# PEP0440 compatible formatted version, see:
# https://www.python.org/dev/peps/pep-0440/
#
# release markers:
#   X.Y
#   X.Y.Z   # For bugfix releases
#
# pre-release markers:
#   X.YaN   # Alpha release
#   X.YbN   # Beta release
#   X.YrcN  # Release Candidate
#   X.Y     # Final release

# version.py defines the VERSION and VERSION_SHORT variables.
# We use exec here so we don't import allennlp_hub whilst setting up.
VERSION = {}
with open("allennlp_hub/version.py") as version_file:
    exec(version_file.read(), VERSION)

install_requirements = []
if not os.environ.get("EXCLUDE_ALLENNLP_IN_SETUP"):
    # Warning: This will not give you the desired version if you've already
    # installed allennlp! See https://github.com/pypa/pip/issues/5898.
    #
    # There used to be an alternative to this using `dependency_links`
    # (https://stackoverflow.com/questions/3472430), but pip decided to
    # remove this in version 19 breaking numerous projects in the process.
    # See https://github.com/pypa/pip/issues/6162.
    #
    # As a mitigation, run `pip uninstall allennlp` before installing this
    # package.
    #
    # TODO(brendanr): Make these point to released versions, when possible, by
    # loading requirements.txt. Currently allennlp-semparse is unreleased and
    # it depends on a specific allennlp SHA. Due to the aforementioned
    # setuptools bug, we explicitly set the allennlp version here to be that
    # required by allennlp-semparse.
    allennlp_sha = "8bc5da2d7d0050374c78b52adde7149425e3b52a"
    semparse_sha = "002f97b34277356333eac7937924a3b7ad48fb24"
    reading_comprehension_sha = "c241f324e8a5af5197808b0f6dc629f1513add54"
    install_requirements = [
        f"allennlp @ git+https://github.com/allenai/allennlp@{allennlp_sha}#egg=allennlp",
        f"allennlp_semparse @ git+https://github.com/allenai/allennlp-semparse@{semparse_sha}#egg=allennlp-semparse",
        f"allennlp_reading_comprehension @ git+https://github.com/allenai/allennlp-reading-comprehension@{reading_comprehension_sha}#egg=allennlp-reading-comprehension",
    ]

# make pytest-runner a conditional requirement,
# per: https://github.com/pytest-dev/pytest-runner#considerations
needs_pytest = {"pytest", "test", "ptr"}.intersection(sys.argv)
pytest_runner = ["pytest-runner"] if needs_pytest else []

setup_requirements = [
    # add other setup requirements as necessary
] + pytest_runner

setup(
    name="allennlp_hub",
    version=VERSION["VERSION"],
    description="A collection of selected of models built with AllenNLP.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    classifiers=[
        "Intended Audience :: Science/Research",
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3.6",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    keywords="allennlp NLP deep learning machine reading",
    url="https://github.com/allenai/allennlp-hub",
    author="Allen Institute for Artificial Intelligence",
    author_email="allennlp@allenai.org",
    license="Apache",
    packages=find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
    install_requires=install_requirements,
    setup_requires=setup_requirements,
    tests_require=["pytest", "flaky", "responses>=0.7"],
    include_package_data=True,
    python_requires=">=3.6.1",
    zip_safe=False,
)

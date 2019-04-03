import setuptools

# use this fix until github.com/pypa/setuptools/pull/1343 is solved
import pypandoc
pypandoc.convert_file("README.md", "rst", outputfile="README.rst")

setuptools.setup(
    setup_requires=["pbr>=1.9", "setuptools>=17.1"],
    pbr=True,
)

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ko_pron",
    version="1.2",
    author="Andriy Koretskyy",
    author_email="kord123@gmail.com",
    description="Korean pronunciation and romanisation based on Wiktionary ko-pron lua module",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    license='MIT',
    keywords='hangul korean pronunciation romanisation romanization IPA Yale McCune-Reischauer WT-revised revised',
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)
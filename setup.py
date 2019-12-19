import setuptools



with open("README.md", "r", endcoding="UTF-8") as fh:
    long_description = fh.read()

setuptools.setup(
    # for install:
    # $ pip install Graduation_Work_sa1am9
    #
    name="Graduation_Work_sa1am9",
    version="0.0.1",
    author="Illya Saltykov",
    author_email="ktillsal@gmail.com",
    description="Flask project",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/sa1am9/Graduation_Work",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
    python_requires='>=3.6',
)
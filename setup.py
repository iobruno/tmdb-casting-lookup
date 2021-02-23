import setuptools

setuptools.setup(
    name='reglobinition-tmdb-crawler',
    version='1.0.0',
    install_requires=[
        "apache-beam[gcp]==2.27.0",
        "google-cloud-storage==1.36.0",
        "omegaconf==2.0.6",
        "requests==2.25.1",
        "pendulum==2.1.2",
        "Pillow==8.1.0",
        "python-slugify==4.0.1",
        "typer==0.3.2"
    ],
    packages=setuptools.find_packages(),
)

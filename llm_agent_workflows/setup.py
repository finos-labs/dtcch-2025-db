from setuptools import setup, find_packages

setup(
    name='llm_agent_workflows',
    version='0.1.0',
    description='A project for processing PDF files with AWS Bedrock analysis',
    author='Your Name',
    author_email='your.email@example.com',
    packages=find_packages(),
    install_requires=[
        'boto3',
        'python-dotenv',
        'PyMuPDF',
        'Pillow'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
from setuptools import setup

setup(
    name='expense-tracker',
    version='0.1',
    py_modules=['app'],
    install_requires=[],
    entry_points={
        'console_scripts': [
            'expense-tracker=app:main',
        ],
    },
    author='Ali Beiti',
    description='A simple CLI expense tracker application',
    url='https://github.com/AliBeiti/Expense_Tracker_CLI',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Environment :: Console',
        'License :: OSI Approved :: MIT License',
    ],
    python_requires='>=3.7',
)

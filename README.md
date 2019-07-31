# SGE
First of all you need to have installed:
- brew
- virtualenv

# Install Requirements:
To install the app you should install python 3.6.5:

brew install python3
brew unlink python

with the previous steps you will install the last python version available, then I installed python 3.6.5 using above link

brew install --ignore-dependencies https://raw.githubusercontent.com/Homebrew/homebrew-core/f2a764ef944b1080be64bd88dca9a1d80130c558/Formula/python.rb --ignore-dependencies

After that I ran brew link --overwrite python. Now I have all pythons in the system to create the virtual environments.

you can check the python versions that you have installed:
kendoteca~ $ python --version
Python 2.7.10
kendoteca~ $ python3.7 --version
Python 3.7.1
kendoteca~ $ python3.6 --version
Python 3.6.5

To create Python 2.7 virtual environment.
kendoteca~ $ virtualenv -p python2.7 env

To create Python 3.6 virtual environment.
kendoteca~ $ virtualenv -p python3.6 env

To create Python 3.7 virtual environment.
kendoteca~ $ virtualenv -p python3.7 env

Once you have python installed we are ready to install the requirements.txt file
kendoteca~ $ source <virtual_environment>/bin/activate

kendoteca~ $ cd /SGE/
kendoteca~ $ pip3 install -r requirements.txt
kendoteca~ $ python manage.py runserver

Done!


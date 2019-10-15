pip install --upgrade pip
pip install pipenv
curl https://pyenv.run | bash
echo 'export PATH="/home/pi/.pyenv/bin:$PATH"' >> ~/.bashrc
echo 'eval "$(pyenv init -)"' >> ~/.bashrc
echo 'eval "$(pyenv virtualenv-init -)"' >> ~/.bashrc
source ~/.bashrc
pyenv install 3.7.3
pipenv install
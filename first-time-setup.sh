sudo apt-get update -y
sudo apt-get install -y libssl-dev bzip2 libreadline6 libreadline6-dev sqlite3
echo "PATH=$HOME/.local/bin:$PATH" >> ~/.bashrc
source ~/.bashrc
python -m pip install pipenv
echo 'export PATH="/home/pi/.pyenv/bin:$PATH"' >> ~/.bashrc
echo 'eval "$(pyenv init -)"' >> ~/.bashrc
echo 'eval "$(pyenv virtualenv-init -)"' >> ~/.bashrc
source ~/.bashrc
curl https://pyenv.run | bash
pyenv install 3.5.3
pipenv install
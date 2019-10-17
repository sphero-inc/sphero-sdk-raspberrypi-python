sudo apt-get update -y
sudo apt-get install -y xterm libssl-dev bzip2 libreadline6 libreadline6-dev sqlite3
python -m pip install pipenv
echo "PATH=$HOME/.local/bin:$PATH" >> ~/.bashrc
curl https://pyenv.run | bash
echo 'export PATH="/home/pi/.pyenv/bin:$PATH"' >> ~/.bashrc
echo 'eval "$(pyenv init -)"' >> ~/.bashrc
echo 'eval "$(pyenv virtualenv-init -)"' >> ~/.bashrc
source ~/.bashrc
xterm -e "pyenv install 3.5.3; pipenv install"

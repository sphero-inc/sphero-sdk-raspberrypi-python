sudo apt-get install -y make build-essential libssl-dev zlib1g-dev libbz2-dev libreadline-dev libsqlite3-dev llvm libncurses5-dev libncursesw5-dev xz-utils tk-dev
python -m pip install pipenv
echo "PATH=$HOME/.local/bin:$PATH" >> ~/.bashrc
source ~/.bashrc
curl https://pyenv.run | bash
echo 'export PATH="/home/pi/.pyenv/bin:$PATH"' >> ~/.bashrc
echo 'eval "$(pyenv init -)"' >> ~/.bashrc
echo 'eval "$(pyenv virtualenv-init -)"' >> ~/.bashrc
source ~/.bashrc
pyenv install 3.5.3
pipenv install
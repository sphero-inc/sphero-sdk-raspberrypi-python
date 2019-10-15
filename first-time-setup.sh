pip install pipenv
curl https://pyenv.run | bash
echo 'export PATH="/home/pi/.pyenv/bin:$PATH"' >> ~/.bashrc
echo 'eval "$(pyenv init -)"' >> ~/.bashrc
echo 'eval "$(pyenv virtualenv-init -)"' >> ~/.bashrc
source ~/.bashrc
pipenv install

if [ $? -eq 0 ]
then
  echo "RVR dependencies succesfully installed."
else
  pyenv install 3.5.3
  pipenv install
fi
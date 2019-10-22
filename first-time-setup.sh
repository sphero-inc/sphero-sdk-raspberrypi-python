sudo apt-get update -y
sudo apt-get install -y libssl-dev bzip2 libreadline6 libreadline6-dev sqlite3
python -m pip install pipenv
printf "PATH=$HOME/.local/bin:$PATH" >> ~/.bashrc
curl https://pyenv.run | bash
printf 'export PATH="/home/pi/.pyenv/bin:$PATH"\neval "$(pyenv init -)"\neval "$(pyenv virtualenv-init -)' >> ~/.bashrc
printf '\n^^^ We just added the lines above to your .bashrc file for your convenience :) ^^^'
printf '\nPlease head over to https://sdk.sphero.com/docs/getting_started/raspberry_pi/python_setup for some final setup instructions.'
printf '\nLove,\nSphero\n'
exec $SHELL


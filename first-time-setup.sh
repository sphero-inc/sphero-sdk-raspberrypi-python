sudo apt-get update -y

sudo apt-get install -y make \
build-essential \
llvm \
libssl-dev \
bzip2 \
zlib1g-dev \
libbz2-dev \
libreadline6 \
libreadline-dev \
libsqlite3-dev \
libncurses5-dev \
libncursesw5-dev \
xz-utils \
tk-dev \
libffi-dev \
liblzma-dev

python -m pip install pipenv

printf "PATH=$HOME/.local/bin:$PATH\n" >> ~/.profile

while true; do
    read -p "A restart is required for changes to take effect.  Restart now?" yn
    case $yn in
        [Yy]* ) sudo reboot; break;;
        [Nn]* ) exit;;
        * ) echo "Please answer yes or no.";;
    esac
done

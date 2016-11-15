curl -fLo ~/.vim/autoload/plug.vim --create-dirs https://raw.githubusercontent.com/junegunn/vim-plug/master/plug.vim
curl https://raw.githubusercontent.com/Rkieltyka/rados/dotfiles/dotfiles/.vimrc --create-dirs -o ~/.vimrc
vim +PlugInstall +qall

call plug#begin('~/.vim/plugged')

Plug 'bling/vim-airline'
Plug 'morhetz/gruvbox'
Plug 'airblade/vim-gitgutter'
Plug 'vim-airline/vim-airline-themes'
Plug 'ervandew/supertab'
Plug 'alfredodeza/khuno.vim'
Plug 'Townk/vim-autoclose'
Plug 'scrooloose/nerdtree'

call plug#end()

" Colours!
syntax on
colorscheme gruvbox
set background=dark

" Show line numbers
set number

" Highlight search results
set hlsearch

" Indentation with four spaces
set tabstop=4
set shiftwidth=4
set softtabstop=4
set expandtab

" Complain about trailing whitespace
set list
set list listchars=tab:→\ ,trail:·

" Auto pairing (Easy way but involves copy/paste issues)
"inoremap { {}<Left>
"inoremap ( ()<Left>
"inoremap [ []<Left>
"inoremap < <><Left>
"inoremap ' ''<Left>

" Set up vim-airline
set laststatus=2
"let g:airline_powerline_fonts = 1
let g:airline_theme='gruvbox'

" Nerdtree config
" --------------------------------------
" Open Nerdtree with vim
autocmd vimenter * NERDTree

" Use CTR+N to toggle Nerdtree ON/OFF
map <C-n> :NERDTreeToggle<CR>


" Make sure to have vimplug installed for plugins

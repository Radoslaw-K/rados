syntax on

" Show line numbers
set number

" Set line marker at column 79 (mostly for python PEP8)
set colorcolumn=79

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
inoremap { {}<Left>
inoremap ( ()<Left>
inoremap [ []<Left>
inoremap " ""<Left>
inoremap < <><Left>
inoremap ' ''<Left>

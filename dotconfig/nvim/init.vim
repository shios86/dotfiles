set nocompatible
filetype on
filetype plugin on
filetype indent on
syntax on
set number
set mouse=
set cindent autoindent expandtab smartindent

set shiftwidth=4 tabstop=4
filetype plugin indent on
autocmd FileType c setlocal shiftwidth=4 tabstop=4 noexpandtab
autocmd FileType terraform setlocal shiftwidth=2 tabstop=2 expandtab autoindent
autocmd FileType terraform-vars setlocal shiftwidth=2 tabstop=2 expandtab autoindent

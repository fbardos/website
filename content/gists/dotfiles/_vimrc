" ============================================================================
" Minimal, robust Vim config
" ============================================================================

" disable old, vi compatibility mode
set nocompatible

" ----------------------------------------------------------------------------
" Core
" ----------------------------------------------------------------------------

" enable filetype detection, filetype plugins and intendation
" (without external plugins)
filetype plugin indent on
syntax enable

let mapleader = " "  		" custom shortcuts
let maplocalleader = "\\"  	" filetype sepcific mappings

" ----------------------------------------------------------------------------
" Editing behavior
" ----------------------------------------------------------------------------

set backspace=indent,eol,start  " let backspace to behave normally
set hidden			            " allow switch buffer without save
set confirm			            " ask instead of error when buffer unsafed
set autoread			        " auto-reload buffer when orig file changed

set wildmenu			        " show completions e.g. with :e ~/.vim<Tab>

" first tab: completes to the longes common match
" further tabs: cycle through matches
set wildmode=longest:full,full
set wildignore+=*.o,*.obj,*.pyc,*.class
set wildignore+=.git,.hg,.svn
set wildignore+=node_modules,dist,build,target

" ----------------------------------------------------------------------------
" Search
" ----------------------------------------------------------------------------

set noignorecase        " keep default search case-senstive
set nosmartcase

set incsearch           " show search matches whily typing
set hlsearch            " highlight search matches

" set keybind for :nohl
nnoremap <silent> <leader><space> :nohlsearch<CR>

" ----------------------------------------------------------------------------
" Display
" ----------------------------------------------------------------------------

set nonumber            " no vertical line numbers
set norelativenumber

set ruler               " show position line, col
set showcmd             " show partial vim command
set showmode            " show current vim mode
set laststatus=2        " always show statusline

set scrolloff=5         " keep lines above/below visible when scrolling
set sidescrolloff=5

set wrap                " line wrapping enabled
set linebreak           " wrap at word boundaries
set breakindent         " visually indent line breaks

" per default, do not show special characters
" but enable them with <leader>l
set nolist
set listchars=tab:»·,trail:·,extends:>,precedes:<,nbsp:+
nnoremap <leader>l :set list!<CR>

set background=dark
silent! colorscheme default

" highlight trailing whitespaces (after colorscheme)
highlight ExtraWhitespace ctermbg=DarkRed guibg=DarkRed
match ExtraWhitespace /\s\+$/

" ----------------------------------------------------------------------------
" Statusline colors
" ----------------------------------------------------------------------------

" Active statusline: brighter and easy to read
highlight StatusLine   ctermfg=Black ctermbg=Gray     cterm=NONE

" Inactive statusline: darker, still readable
highlight StatusLineNC ctermfg=White ctermbg=DarkGray cterm=NONE

" not so aggressive color column
highlight ColorColumn ctermbg=DarkGray guibg=#2a2a2a

" ----------------------------------------------------------------------------
" Indentation
" ----------------------------------------------------------------------------

set autoindent          " inherit indentation from previous line
set nosmartindent       " indentation is handled by filetype plugin
set expandtab           " IMPORTANT: inserts spaces when pressing <Tab>
set tabstop=4           " displays a real tab as 4 cols wide
set shiftwidth=4        " keeps autoindent and manual indent predictable
set softtabstop=4       " controls how tab and backspace behave while editing
set copyindent          " copy the structure of existing ind. when autoindent
set preserveindent      " tries to preserve existing indentation

" ----------------------------------------------------------------------------
" Splits
" ----------------------------------------------------------------------------

set splitbelow          " horizontal splits open below
set splitright          " vertical splits open right

" ----------------------------------------------------------------------------
" Buffers
" ----------------------------------------------------------------------------

nnoremap <leader>bn :bnext<CR>
nnoremap <leader>bp :bprevious<CR>
nnoremap <leader>bd :bdelete<CR>
nnoremap <leader>ls :ls<CR>:b<Space>

" ----------------------------------------------------------------------------
" Persistent undo, swap, and backups
" ----------------------------------------------------------------------------

set backup
set backupdir=~/.vim/backup//
set directory=~/.vim/swap//

if has('persistent_undo')
  set undofile
  set undodir=~/.vim/undo//
endif

if !isdirectory(expand('~/.vim/backup'))
  call mkdir(expand('~/.vim/backup'), 'p')
endif

if !isdirectory(expand('~/.vim/swap'))
  call mkdir(expand('~/.vim/swap'), 'p')
endif

if has('persistent_undo') && !isdirectory(expand('~/.vim/undo'))
  call mkdir(expand('~/.vim/undo'), 'p')
endif

" ----------------------------------------------------------------------------
" Clipboard
" ----------------------------------------------------------------------------
" Use the system clipboard if this Vim supports it.

if has('clipboard')
  set clipboard=unnamedplus
endif

" ----------------------------------------------------------------------------
" Mouse
" ----------------------------------------------------------------------------

set mouse=a

" ----------------------------------------------------------------------------
" Folding
" ----------------------------------------------------------------------------

set foldmethod=manual           " no automatic fold
set foldlevelstart=99

" ----------------------------------------------------------------------------
" Grep
" ----------------------------------------------------------------------------

" use rg for vim's built-in grep command
if executable('rg')
  set grepprg=rg\ --vimgrep\ --smart-case\ --hidden
  set grepformat=%f:%l:%c:%m
endif

nnoremap <leader>g :grep<Space>

" ----------------------------------------------------------------------------
" Useful mappings
" ----------------------------------------------------------------------------

nnoremap <leader>w :write<CR>
nnoremap <leader>q :quit<CR>

nnoremap <leader>ev :edit ~/.vimrc<CR>
nnoremap <leader>sv :source ~/.vimrc<CR>

" joins lines without losing cursor position
nnoremap J mzJ`z

" after jumping to next or previous search result, vim centers the result
" on screen and opens folds if needed
nnoremap n nzzzv
nnoremap N Nzzzv

" ----------------------------------------------------------------------------
" NetRW: built-in file browser
" ----------------------------------------------------------------------------

let g:netrw_banner = 0
let g:netrw_liststyle = 3
let g:netrw_browse_split = 0
let g:netrw_altv = 1
let g:netrw_winsize = 25

nnoremap <leader>e :Explore<CR>

" ----------------------------------------------------------------------------
" Filetype-specific settings
" Keep these here so the entire config remains one file.
" ----------------------------------------------------------------------------

augroup user_filetypes
  autocmd!

  " Git commits
  autocmd FileType gitcommit setlocal spell textwidth=72 colorcolumn=73

  " Markdown
  autocmd FileType markdown setlocal wrap linebreak spell textwidth=80 tabstop=2 shiftwidth=2 softtabstop=2

  " Plain text
  autocmd FileType text setlocal wrap linebreak spell textwidth=80

  " YAML
  autocmd FileType yaml setlocal tabstop=2 shiftwidth=2 softtabstop=2 expandtab

  " JSON
  autocmd FileType json setlocal tabstop=2 shiftwidth=2 softtabstop=2 expandtab

  " Shell scripts
  autocmd FileType sh setlocal tabstop=2 shiftwidth=2 softtabstop=2 expandtab

  " Python
  autocmd FileType python setlocal tabstop=4 shiftwidth=4 softtabstop=4 expandtab
augroup END

" ----------------------------------------------------------------------------
" Trailing whitespace helper
" ----------------------------------------------------------------------------

command! TrimWhitespace %s/\s\+$//e

" ----------------------------------------------------------------------------
" Terminal/local compatibility
" ----------------------------------------------------------------------------

set ttyfast

" ----------------------------------------------------------------------------
" Security
" ----------------------------------------------------------------------------

" modelines allow individual files to set Vim options from comments inside
" the file.
set nomodeline

syntax on
set fileformat=unix
set encoding=UTF-8
au BufNewFile,BufRead *.py
    \ set tabstop=4 |
    \ set softtabstop=4 |
    \ set shiftwidth=4 |
set tabstop=2
set softtabstop=2
set shiftwidth=2
set autoindent
set smartindent
set smarttab
set expandtab
set nowrap
set number

" Dynamically map F2 to save and run the script based on file type
autocmd FileType bash nnoremap <buffer> <F2> :w<CR>:!bash %<CR>
autocmd FileType python nnoremap <buffer> <F2> :w<CR>:!python3 %<CR>
autocmd FileType sh nnoremap <buffer> <F2> :w<CR>:!bash %<CR>
autocmd FileType perl nnoremap <buffer> <F2> :w<CR>:!perl %<CR>
autocmd FileType javascript nnoremap <buffer> <F2> :w<CR>:!node %<CR>

" Auto-load template when creating a new file
autocmd BufNewFile * call InsertTemplate()

function! InsertTemplate()
    " Get the file extension
    let l:ext = expand('%:e')

    " Construct the template path
    let l:template = expand("~/.vim/templates/template." . l:ext)

    " Debugging: Check if the template file exists
    if !filereadable(l:template)
        echohl WarningMsg | echo "Template not found: " . l:template | echohl None
        return
    endif

    " Load the template content at the beginning of the file
    execute "0r " . l:template

    " Replace placeholders only if they exist in the template
    silent! execute "%s/__SCRIPT_NAME__/" . expand('%:t') . "/g"
    silent! execute "%s/__AUTHOR__/" . system("whoami | tr -d '\n'") . "/g"
    silent! execute "%s/__DATE__/" . strftime("%Y-%m-%d %H:%M:%S") . "/g"

    " Move cursor to the script body
    normal! 10G2l
endfunction

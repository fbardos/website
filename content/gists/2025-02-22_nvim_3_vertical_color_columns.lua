-- toggle colorcolumn
function ToggleColorColumns()
    if vim.wo.colorcolumn == "" then
	--  80: readable by almost anyone
	--  88: preferred by python black
	-- 120: viewable by wider windows
        vim.wo.colorcolumn = "81,89,121"

        -- Set different colors for different columns
        -- in NVIM, only one ColorColumn color is supported out of the box
        vim.cmd([[highlight ColorColumn guibg=#9E1E1E]])
    else
        -- reset
        vim.wo.colorcolumn = ""
        vim.cmd([[highlight ColorColumn guibg=#212121]])
        vim.opt.cursorline = true -- keep horizontal line
    end
end

vim.api.nvim_set_keymap(
    "n",
    "<leader>m",
    ":lua ToggleColorColumns()<CR>",
    { desc = "Toggle colorcolumn for 80, 88 and 120 line characters.", noremap = true, silent = true }
)


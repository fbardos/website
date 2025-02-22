-- using lazy.nvim
return {
  "stevearc/conform.nvim",
  event = { "BufReadPre", "BufNewFile" },
  config = function()
    require("conform").setup({
      formatters = {
        isort = {
          args = { "--profile", "black", "--force-single-line-imports", "-" },
          stdin = true,
        },
        black = {
          args = { "--skip-string-normalization", "-" },
          stdin = true,
        },
      },
      formatters_by_ft = {
        python = {"isort", "black"},
      },
      format_on_save = {
        lsp_fallback = true,
        timeout_ms = 500,
      },
    })

    -- Create a manual format command
    vim.api.nvim_create_user_command("Format", function()
      require("conform").format({ async = true, lsp_fallback = true })
    end, { desc = "Format current buffer" })
  end,
}

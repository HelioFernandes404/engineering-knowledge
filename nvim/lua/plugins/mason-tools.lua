return {
  "WhoIsSethDaniel/mason-tool-installer.nvim",
  dependencies = {
    "williamboman/mason.nvim",
    "williamboman/mason-lspconfig.nvim", -- optional but handy
  },
  opts = {
    ensure_installed = {
      "ansible-language-server",
      "bash-language-server",
      "black",
      "docker-compose-language-service",
      "dockerfile-language-server",
      "eslint_d",
      "intelephense",
      "json-lsp",
      "lua-language-server",
      "php-cs-fixer",
      "phpstan",
      "prettier",
      "prettierd",
      "pyright",
      "ruff",
      "shellcheck",
      "shfmt",
      "stylua",
      "typescript-language-server",
      "yaml-language-server",
      "yamllint",
    },
    auto_update = false,
    run_on_start = true,
  },
  -- If you prefer explicit setup for mason itself:
  config = function(_, opts)
    require("mason").setup({})
    require("mason-tool-installer").setup(opts)
  end,
}

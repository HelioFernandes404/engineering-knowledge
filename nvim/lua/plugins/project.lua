return {
  "ahmedkhalf/project.nvim",
  event = "VeryLazy",
  config = function()
    require("project_nvim").setup({
      detection_methods = { "pattern" },
      patterns = { ".git", "Makefile", "package.json", "pyproject.toml" },
      silent_chdir = false, -- shows cwd change
    })

    -- Load Telescope integration if installed
    require("telescope").load_extension("projects")
  end,
}

return {
  "ThePrimeagen/harpoon",
  branch = "harpoon2",
  dependencies = { "nvim-lua/plenary.nvim" },

  config = function()
    local harpoon = require("harpoon")
    local wk = require("which-key")

    harpoon:setup({
      settings = {
        save_on_toggle = true,
        sync_on_ui_close = true,
        key = function()
          return vim.loop.cwd()
        end,
      },
    })

    local terminals = harpoon:list("term")

    -- ← use .add() with the new "list-of-lists" spec :contentReference[oaicite:0]{index=0}
    wk.add({
      { "<leader>h", group = "Harpoon" },

      {
        "<leader>ha",
        function()
          harpoon:list():add()
        end,
        desc = "Add file",
      },

      {
        "<leader>hh",
        function()
          harpoon.ui:toggle_quick_menu(harpoon:list())
        end,
        desc = "Menu",
      },

      {
        "<leader>hg",
        function()
          local idx
          for i, item in ipairs(terminals.items) do
            if item.value == "lazygit" then
              idx = i
              break
            end
          end
          if not idx then
            terminals:append("lazygit")
            idx = #terminals.items
          end
          terminals:select(idx)
        end,
        desc = "Lazygit terminal",
      },

      {
        "<leader>h1",
        function()
          harpoon:list():select(1)
        end,
        desc = "Jump to file 1",
      },

      {
        "<leader>h2",
        function()
          harpoon:list():select(2)
        end,
        desc = "Jump to file 2",
      },

      {
        "<leader>h3",
        function()
          harpoon:list():select(3)
        end,
        desc = "Jump to file 3",
      },

      {
        "<leader>h4",
        function()
          harpoon:list():select(4)
        end,
        desc = "Jump to file 4",
      },
    })
  end,
}

-- Keymaps are automatically loaded on the VeryLazy event
-- Default keymaps that are always set: https://github.com/LazyVim/LazyVim/blob/main/lua/lazyvim/config/keymaps.lua
-- Add any additional keymaps here
-- Yanks remotely
vim.keymap.set("v", "<leader>y", function()
  require("osc52").copy_visual()
end, { desc = "Yank to system clipboard (OSC52)" })

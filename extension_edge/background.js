// Listen for the context menu item click
chrome.runtime.onInstalled.addListener(function () {
  // Create a context menu item for images
  chrome.contextMenus.create({
    id: "saveImageAs",
    title: "Save Image As",
    contexts: ["image"],
  });
});

// Listen for the context menu item click
chrome.contextMenus.onClicked.addListener(function (info, tab) {
  if (info.menuItemId === "saveImageAs") {
    // Download the image
    chrome.downloads.download({
      url: info.srcUrl,
      filename: "downloaded_image.jpg",
      saveAs: true,
    });
  }
});

// Listen for the keyboard shortcut command
chrome.commands.onCommand.addListener(function (command) {
  if (command === "save-image-as") {
    // Get the active tab
    chrome.tabs.query({ active: true, currentWindow: true }, function (tabs) {
      chrome.tabs.sendMessage(tabs[0].id, { action: "saveImageAs" });
    });
  }
});

// Listen for messages from the background script
chrome.runtime.onMessage.addListener(function (request, sender, sendResponse) {
  if (request.action === "saveImageAs") {
    // Find the first image on the page
    const image = document.querySelector("img");
    if (image) {
      // Trigger a download
      chrome.runtime.sendMessage({
        url: image.src,
        filename: "downloaded_image.jpg",
      });
    }
  }
});

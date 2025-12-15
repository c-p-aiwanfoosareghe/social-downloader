async function download() {
  const url = document.getElementById("url").value;
  const status = document.getElementById("status");

  if (!url) {
    status.textContent = "Paste a video link.";
    return;
  }

  status.textContent = "Downloading...";

  try {
    const res = await fetch("/api/download", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ url })
    });

    const data = await res.json();

    if (!data.ok) {
      status.textContent = "Download failed.";
      return;
    }

    // 🔴 iOS SAFE DOWNLOAD
    const a = document.createElement("a");
    a.href = data.download_url;
    a.download = "";
    document.body.appendChild(a);
    a.click();
    a.remove();

    status.textContent = "Download completed. Check Safari downloads.";

  } catch (e) {
    status.textContent = "Error occurred.";
  }
}

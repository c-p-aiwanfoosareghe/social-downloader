async function download() {
  const url = document.getElementById("url").value;
  const status = document.getElementById("status");

  if (!url) {
    status.textContent = "Please paste a link.";
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

    if (data.ok) {
      const a = document.createElement("a");
      a.href = data.video_url;
      a.download = "";
      document.body.appendChild(a);
      a.click();
      a.remove();
      status.textContent = "Download complete!";
    } else {
      status.textContent = "Download failed.";
    }
  } catch (err) {
    status.textContent = "Error downloading.";
  }
}

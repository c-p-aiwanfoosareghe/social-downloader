const btn = document.getElementById("downloadBtn");
const input = document.getElementById("urlInput");
const loading = document.getElementById("loading");
const result = document.getElementById("result");
const link = document.getElementById("downloadLink");

btn.addEventListener("click", async () => {
  const url = input.value.trim();
  if (!url) return alert("Paste a video link");

  loading.classList.remove("hidden");
  result.classList.add("hidden");

  try {
    const res = await fetch("/scrape", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ url })
    });

    const json = await res.json();
    loading.classList.add("hidden");

    if (json.ok && json.data.video_url) {
      link.href = json.data.video_url;
      result.classList.remove("hidden");

      // Auto-download on mobile
      setTimeout(() => {
        const a = document.createElement("a");
        a.href = json.data.video_url;
        a.download = "";
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
      }, 500);
    } else {
      alert("Download failed");
    }
  } catch {
    loading.classList.add("hidden");
    alert("Server error");
  }
});

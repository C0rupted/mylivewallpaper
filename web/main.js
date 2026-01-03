const API_URL = "http://localhost:8000/api/";

const videoEl = document.getElementById("bg-video");



async function setWallpaper(url) {
    const res = await fetch(url);
    if (!res.ok) throw new Error("Failed to fetch video");

    const blob = await res.blob();
    const blobUrl = URL.createObjectURL(blob);

    videoEl.src = blobUrl;
    videoEl.play().catch(() => {});
}


async function init() {
    try {
        await setWallpaper(API_URL + "wallpaper");
    } catch (e) {
        console.error("Error initializing:", e);
    }
}

init();

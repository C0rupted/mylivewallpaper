const API_URL = "/api/";
const container = document.getElementById("wallpaper-container");
const searchBar = document.getElementById("search-bar");
const gridBtn = document.getElementById("grid-btn");
const listBtn = document.getElementById("list-btn");

let wallpapers = [];
let currentSelection = null;
let currentView = "grid";

async function fetchWallpapers() {
    const res = await fetch(API_URL + "wallpapers");
    const data = await res.json();
    wallpapers = data.wallpapers;
    currentSelection = data.selected;
    renderWallpapers();
}

function getThumbnailURL(filename) {
    return `${API_URL}wallpaper_thumbnails/${filename}`;
}

function renderWallpapers() {
    container.innerHTML = "";
    const filter = searchBar.value.toLowerCase();

    wallpapers
        .filter(name => name.toLowerCase().includes(filter))
        .forEach(name => {
            const wrapper = document.createElement("div");
            wrapper.classList.add("wallpaper-item");
            if (currentSelection === name) wrapper.classList.add("selected");

            const thumb = document.createElement("img");
            thumb.src = getThumbnailURL(name);

            const label = document.createElement("div");
            label.classList.add("wallpaper-name");
            label.textContent = name.replace(/\.[^/.]+$/, "");

            wrapper.appendChild(thumb);
            wrapper.appendChild(label);

            wrapper.addEventListener("click", async () => {
                await selectWallpaper(name);
                document.querySelectorAll(".wallpaper-item").forEach(el => el.classList.remove("selected"));
                wrapper.classList.add("selected");
            });

            container.appendChild(wrapper);
        });
}

async function selectWallpaper(name) {
    const res = await fetch(API_URL + "select_wallpaper", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({name})
    });
    if (res.ok) currentSelection = name;
}

searchBar.addEventListener("input", renderWallpapers);

gridBtn.addEventListener("click", () => {
    container.classList.remove("list");
    container.classList.add("grid");
    currentView = "grid";
    gridBtn.classList.add("active");
    listBtn.classList.remove("active");
});

listBtn.addEventListener("click", () => {
    container.classList.remove("grid");
    container.classList.add("list");
    currentView = "list";
    listBtn.classList.add("active");
    gridBtn.classList.remove("active");
});

document.getElementById("open-folder-btn").addEventListener("click", async () => {
    await fetch(API_URL + "open_wallpaper_folder", { method: "POST" });
});


fetchWallpapers();

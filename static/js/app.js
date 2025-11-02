import { Modal } from './modal.js';

const API_URL = '/api/';
const STORAGE_KEY = 'mylivewallpaper:selected-wallpaper';

const videoEl = document.getElementById('bg-video');
const btn = document.getElementById('settings-btn');

async function fetchWallpapers() {
	const res = await fetch(API_URL + "wallpapers");
	if (!res.ok) throw new Error('Failed to fetch wallpapers');
	return await res.json();
}


function setWallpaper(url) {
	if (!url) return;
	videoEl.src = url;
	videoEl.play().catch(() => {});
	localStorage.setItem(STORAGE_KEY, url);
}

function getSavedWallpaper() {
	return localStorage.getItem(STORAGE_KEY);
}

async function openSelector(wallpapers) {
	const modal = new Modal({ title: 'Choose Wallpaper' });

	const grid = document.createElement('div');
	grid.className = 'grid';

	let selected = getSavedWallpaper();

	for (const wp of wallpapers) {
		const thumb = document.createElement('div');
		thumb.className = 'thumb';
		thumb.dataset.video = wp.video;

		const img = document.createElement('img');
		img.src = wp.thumbnail;
		const label = document.createElement('div');
		label.className = 'label';
		label.textContent = wp.name;

		thumb.appendChild(img);
		thumb.appendChild(label);
		grid.appendChild(thumb);

		if (wp.video === selected) thumb.classList.add('selected');

		thumb.addEventListener('click', () => {
			grid.querySelectorAll('.selected').forEach(el => el.classList.remove('selected'));
			thumb.classList.add('selected');
			selected = wp.video;
		});
	}

	const footer = document.createElement('div');
	footer.className = 'modal-footer';

	const openFolder = document.createElement('button');
	openFolder.className = 'btn ghost';
	openFolder.textContent = '📁 Open Folder';
	openFolder.addEventListener('click', async () => {
		try {
			await fetch('/api/openwallpaperfolder');
		} catch (err) {
			console.error('Failed to open folder:', err);
		}
	});

	const cancel = document.createElement('button');
	cancel.className = 'btn ghost';
	cancel.textContent = 'Cancel';
	cancel.addEventListener('click', () => modal.close());

	const confirm = document.createElement('button');
	confirm.className = 'btn primary';
	confirm.textContent = 'Confirm';
	confirm.addEventListener('click', () => {
		if (selected) setWallpaper(selected);
		modal.close();
	});

	footer.appendChild(openFolder);
	footer.appendChild(cancel);
	footer.appendChild(confirm);

	const wrapper = document.createElement('div');
	wrapper.appendChild(grid);
	wrapper.appendChild(footer);

	modal.setContent(wrapper);
	modal.open();
}

async function init() {
	
	const res = await fetch(API_URL + "menubarheight");
	if (!res.ok) throw new Error('Failed to fetch menubarheight');
	const menubarheight = await res.json();

	document.getElementById('bg-video').style.top = "-" + menubarheight + "px";
	document.getElementById('bg-video').style.height = "calc(100% + " + menubarheight + "px)";

	
	try {
		let wallpapers = await fetchWallpapers();

		const saved = getSavedWallpaper();
		if (saved && wallpapers.some(w => w.video === saved)) {
			setWallpaper(saved);
		} else {
			setWallpaper(wallpapers[0]?.video);
		}

		btn.addEventListener('click', async () => {
			wallpapers = await fetchWallpapers();
			await openSelector(wallpapers);
		});
	} catch (e) {
		console.error('Error initializing:', e);
	}
}

init();

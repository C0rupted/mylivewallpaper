export class Modal {
	constructor({ title = "Modal" } = {}) {
		this.overlay = document.createElement("div");
		this.overlay.className = "modal-overlay";

		this.modal = document.createElement("div");
		this.modal.className = "modal";

		const header = document.createElement("div");
		header.className = "modal-header";
		const h2 = document.createElement("h2");
		h2.textContent = title;
		const close = document.createElement("span");
		close.className = "modal-close";
		close.innerHTML = "&times;";
		close.addEventListener("click", () => this.close());
		header.appendChild(h2);
		header.appendChild(close);

		this.content = document.createElement("div");
		this.content.className = "modal-content";

		this.modal.appendChild(header);
		this.modal.appendChild(this.content);

		this.overlay.appendChild(this.modal);
		this.overlay.addEventListener("click", (e) => {
			if (e.target === this.overlay) this.close();
		});

    	document.body.appendChild(this.overlay);
	}

	setContent(el) {
		this.content.innerHTML = "";
		this.content.appendChild(el);
	}

	open() {
		this.overlay.classList.add("open");
		setTimeout(() => this.modal.classList.add("open"), 10);
	}

	close() {
		this.modal.classList.remove("open");
		setTimeout(() => {
			this.overlay.classList.remove("open");
			setTimeout(() => this.overlay.remove(), 200);
		}, 100);
	}
}

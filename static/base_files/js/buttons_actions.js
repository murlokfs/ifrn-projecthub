document.addEventListener("click", (e) => {
    const btn = e.target.closest("[data-action]");
    if (!btn) return;

    const action = btn.getAttribute("data-action");

    if (action.startsWith("go:")) {
        const url = action.replace("go:", "").trim();
        window.location.href = url;
        return;
    }

    if (action === "closeModal") {
        const modal = document.querySelector(".modal-backdrop.visible");
        if (modal) modal.classList.remove("visible");
        return;
    }

    if (action === "openPublishModal") {
        const evt = new CustomEvent("openPublishModal", { bubbles: true });
        document.dispatchEvent(evt);
        return;
    }
});
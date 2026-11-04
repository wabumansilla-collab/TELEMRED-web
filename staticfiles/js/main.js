document.addEventListener("DOMContentLoaded", () => {
    // --- PARTÍCULAS DEL CURSOR ---
    const cursorParticles = document.createElement("div");
    cursorParticles.id = "cursor-particles";
    document.body.appendChild(cursorParticles);

    document.addEventListener("mousemove", (e) => {
        cursorParticles.style.left = e.clientX + "px";
        cursorParticles.style.top = e.clientY + "px";
        cursorParticles.style.opacity = "0.8";

        clearTimeout(cursorParticles.timer);
        cursorParticles.timer = setTimeout(() => {
            cursorParticles.style.opacity = "0";
        }, 400);
    });

    // --- SISTEMA DE TOASTS ---
    window.showToast = function(message, type = 'success') {
        let container = document.querySelector('.toast-container');
        if (!container) {
            container = document.createElement('div');
            container.className = 'toast-container';
            document.body.appendChild(container);
        }
        
        const toast = document.createElement('div');
        toast.className = 'toast';
        toast.innerHTML = `
            <span style="font-size: 1.2rem;">${type === 'success' ? '🚀' : '⚠️'}</span>
            <span>${message}</span>
        `;
        
        if (type === 'error') {
            toast.style.borderColor = '#FF6B9D';
            toast.style.borderLeftColor = '#FF6B9D';
        }
        
        container.appendChild(toast);
        
        setTimeout(() => {
            toast.style.opacity = '0';
            toast.style.transform = 'translateX(50px)';
            toast.style.transition = 'all 0.3s ease';
            setTimeout(() => toast.remove(), 300);
        }, 3500);
    };

    // --- BÚSQUEDA Y FILTRADO EN VIVO DE PRODUCTOS ---
    const searchInput = document.getElementById("product-search");
    const filterPills = document.querySelectorAll(".filter-pill");
    const productCards = document.querySelectorAll(".product-card-wrapper");

    if (searchInput || filterPills.length > 0) {
        let activeFilter = 'all';

        function filterProducts() {
            const query = searchInput ? searchInput.value.toLowerCase().trim() : '';

            productCards.forEach(card => {
                const title = card.getAttribute('data-name') || '';
                const type = card.getAttribute('data-type') || 'all';
                const category = card.getAttribute('data-category') || '';

                const matchesQuery = title.toLowerCase().includes(query) || category.toLowerCase().includes(query);
                const matchesFilter = activeFilter === 'all' || type === activeFilter;

                if (matchesQuery && matchesFilter) {
                    card.style.display = 'block';
                    setTimeout(() => card.style.opacity = '1', 50);
                } else {
                    card.style.opacity = '0';
                    setTimeout(() => card.style.display = 'none', 200);
                }
            });
        }

        if (searchInput) {
            searchInput.addEventListener("input", filterProducts);
        }

        filterPills.forEach(pill => {
            pill.addEventListener("click", () => {
                filterPills.forEach(p => p.classList.remove("active"));
                pill.classList.add("active");
                activeFilter = pill.getAttribute("data-filter");
                filterProducts();
            });
        });
    }

    // --- SIMULACIÓN DEL PUNTO DE VENTA (POS) INTERACTIVO ---
    const posProducts = document.querySelectorAll(".pos-add-btn");
    const posTableBody = document.getElementById("pos-cart-body");
    const posTotalEl = document.getElementById("pos-total");
    const posCheckoutBtn = document.getElementById("pos-checkout-btn");
    const posClearBtn = document.getElementById("pos-clear-btn");

    if (posTableBody && posTotalEl) {
        let posCart = [];

        function updatePosCart() {
            posTableBody.innerHTML = '';
            if (posCart.length === 0) {
                posTableBody.innerHTML = `<tr><td colspan="4" style="text-align: center; color: var(--text-muted);">Terminal vacía. Seleccione productos a la izquierda.</td></tr>`;
                posTotalEl.textContent = '$0.00';
                return;
            }

            let total = 0;
            posCart.forEach((item, index) => {
                const subtotal = item.price * item.quantity;
                total += subtotal;

                const row = document.createElement("tr");
                row.innerHTML = `
                    <td><b>${item.name}</b><br><small style="color: var(--text-accent);">${item.type === 'physical' ? '📦 Físico' : '⚡ Servicio'}</small></td>
                    <td>$${item.price.toFixed(2)}</td>
                    <td>
                        <button class="pos-qty-btn" onclick="changePosQty(${index}, -1)">-</button>
                        <span style="margin: 0 8px;">${item.quantity}</span>
                        <button class="pos-qty-btn" onclick="changePosQty(${index}, 1)">+</button>
                    </td>
                    <td>$${subtotal.toFixed(2)}</td>
                `;
                posTableBody.appendChild(row);
            });

            posTotalEl.textContent = `$${total.toFixed(2)}`;
        }

        window.changePosQty = function(index, delta) {
            posCart[index].quantity += delta;
            if (posCart[index].quantity <= 0) {
                posCart.splice(index, 1);
            }
            updatePosCart();
        };

        posProducts.forEach(btn => {
            btn.addEventListener("click", () => {
                const id = btn.getAttribute("data-id");
                const name = btn.getAttribute("data-name");
                const price = parseFloat(btn.getAttribute("data-price"));
                const type = btn.getAttribute("data-type");

                const existing = posCart.find(item => item.id === id);
                if (existing) {
                    existing.quantity += 1;
                } else {
                    posCart.push({ id, name, price, type, quantity: 1 });
                }
                updatePosCart();
                showToast(`Añadido: ${name}`, 'success');
            });
        });

        if (posClearBtn) {
            posClearBtn.addEventListener("click", () => {
                posCart = [];
                updatePosCart();
                showToast("Terminal POS reiniciada", 'success');
            });
        }

        if (posCheckoutBtn) {
            posCheckoutBtn.addEventListener("click", () => {
                if (posCart.length === 0) {
                    showToast("No hay ítems para procesar", 'error');
                    return;
                }
                const totalText = posTotalEl.textContent;
                posCart = [];
                updatePosCart();
                showToast(`Transacción POS aprobada por ${totalText} ✅ Recibo impreso.`, 'success');
            });
        }
    }
});

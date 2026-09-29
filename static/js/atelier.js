/**
 * STYLE SPHERE ATELIER — Master Interactive Luxury Experience
 * Features:
 *  1. Boutique Cursor-Following Spotlight Glow
 *  2. Interactive 240+ GSM Fabric Weave Inspector Modal
 *  3. Zero-Reload AJAX Wishlist Toggle with Haptic Particle Pulse
 *  4. Zero-Reload AJAX Quick-Add to Bag with Counter Updates
 *  5. Lookbook Grid vs Runway Magazine View Switcher (Persistent)
 *  6. Boxy Fit Silhouette Calculator
 *  7. Floating Luxury Toast Notification Engine
 */

// --- 1. CSRF Helper ---
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// --- 2. Boutique Cursor-Following Spotlight Glow ---
function initBoutiqueSpotlight() {
    const cards = document.querySelectorAll('.luxury-card, .spotlight-card');
    cards.forEach(card => {
        card.addEventListener('mousemove', e => {
            const rect = card.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;
            card.style.setProperty('--mouse-x', `${x}px`);
            card.style.setProperty('--mouse-y', `${y}px`);
        });
    });
}

// --- 3. Interactive Fabric Weave Inspector Modal ---
function openFabricInspector(pieceName = 'Heavyweight Atelier Piece', gsm = 240) {
    const modal = document.getElementById('fabricInspectorModal');
    const title = document.getElementById('fabricModalPieceName');
    const slider = document.getElementById('fabricGsmSlider');
    if (!modal) return;

    if (title) title.innerText = `${pieceName} • Heavyweight Specification`;
    if (slider) {
        slider.value = gsm;
        updateFabricSimulator(gsm);
    }
    modal.classList.remove('hidden');
    document.body.style.overflow = 'hidden';
}

function closeFabricInspector() {
    const modal = document.getElementById('fabricInspectorModal');
    if (!modal) return;
    modal.classList.add('hidden');
    document.body.style.overflow = '';
}

function updateFabricSimulator(val) {
    val = parseInt(val, 10);
    const canvas = document.getElementById('fabricTextureCanvas');
    const readout = document.getElementById('gsmReadout');
    const subtext = document.getElementById('gsmSubtext');
    const gradeBadge = document.getElementById('fabricGradeBadge');
    const zoomDisplay = document.getElementById('zoomLevelDisplay');

    if (readout) readout.innerText = `${val}+ GSM`;

    if (canvas) {
        // Adjust weave grid density based on GSM
        const step = Math.max(2, Math.round(14 - (val / 25)));
        canvas.style.backgroundSize = `100% 100%, ${step}px ${step}px, ${step}px ${step}px`;
    }

    if (val < 190) {
        if (subtext) subtext.innerText = "Commercial Single-Jersey • Translucent Hand-Feel";
        if (gradeBadge) {
            gradeBadge.innerText = "STANDARD COMMERCIAL";
            gradeBadge.className = "px-2.5 py-1 rounded bg-zinc-800 text-zinc-300 font-mono text-[9px] uppercase";
        }
        if (zoomDisplay) zoomDisplay.innerText = "20X OPTICAL MACRO";
    } else if (val < 230) {
        if (subtext) subtext.innerText = "Mid-Weight Combed Cotton • Standard Casual Fit";
        if (gradeBadge) {
            gradeBadge.innerText = "MID-WEIGHT TEE";
            gradeBadge.className = "px-2.5 py-1 rounded bg-zinc-700 text-white font-mono text-[9px] uppercase";
        }
        if (zoomDisplay) zoomDisplay.innerText = "35X OPTICAL MACRO";
    } else {
        if (subtext) subtext.innerText = "Heavy French Terry Loopback • Boxy Tailored Drape";
        if (gradeBadge) {
            gradeBadge.innerText = `${val} GSM ATELIER BESPOKE`;
            gradeBadge.className = "px-2.5 py-1 rounded bg-luxury-gold text-black font-bold font-mono text-[9px] uppercase tracking-wider";
        }
        if (zoomDisplay) zoomDisplay.innerText = "60X OPTICAL MACRO";
    }
}

// --- 4. Zero-Reload AJAX Wishlist Toggle ---
async function toggleWishlistAjax(event, productId, url) {
    if (event) event.preventDefault();
    const btn = event.currentTarget || event.target.closest('a');
    const icon = btn ? btn.querySelector('i') : null;

    try {
        const response = await fetch(url, {
            method: 'GET',
            headers: {
                'X-Requested-With': 'XMLHttpRequest'
            }
        });

        if (response.ok) {
            const data = await response.json();
            if (data.status === 'ok') {
                if (data.action === 'added') {
                    if (icon) {
                        icon.className = 'bi bi-heart-fill text-luxury-gold scale-125 transition-transform duration-300';
                        setTimeout(() => icon.classList.remove('scale-125'), 300);
                    }
                    showAtelierToast(data.message || 'Piece added to your Private Archive', 'wishlist');
                } else {
                    if (icon) {
                        icon.className = 'bi bi-heart text-zinc-400 transition-colors';
                    }
                    showAtelierToast(data.message || 'Piece removed from your Wishlist', 'info');
                }

                // Update Header Wishlist Badge
                updateWishlistBadges(data.total_wishlist);
            }
        } else {
            // Fallback for unauthenticated users redirecting to login
            window.location.href = url;
        }
    } catch (err) {
        window.location.href = url;
    }
}

function updateWishlistBadges(count) {
    const badges = document.querySelectorAll('.wishlist-counter-badge');
    badges.forEach(b => {
        b.innerText = count;
        if (count > 0) b.classList.remove('hidden');
        else b.classList.add('hidden');
    });
}

// --- 5. Zero-Reload AJAX Quick-Add to Bag ---
async function addToBagAjax(event, formElement) {
    if (event) event.preventDefault();
    const form = formElement || event.target;
    const url = form.action;
    const formData = new FormData(form);
    const submitBtn = form.querySelector('button[type="submit"]');

    if (submitBtn) {
        submitBtn.disabled = true;
        submitBtn.classList.add('opacity-75');
    }

    try {
        const response = await fetch(url, {
            method: 'POST',
            body: formData,
            headers: {
                'X-Requested-With': 'XMLHttpRequest'
            }
        });

        if (response.ok) {
            const data = await response.json();
            if (data.status === 'ok') {
                showAtelierToast(`✓ ${data.product_name} (${data.size}) added to your Bag`, 'bag');
                updateBagBadges(data.total_items);
            } else {
                showAtelierToast(data.message || 'Item could not be added', 'error');
            }
        } else {
            form.submit();
        }
    } catch (e) {
        form.submit();
    } finally {
        if (submitBtn) {
            submitBtn.disabled = false;
            submitBtn.classList.remove('opacity-75');
        }
    }
}

function updateBagBadges(count) {
    const badges = document.querySelectorAll('.bag-counter-badge');
    badges.forEach(b => {
        b.innerText = count;
        if (count > 0) b.classList.remove('hidden');
        else b.classList.add('hidden');
    });
}

// --- 6. Lookbook Grid vs Runway Magazine View Switcher ---
function setCatalogView(mode) {
    const grid = document.getElementById('piecesCatalogGrid');
    const gridBtn = document.getElementById('viewGridBtn');
    const runwayBtn = document.getElementById('viewRunwayBtn');
    if (!grid) return;

    if (mode === 'runway') {
        // Dramatic 2-Column Staggered Editorial Runway Format
        grid.className = 'grid grid-cols-1 md:grid-cols-2 gap-8 lg:gap-12';
        if (runwayBtn) {
            runwayBtn.className = 'px-3 py-1.5 rounded-lg text-xs font-mono uppercase tracking-wider transition-all bg-white text-black font-bold shadow-md';
        }
        if (gridBtn) {
            gridBtn.className = 'px-3 py-1.5 rounded-lg text-xs font-mono uppercase tracking-wider transition-all text-zinc-400 hover:text-white';
        }
        localStorage.setItem('atelier_catalog_view', 'runway');
    } else {
        // Standard 4-Column Shopping Lookbook Grid
        grid.className = 'grid grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-3.5 sm:gap-6 lg:gap-8';
        if (gridBtn) {
            gridBtn.className = 'px-3 py-1.5 rounded-lg text-xs font-mono uppercase tracking-wider transition-all bg-white text-black font-bold shadow-md';
        }
        if (runwayBtn) {
            runwayBtn.className = 'px-3 py-1.5 rounded-lg text-xs font-mono uppercase tracking-wider transition-all text-zinc-400 hover:text-white';
        }
        localStorage.setItem('atelier_catalog_view', 'grid');
    }
}

function initCatalogView() {
    const saved = localStorage.getItem('atelier_catalog_view');
    if (saved === 'runway') {
        setCatalogView('runway');
    }
}

// --- 7. Boxy Fit Silhouette Calculator ---
function selectFitSilhouette(mode) {
    const note = document.getElementById('silhouetteNote');
    const recSize = document.getElementById('recommendedSizeDisplay');
    const buttons = document.querySelectorAll('.silhouette-toggle-btn');

    buttons.forEach(btn => {
        btn.classList.remove('bg-white', 'text-black', 'font-bold');
        btn.classList.add('text-zinc-400');
    });

    const activeBtn = document.getElementById(`fitBtn_${mode}`);
    if (activeBtn) {
        activeBtn.classList.add('bg-white', 'text-black', 'font-bold');
        activeBtn.classList.remove('text-zinc-400');
    }

    if (!note) return;

    if (mode === 'clean') {
        note.innerHTML = "<strong>Clean Tailored Fit:</strong> Sits naturally at the shoulder seam. Order your standard size for an everyday fitted silhouette.";
        if (recSize) recSize.innerText = "RECOMMENDED: M";
    } else if (mode === 'boxy') {
        note.innerHTML = "<strong>Signature Atelier Boxy Drape:</strong> 2.5-inch dropped shoulder with wide chest box. True to modern luxury oversized proportions.";
        if (recSize) recSize.innerText = "RECOMMENDED: L (SIGNATURE)";
    } else if (mode === 'baggy') {
        note.innerHTML = "<strong>Harajuku Runway Volume:</strong> Exaggerated drape extending past elbows with generous torso length. Size up once for maximum street presence.";
        if (recSize) recSize.innerText = "RECOMMENDED: XL";
    }
}

// --- 8. Floating Luxury Toast Notification Engine ---
function showAtelierToast(message, type = 'info') {
    let container = document.getElementById('atelierToastContainer');
    if (!container) {
        container = document.createElement('div');
        container.id = 'atelierToastContainer';
        container.className = 'fixed bottom-20 sm:bottom-8 right-4 sm:right-8 z-50 pointer-events-none flex flex-col gap-2.5 max-w-sm w-full';
        document.body.appendChild(container);
    }

    const toast = document.createElement('div');
    toast.className = 'pointer-events-auto p-4 rounded-2xl bg-[#111114]/95 backdrop-blur-2xl border border-luxury-gold/40 text-white shadow-[0_20px_50px_rgba(0,0,0,0.8)] flex items-center justify-between gap-3 transform translate-y-4 opacity-0 transition-all duration-300';

    let iconHtml = '<i class="bi bi-gem text-luxury-gold text-lg"></i>';
    if (type === 'wishlist') iconHtml = '<i class="bi bi-heart-fill text-luxury-gold text-lg"></i>';
    else if (type === 'bag') iconHtml = '<i class="bi bi-bag-check-fill text-luxury-gold text-lg"></i>';
    else if (type === 'error') iconHtml = '<i class="bi bi-exclamation-octagon-fill text-rose-400 text-lg"></i>';

    toast.innerHTML = `
        <div class="flex items-center gap-3">
            <div class="w-8 h-8 rounded-xl bg-zinc-900 border border-zinc-800 flex items-center justify-center flex-shrink-0">
                ${iconHtml}
            </div>
            <div class="flex flex-col text-left">
                <span class="text-[9px] font-mono text-luxury-gold uppercase tracking-widest">ATELIER NOTICE</span>
                <span class="text-xs font-semibold text-zinc-100">${message}</span>
            </div>
        </div>
        <button type="button" class="text-zinc-500 hover:text-white p-1" onclick="this.parentElement.remove()">
            <i class="bi bi-x text-sm"></i>
        </button>
    `;

    container.appendChild(toast);

    // Trigger smooth slide in
    requestAnimationFrame(() => {
        toast.classList.remove('translate-y-4', 'opacity-0');
    });

    // Auto dismiss after 3.8s
    setTimeout(() => {
        toast.classList.add('translate-y-4', 'opacity-0');
        setTimeout(() => toast.remove(), 300);
    }, 3800);
}


// --- 10. Web Audio API Sensory Branding ---
const AtelierAudio = (function() {
    let ctx = null;
    let enabled = localStorage.getItem('stylesphere_sfx') !== 'false';

    function getAudioContext() {
        if (!ctx && (window.AudioContext || window.webkitAudioContext)) {
            const AudioCtx = window.AudioContext || window.webkitAudioContext;
            ctx = new AudioCtx();
        }
        if (ctx && ctx.state === 'suspended') {
            ctx.resume();
        }
        return ctx;
    }

    return {
        isEnabled: () => enabled,
        toggle: function() {
            enabled = !enabled;
            localStorage.setItem('stylesphere_sfx', enabled);
            const btn = document.getElementById('sfx-toggle-btn');
            if (btn) {
                btn.innerHTML = enabled ? 'SFX: <span class="text-emerald-400 font-bold">ON</span>' : 'SFX: <span class="text-zinc-500 font-bold">OFF</span>';
            }
            if (enabled) this.playClick();
            return enabled;
        },
        playClick: function() {
            if (!enabled) return;
            try {
                const c = getAudioContext();
                if (!c) return;
                const osc = c.createOscillator();
                const gain = c.createGain();
                osc.type = 'sine';
                osc.frequency.setValueAtTime(800, c.currentTime);
                osc.frequency.exponentialRampToValueAtTime(320, c.currentTime + 0.035);
                gain.gain.setValueAtTime(0.06, c.currentTime);
                gain.gain.exponentialRampToValueAtTime(0.001, c.currentTime + 0.035);
                osc.connect(gain);
                gain.connect(c.destination);
                osc.start();
                osc.stop(c.currentTime + 0.04);
            } catch(e) {}
        },
        playChime: function() {
            if (!enabled) return;
            try {
                const c = getAudioContext();
                if (!c) return;
                const freqs = [523.25, 659.25, 783.99, 1046.50];
                freqs.forEach((freq, i) => {
                    const osc = c.createOscillator();
                    const gain = c.createGain();
                    osc.type = 'sine';
                    osc.frequency.setValueAtTime(freq, c.currentTime + (i * 0.04));
                    gain.gain.setValueAtTime(0.04, c.currentTime + (i * 0.04));
                    gain.gain.exponentialRampToValueAtTime(0.0001, c.currentTime + 0.3 + (i * 0.04));
                    osc.connect(gain);
                    gain.connect(c.destination);
                    osc.start(c.currentTime + (i * 0.04));
                    osc.stop(c.currentTime + 0.35 + (i * 0.04));
                });
            } catch(e) {}
        }
    };
})();

// --- 11. 10x Textile Microscopy Loupe ---
function initTextileLoupe() {
    const mainImg = document.getElementById('mainGalleryImage') || document.getElementById('main-product-image');
    if (!mainImg) return;

    const container = mainImg.parentElement;
    if (!container) return;
    container.style.position = 'relative';

    let loupe = document.getElementById('textile-loupe');
    if (!loupe) {
        loupe = document.createElement('div');
        loupe.id = 'textile-loupe';
        loupe.className = 'hidden md:block pointer-events-none absolute w-40 h-40 rounded-full border border-amber-400/50 shadow-2xl overflow-hidden z-30 opacity-0 transition-opacity duration-150';
        loupe.style.backgroundRepeat = 'no-repeat';
        loupe.style.boxShadow = '0 0 30px rgba(251, 191, 36, 0.3), inset 0 0 20px rgba(0,0,0,0.85)';
        container.appendChild(loupe);
    }

    container.addEventListener('mouseenter', () => {
        if (!mainImg.src) return;
        loupe.style.backgroundImage = 'url("' + mainImg.src + '")';
        loupe.style.opacity = '1';
    });

    container.addEventListener('mouseleave', () => {
        loupe.style.opacity = '0';
    });

    container.addEventListener('mousemove', (e) => {
        const rect = container.getBoundingClientRect();
        const x = e.clientX - rect.left;
        const y = e.clientY - rect.top;

        if (x < 0 || y < 0 || x > rect.width || y > rect.height) {
            loupe.style.opacity = '0';
            return;
        }

        loupe.style.opacity = '1';
        loupe.style.left = (x - 80) + 'px';
        loupe.style.top = (y - 80) + 'px';

        const zoom = 2.5;
        loupe.style.backgroundSize = (rect.width * zoom) + 'px ' + (rect.height * zoom) + 'px';
        loupe.style.backgroundPosition = '-' + (x * zoom - 80) + 'px -' + (y * zoom - 80) + 'px';
    });
}

// --- 12. Cart Abandonment Exit-Intent Privilege Modal ---
function initExitIntentPrivilege() {
    let triggered = sessionStorage.getItem('stylesphere_exit_intent_shown');
    if (triggered) return;

    document.addEventListener('mouseleave', (e) => {
        if (e.clientY <= 10 && !triggered) {
            triggered = true;
            sessionStorage.setItem('stylesphere_exit_intent_shown', 'true');
            showExitPrivilegeModal();
        }
    });
}

function showExitPrivilegeModal() {
    if (document.getElementById('exit-intent-modal')) return;
    const modal = document.createElement('div');
    modal.id = 'exit-intent-modal';
    modal.className = 'fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/80 backdrop-blur-md transition-opacity duration-300 opacity-0';
    modal.innerHTML = `
        <div class="bg-zinc-950 border border-zinc-800 rounded-2xl max-w-md w-full p-8 text-center space-y-6 shadow-2xl relative">
            <button onclick="document.getElementById('exit-intent-modal').remove()" class="absolute top-4 right-4 text-zinc-500 hover:text-white text-lg p-2">&times;</button>
            <div class="w-12 h-12 mx-auto rounded-full bg-amber-500/10 border border-amber-500/30 flex items-center justify-center text-amber-400 text-xl">
                ✦
            </div>
            <div>
                <span class="text-[10px] font-mono tracking-[0.25em] text-zinc-400 uppercase">ATELIER PRIVILEGE</span>
                <h3 class="text-xl font-luxury font-bold text-white mt-1">Before You Conclude Your Visit</h3>
                <p class="text-xs text-zinc-400 mt-2 leading-relaxed">
                    Enjoy complimentary insured delivery and an exclusive 10% privilege reduction on your order with code.
                </p>
            </div>
            <div class="bg-zinc-900 border border-zinc-800 rounded-xl p-3 text-center">
                <span class="text-[10px] text-zinc-500 uppercase tracking-widest block">Privilege Code</span>
                <span class="text-sm font-mono font-bold text-amber-300 tracking-wider">ATELIER10</span>
            </div>
            <div class="flex gap-3">
                <a href="/cart/" class="flex-1 py-3 bg-white hover:bg-zinc-200 text-black text-xs font-semibold uppercase tracking-wider rounded-xl transition-all">View Bag</a>
                <button onclick="document.getElementById('exit-intent-modal').remove()" class="py-3 px-4 bg-zinc-900 hover:bg-zinc-800 text-zinc-300 text-xs font-medium rounded-xl border border-zinc-800 transition-all">Continue Browsing</button>
            </div>
        </div>
    `;
    document.body.appendChild(modal);
    requestAnimationFrame(() => modal.classList.remove('opacity-0'));
}

// --- 13. Instant Search Autocomplete with Live Suggestions ---
function initLiveSearchAutocomplete() {
    const searchInputs = document.querySelectorAll('input[name="q"]');
    searchInputs.forEach(input => {
        let debounceTimer = null;
        let suggestionBox = null;

        input.addEventListener('input', (e) => {
            const query = e.target.value.trim();
            clearTimeout(debounceTimer);
            if (query.length < 2) {
                if (suggestionBox) suggestionBox.remove();
                suggestionBox = null;
                return;
            }

            debounceTimer = setTimeout(() => {
                fetch('/api/products/?search=' + encodeURIComponent(query))
                    .then(res => res.json())
                    .then(data => {
                        const results = data.results || (Array.isArray(data) ? data : []);
                        if (!suggestionBox) {
                            suggestionBox = document.createElement('div');
                            suggestionBox.className = 'absolute top-full left-0 right-0 mt-2 bg-zinc-950 border border-zinc-800 rounded-xl shadow-2xl p-2 z-50 space-y-1 max-h-72 overflow-y-auto';
                            input.parentElement.style.position = 'relative';
                            input.parentElement.appendChild(suggestionBox);
                        }

                        if (results.length === 0) {
                            suggestionBox.innerHTML = '<div class="p-3 text-xs text-zinc-500 text-center font-mono">No matching editions found</div>';
                        } else {
                            suggestionBox.innerHTML = results.slice(0, 5).map(p => `
                                <a href="/${p.id}/${p.slug}/" class="flex items-center gap-3 p-2 rounded-lg hover:bg-zinc-900 transition-all text-left group">
                                    <div class="w-10 h-10 rounded bg-zinc-800 overflow-hidden flex-shrink-0">
                                        ${p.image ? `<img src="${p.image}" class="w-full h-full object-cover">` : '<div class="w-full h-full flex items-center justify-center text-[10px] text-zinc-500">No Img</div>'}
                                    </div>
                                    <div class="flex-1 min-w-0">
                                        <p class="text-xs text-white group-hover:text-amber-300 font-medium truncate">${p.name}</p>
                                        <p class="text-[10px] text-zinc-400 font-mono">₹${p.price} • ${p.gsm || 240} GSM</p>
                                    </div>
                                </a>
                            `).join('');
                        }
                    })
                    .catch(() => {});
            }, 250);
        });

        document.addEventListener('click', (e) => {
            if (suggestionBox && !input.contains(e.target) && !suggestionBox.contains(e.target)) {
                suggestionBox.remove();
                suggestionBox = null;
            }
        });
    });
}

// --- 9. Global Init on DOMContentLoaded ---
document.addEventListener('DOMContentLoaded', () => {
    initBoutiqueSpotlight();
    initCatalogView();
    initTextileLoupe();
    initExitIntentPrivilege();
    initLiveSearchAutocomplete();

    // Hook size buttons to sensory click
    document.querySelectorAll('.size-selector-btn, .size-pill, button, a[href*="add"]').forEach(el => {
        el.addEventListener('click', () => {
            if (window.AtelierAudio) AtelierAudio.playClick();
        });
    });

    // Close modal on ESC key
    document.addEventListener('keydown', e => {
        if (e.key === 'Escape') {
            closeFabricInspector();
            const exitM = document.getElementById('exit-intent-modal');
            if (exitM) exitM.remove();
        }
    });
});

// Projects portfolio: filter + search against the DRF API with masonry and lightbox.
(function() {
  const grid = document.getElementById("grid");
  const empty = document.getElementById("empty");
  const loading = document.getElementById("loading");
  const search = document.getElementById("search");
  const statusSel = document.getElementById("status");
  const industrySel = document.getElementById("industry");
  const techSel = document.getElementById("technology");
  const clearBtn = document.getElementById("clear-filters");
  const toggleView = document.getElementById("toggle-view");
  const resultCount = document.getElementById("result-count");
  const quickFilters = document.querySelectorAll(".quick-filter");
  let isListView = false;

  function card(p) {
    const thumb = p.thumbnail
      ? `<img src="${p.thumbnail}" class="card-img-top" alt="${p.title}" loading="lazy">`
      : `<div class="card-img-top bg-blue d-flex align-items-center justify-content-center text-white" style="height:200px"><span class="h4">${p.title.charAt(0)}</span></div>`;
    const badge = p.status === 'ongoing'
      ? '<span class="badge bg-warning text-dark">Ongoing</span>'
      : '<span class="badge bg-success">Completed</span>';
    return `<div class="masonry-item">
      <div class="card project-card h-100 shadow-sm">
        <a href="/projects/${p.slug}/">${thumb}</a>
        <div class="card-body">
          <a href="/projects/${p.slug}/" class="text-decoration-none">
            <h3 class="h6 text-dark">${p.title}</h3>
          </a>
          <p class="text-muted small mb-1">${p.industry_name || p.industry}</p>
          ${badge}
        </div>
      </div>
    </div>`;
  }

  function buildQuery() {
    const params = new URLSearchParams();
    if (search.value.trim()) params.set("search", search.value.trim());
    if (statusSel.value) params.set("status", statusSel.value);
    if (industrySel.value) params.set("industry__slug", industrySel.value);
    if (techSel && techSel.value) params.set("technologies__name", techSel.value);
    const qs = params.toString();
    return qs ? `?${qs}` : "";
  }

  async function loadProjects() {
    if (loading) loading.classList.remove("d-none");
    if (grid) grid.innerHTML = "";
    try {
      const res = await fetch(`/api/v1/projects/${buildQuery()}`);
      const data = await res.json();
      const results = data.results || data;
      if (grid) {
        grid.innerHTML = results.map(card).join("");
        if (isListView) {
          grid.className = 'list-view';
        } else {
          grid.className = 'masonry-grid grid-view';
        }
      }
      if (empty) empty.classList.toggle("d-none", results.length > 0);
      if (resultCount) resultCount.textContent = results.length + " project" + (results.length !== 1 ? "s" : "") + " found";
    } catch (err) {
      if (grid) grid.innerHTML = '<p class="text-muted text-center py-5">Failed to load projects. Please try again.</p>';
    } finally {
      if (loading) loading.classList.add("d-none");
    }
  }

  let debounceTimer;
  function onChange() {
    clearTimeout(debounceTimer);
    debounceTimer = setTimeout(loadProjects, 250);
  }

  if (search) search.addEventListener("input", onChange);
  if (statusSel) statusSel.addEventListener("change", onChange);
  if (industrySel) industrySel.addEventListener("change", onChange);
  if (techSel) techSel.addEventListener("change", onChange);
  if (clearBtn) {
    clearBtn.addEventListener("click", function() {
      if (search) search.value = "";
      if (statusSel) statusSel.value = "";
      if (industrySel) industrySel.value = "";
      if (techSel) techSel.value = "";
      quickFilters.forEach(function(b) { b.className = b.className.replace(" active", ""); b.className = b.className.replace("btn-outline-brand", "btn-outline-secondary"); });
      document.querySelector('.quick-filter[data-filter=""]').className = "btn btn-sm btn-outline-brand quick-filter active";
      loadProjects();
    });
  }
  // Quick filter buttons
  quickFilters.forEach(function(btn) {
    btn.addEventListener("click", function() {
      quickFilters.forEach(function(b) { b.className = b.className.replace(" active", ""); b.className = b.className.replace("btn-outline-brand", "btn-outline-secondary"); });
      this.className = this.className.replace("btn-outline-secondary", "btn-outline-brand") + " active";
      var filter = this.dataset.filter;
      // Map quick filter values to the proper select fields
      if (filter === "ongoing" || filter === "completed") {
        statusSel.value = filter;
        techSel.value = "";
      } else if (filter === "Robotics" || filter === "IIoT" || filter === "Machine Vision" || filter === "AI Analytics") {
        techSel.value = filter;
        statusSel.value = "";
      } else {
        statusSel.value = "";
        techSel.value = "";
      }
      loadProjects();
    });
  });

  if (toggleView) {
    toggleView.addEventListener("click", function() {
      isListView = !isListView;
      if (grid) {
        grid.className = isListView ? 'list-view' : 'masonry-grid grid-view';
      }
      toggleView.innerHTML = isListView
        ? '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="3" width="7" height="7"/><rect x="14" y="3" width="7" height="7"/><rect x="3" y="14" width="7" height="7"/><rect x="14" y="14" width="7" height="7"/></svg>'
        : '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="8" y1="6" x2="21" y2="6"/><line x1="8" y1="12" x2="21" y2="12"/><line x1="8" y1="18" x2="21" y2="18"/><line x1="3" y1="6" x2="3.01" y2="6"/><line x1="3" y1="12" x2="3.01" y2="12"/><line x1="3" y1="18" x2="3.01" y2="18"/></svg>';
    });
  }

  // Lightbox
  document.addEventListener('click', function(e) {
    const trigger = e.target.closest('.gallery-trigger');
    if (trigger) {
      e.preventDefault();
      const lb = document.getElementById('lightbox');
      const lbImg = document.getElementById('lightbox-img');
      if (lb && lbImg) {
        lbImg.src = trigger.dataset.src;
        lb.classList.add('active');
      }
    }
  });

  loadProjects();
})();

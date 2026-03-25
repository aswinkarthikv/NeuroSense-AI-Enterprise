document.addEventListener('DOMContentLoaded', () => {
    // 1. Initialize Logout
    const logoutBtn = document.getElementById('logoutBtn');
    if (logoutBtn) {
        logoutBtn.addEventListener('click', async () => {
            await fetch('/api/v1/auth/logout', { method: 'POST' });
            window.location.href = '/';
        });
    }

    // 2. Load Patient Data if on Dashboard
    const patientTable = document.getElementById('patient-table-body');
    if (patientTable) {
        loadPatients();
        initCharts();
    }

    // 3. Initialize UI Components (Filters, Buttons)
    initUI();
});

async function loadPatients() {
    try {
        const res = await fetch('/api/v1/patients/');
        const data = await res.json();

        if (data.status === 'success') {
            document.getElementById('stat-total-patients').textContent = data.count;
            document.getElementById('table-count').textContent = data.count;

            const tbody = document.getElementById('patient-table-body');
            tbody.innerHTML = ''; // Clear loading

            // Only show top 10 for dashboard
            data.patients.slice(0, 10).forEach((p, idx) => {
                const tr = document.createElement('tr');
                tr.className = `animate-fade-in animate-delay-${(idx % 3) + 1}`;

                // Risk formatting
                let riskBadge = '';
                if (p.baseline_risk > 70) {
                    riskBadge = `<span class="px-2 py-1 bg-rose-100 text-rose-700 rounded text-xs font-bold">${p.baseline_risk.toFixed(1)} High</span>`;
                } else if (p.baseline_risk > 40) {
                    riskBadge = `<span class="px-2 py-1 bg-amber-100 text-amber-700 rounded text-xs font-bold">${p.baseline_risk.toFixed(1)} Med</span>`;
                } else {
                    riskBadge = `<span class="px-2 py-1 bg-emerald-100 text-emerald-700 rounded text-xs font-bold">${p.baseline_risk.toFixed(1)} Low</span>`;
                }

                tr.innerHTML = `
                    <td class="py-3 px-6 border-b border-slate-100 font-mono text-xs text-slate-500">${p.id.split('-')[0]}***</td>
                    <td class="py-3 px-6 border-b border-slate-100 font-medium">
                        <div class="flex items-center">
                            <div class="h-8 w-8 rounded-full bg-indigo-100 text-indigo-600 flex items-center justify-center font-bold mr-3">
                                ${p.name.charAt(0)}
                            </div>
                            <div>
                                <div>${p.name}</div>
                                <div class="text-xs text-slate-400">${p.email}</div>
                            </div>
                        </div>
                    </td>
                    <td class="py-3 px-6 border-b border-slate-100 text-sm">${p.gender}</td>
                    <td class="py-3 px-6 border-b border-slate-100 text-sm">${p.last_assessment}</td>
                    <td class="py-3 px-6 border-b border-slate-100">${riskBadge}</td>
                    <td class="py-3 px-6 border-b border-slate-100 text-right">
                        <a href="/patients/${p.id}" class="text-indigo-600 hover:text-indigo-900 font-medium text-sm">View <i class="fas fa-chevron-right text-xs ml-1"></i></a>
                    </td>
                `;
                tbody.appendChild(tr);
            });
        }
    } catch (err) {
        console.error("Failed to load patients", err);
    }
}

function initCharts() {
    // Shared styling
    Chart.defaults.font.family = "'Outfit', sans-serif";
    Chart.defaults.color = '#64748b';

    // Trajectory Chart
    const ctx1 = document.getElementById('riskTrajectoryChart');
    if (ctx1) {
        new Chart(ctx1, {
            type: 'line',
            data: {
                labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul'],
                datasets: [
                    {
                        label: 'Average Clinic UPDRS Risk',
                        data: [45, 47, 46, 50, 48, 52, 53],
                        borderColor: '#6366f1', // Indigo
                        backgroundColor: 'rgba(99, 102, 241, 0.1)',
                        borderWidth: 2,
                        tension: 0.4,
                        fill: true,
                        pointBackgroundColor: '#fff',
                        pointBorderColor: '#6366f1',
                        pointBorderWidth: 2,
                        pointRadius: 4
                    },
                    {
                        label: 'Baseline Expected',
                        data: [40, 41, 42, 43, 44, 45, 46],
                        borderColor: '#cbd5e1', // Slate 300
                        borderDash: [5, 5],
                        borderWidth: 2,
                        tension: 0.4,
                        fill: false,
                        pointRadius: 0
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: { legend: { position: 'bottom' } },
                scales: {
                    y: { beginAtZero: true, max: 100, grid: { borderDash: [2, 4], color: '#f1f5f9' } },
                    x: { grid: { display: false } }
                }
            }
        });
    }

    // Distribution Chart
    const ctx2 = document.getElementById('riskDistributionChart');
    if (ctx2) {
        new Chart(ctx2, {
            type: 'doughnut',
            data: {
                labels: ['Low Risk', 'Medium Risk', 'High Risk'],
                datasets: [{
                    data: [45, 30, 25], // Mock percentages
                    backgroundColor: ['#10b981', '#f59e0b', '#ef4444'],
                    borderWidth: 0,
                    hoverOffset: 4
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                cutout: '70%',
                plugins: {
                    legend: { position: 'bottom' }
                }
            }
        });
    }
}

function initUI() {
    // Notifications Mock
    const notifBtn = document.getElementById('notifBtn');
    if (notifBtn) {
        notifBtn.addEventListener('click', () => {
            alert('Enterprise Notifications\n\n1. Patient J.D completed new Voice test.\n2. Server cluster 3 updated.\n3. Clinical report ready for review.');
        });
    }

    // Export Analytics Mock
    const exportBtn = document.getElementById('exportBtn');
    if (exportBtn) {
        exportBtn.addEventListener('click', () => {
            alert('Initiating massive PDF/CSV export from Enterprise database...\n[Demo: Report would download here.]');
        });
    }

    // Client-side Table Filtering
    setupTableFilters();
}

function setupTableFilters() {
    const filterBtns = document.querySelectorAll('.filter-btn');
    const tableBody = document.querySelector('tbody');

    if (!filterBtns.length || !tableBody) return;

    filterBtns.forEach(btn => {
        btn.addEventListener('click', (e) => {
            // Update Active State
            filterBtns.forEach(b => {
                b.classList.remove('bg-white', 'shadow-sm', 'border-slate-200');
                b.classList.add('bg-transparent', 'border-transparent');
            });
            e.target.classList.add('bg-white', 'shadow-sm', 'border-slate-200');
            e.target.classList.remove('bg-transparent', 'border-transparent');

            const filterType = e.target.dataset.filter;
            const rows = Array.from(tableBody.querySelectorAll('tr'));

            // Apply Filters (hide/show rows)
            rows.forEach(row => {
                // If it's a loading or empty row, skip
                if (row.cells.length === 1) return;

                let show = false;
                // Simplified text search for Risk tags
                const textContent = row.textContent.toUpperCase();

                if (filterType === 'all') {
                    show = true;
                } else if (filterType === 'high' && textContent.includes('HIGH')) {
                    show = true;
                } else if (filterType === 'med' && textContent.includes('MED')) {
                    show = true;
                } else if (filterType === 'low' && textContent.includes('LOW')) {
                    show = true;
                }

                row.style.display = show ? '' : 'none';
            });

            // Optional sorting logic for "recent" could be implemented here 
            // by actually reorganizing the DOM elements based on date text.
        });
    });
}

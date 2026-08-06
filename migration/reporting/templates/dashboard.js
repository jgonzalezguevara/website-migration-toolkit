function parseChartData(element) {
    const raw = element.dataset.values || "{}";

    try {
        return JSON.parse(raw);
    } catch (error) {
        console.error("Invalid chart data", error);
        return {};
    }
}


function renderChart(element) {
    const values = parseChartData(element);
    const entries = Object.entries(values);

    if (entries.length === 0) {
        element.innerHTML = (
            '<p class="empty-state">No data available</p>'
        );
        return;
    }

    const maximum = Math.max(
        ...entries.map(([, value]) => Number(value))
    );

    element.innerHTML = entries
        .map(([label, value]) => {
            const numericValue = Number(value);

            const percentage = maximum > 0
                ? (numericValue / maximum) * 100
                : 0;

            return `
                <div class="chart-row">
                    <span class="chart-label">${escapeHtml(label)}</span>
                    <div class="chart-track">
                        <div
                            class="chart-bar"
                            style="width: ${percentage}%"
                        ></div>
                    </div>
                    <strong class="chart-value">
                        ${numericValue}
                    </strong>
                </div>
            `;
        })
        .join("");
}


function escapeHtml(value) {
    const container = document.createElement("div");

    container.textContent = String(value);

    return container.innerHTML;
}


function configureIssueSearch() {
    const search = document.getElementById(
        "issue-search"
    );

    const table = document.getElementById(
        "issues-table"
    );

    if (!search || !table) {
        return;
    }

    const rows = Array.from(
        table.querySelectorAll("tbody tr")
    );

    search.addEventListener("input", () => {
        const query = search.value
            .trim()
            .toLowerCase();

        for (const row of rows) {
            const text = row.textContent
                .toLowerCase();

            row.hidden = (
                query !== ""
                && !text.includes(query)
            );
        }
    });
}


function initializeDashboard() {
    const charts = document.querySelectorAll(
        ".chart[data-values]"
    );

    for (const chart of charts) {
        renderChart(chart);
    }

    configureIssueSearch();
}


document.addEventListener(
    "DOMContentLoaded",
    initializeDashboard
);

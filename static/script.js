async function analyzePage(event) {
    if (event) {
        event.preventDefault();
    }

    const url = document.getElementById("url").value.trim();
    const result = document.getElementById("result");

    if (!url) {
        result.innerHTML = `
            <div class="result-card">
                <h3>⚠ Please enter a website URL</h3>
                <p>Type a full website address such as https://example.com.</p>
            </div>
        `;
        return;
    }

    result.innerHTML = `
        <div class="loading">
            <div class="spinner"></div>
            <p>Analyzing website...</p>
        </div>
    `;

    try {
        const response = await fetch("/analyze", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ url })
        });

        const data = await response.json();

        if (!response.ok || data.error) {
            result.innerHTML = `
                <div class="result-card">
                    <h3>❌ Analysis failed</h3>
                    <p>${data.error || "Unable to analyze this website."}</p>
                </div>
            `;
            return;
        }

        let statusClass = "green";
        if (data.status >= 400) {
            statusClass = "red";
        } else if (data.status >= 300) {
            statusClass = "orange";
        }

        const scoreClass = data.seo_score >= 80 ? "green" : data.seo_score >= 60 ? "orange" : "red";
        const issuesList = (data.issues || []).length
            ? data.issues.map((issue) => `<li>${issue}</li>`).join("")
            : "<li>No major issues detected.</li>";

        result.innerHTML = `
            <div class="result-card">
                <div class="score-panel">
                    <div>
                        <div class="score-value ${scoreClass}">${data.seo_score}</div>
                        <p>SEO Score</p>
                    </div>
                    <div class="progress-bar">
                        <div class="progress-fill" style="width:${data.seo_score}%"></div>
                    </div>
                </div>

                <div class="actions">
                    <button type="button" id="copyBtn">Copy Report</button>
                </div>

                <div class="result-grid">
                    <div class="card">
                        <h3>🌐 Website</h3>
                        <p>${data.title}</p>
                    </div>
                    <div class="card">
                        <h3>🟢 HTTP Status</h3>
                        <p class="${statusClass}">${data.status}</p>
                    </div>
                    <div class="card">
                        <h3>⚡ Response Time</h3>
                        <p>${data.response_time}</p>
                    </div>
                    <div class="card">
                        <h3>📝 Meta Description</h3>
                        <p>${data.meta_description}</p>
                    </div>
                    <div class="card">
                        <h3>📑 H1 Tags</h3>
                        <p>${data.h1_count}</p>
                    </div>
                    <div class="card">
                        <h3>🖼 Missing ALT Images</h3>
                        <p>${data.missing_alt_images}</p>
                    </div>
                    <div class="card">
                        <h3>📚 Word Count</h3>
                        <p>${data.word_count}</p>
                    </div>
                    <div class="card">
                        <h3>🔎 Suggested Improvements</h3>
                        <ul>${issuesList}</ul>
                    </div>
                </div>

                <div id="reportText" style="display:none;">
                    Page Pulse Report\nURL: ${url}\nSEO Score: ${data.seo_score}\nStatus: ${data.status}\nResponse Time: ${data.response_time}\nTitle: ${data.title}\nMeta Description: ${data.meta_description}\nH1 Count: ${data.h1_count}\nMissing ALT Images: ${data.missing_alt_images}\nWord Count: ${data.word_count}\nIssues: ${(data.issues || []).join(", ") || "None"}
                </div>
            </div>
        `;

        saveHistory({ url, title: data.title, score: data.seo_score });
        renderHistory();

        document.getElementById("copyBtn").addEventListener("click", copyReport);
    } catch (error) {
        result.innerHTML = `
            <div class="result-card">
                <h3>❌ Something went wrong</h3>
                <p>Please try again in a moment.</p>
            </div>
        `;
    }
}

function saveHistory(entry) {
    const history = JSON.parse(localStorage.getItem("pagePulseHistory") || "[]");
    const nextHistory = [
        { ...entry, timestamp: new Date().toLocaleString() },
        ...history.filter((item) => item.url !== entry.url)
    ].slice(0, 6);
    localStorage.setItem("pagePulseHistory", JSON.stringify(nextHistory));
}

function renderHistory() {
    const history = JSON.parse(localStorage.getItem("pagePulseHistory") || "[]");
    const historyList = document.getElementById("historyList");

    if (!history.length) {
        historyList.innerHTML = "<li>No reports yet. Analyze a website to get started.</li>";
        return;
    }

    historyList.innerHTML = history.map((item) => `
        <li><strong>${item.score}</strong> • ${item.url} • ${item.timestamp}</li>
    `).join("");
}

function copyReport() {
    const text = document.getElementById("reportText")?.innerText;
    if (!text) {
        return;
    }

    navigator.clipboard.writeText(text).then(() => {
        alert("Report copied to clipboard.");
    }).catch(() => {
        alert("Copy failed. Please select and copy the text manually.");
    });
}

document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("analyzeForm");
    if (form) {
        form.addEventListener("submit", analyzePage);
    }
    renderHistory();
});
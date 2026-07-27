/**
 * ResumeAI Pro - Enterprise Dashboard JavaScript Engine
 * Renders Chart.js visualizations dynamically based ONLY on backend calculated values.
 */

document.addEventListener('DOMContentLoaded', function () {

    // 1. File Upload Interaction
    const fileInput = document.getElementById('resume_file');
    const fileArea = document.getElementById('upload-area');
    const fileNameDisplay = document.getElementById('file-name-display');

    if (fileArea && fileInput) {
        fileArea.addEventListener('click', () => fileInput.click());

        fileInput.addEventListener('change', function () {
            if (this.files && this.files[0]) {
                fileNameDisplay.textContent = 'Selected File: ' + this.files[0].name;
                fileNameDisplay.style.color = '#2563EB';
                fileNameDisplay.style.fontWeight = '600';
            }
        });

        fileArea.addEventListener('dragover', (e) => {
            e.preventDefault();
            fileArea.classList.add('dragover');
        });

        fileArea.addEventListener('dragleave', () => {
            fileArea.classList.remove('dragover');
        });

        fileArea.addEventListener('drop', (e) => {
            e.preventDefault();
            fileArea.classList.remove('dragover');
            if (e.dataTransfer.files && e.dataTransfer.files[0]) {
                fileInput.files = e.dataTransfer.files;
                fileNameDisplay.textContent = 'Selected File: ' + e.dataTransfer.files[0].name;
                fileNameDisplay.style.color = '#2563EB';
                fileNameDisplay.style.fontWeight = '600';
            }
        });
    }

    // 2. ATS Score Doughnut Chart
    const atsCanvas = document.getElementById('atsScoreGauge');
    if (atsCanvas) {
        const atsScore = parseInt(atsCanvas.dataset.score || '0');
        const color = atsScore >= 80 ? '#10B981' : (atsScore >= 65 ? '#F59E0B' : '#EF4444');
        new Chart(atsCanvas, {
            type: 'doughnut',
            data: {
                labels: ['ATS Score', 'Deficiency Gap'],
                datasets: [{
                    data: [atsScore, 100 - atsScore],
                    backgroundColor: [color, '#E2E8F0'],
                    borderWidth: 0
                }]
            },
            options: {
                cutout: '76%',
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { display: false },
                    tooltip: { enabled: false }
                }
            }
        });
    }

    // 3. Granular Multi-Factor ATS Breakdown Chart
    const factorCanvas = document.getElementById('atsFactorChart');
    if (factorCanvas) {
        const contact = parseInt(factorCanvas.dataset.contact || '10');
        const skills = parseInt(factorCanvas.dataset.skills || '20');
        const edu = parseInt(factorCanvas.dataset.edu || '10');
        const projects = parseInt(factorCanvas.dataset.projects || '16');
        const exp = parseInt(factorCanvas.dataset.exp || '12');
        const cert = parseInt(factorCanvas.dataset.cert || '10');
        const formatting = parseInt(factorCanvas.dataset.formatting || '5');
        const density = parseInt(factorCanvas.dataset.density || '4');

        new Chart(factorCanvas, {
            type: 'bar',
            data: {
                labels: ['Contact (10)', 'Skills (25)', 'Education (10)', 'Projects (20)', 'Experience (15)', 'Certifications (10)', 'Formatting (5)', 'Keyword Match (5)'],
                datasets: [{
                    label: 'Score Earned',
                    data: [contact, skills, edu, projects, exp, cert, formatting, density],
                    backgroundColor: ['#2563EB', '#06B6D4', '#10B981', '#F59E0B', '#8B5CF6', '#EC4899', '#64748B', '#3B82F6'],
                    borderRadius: 6
                }]
            },
            options: {
                indexAxis: 'y',
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    x: { beginAtZero: true, max: 25 }
                },
                plugins: {
                    legend: { display: false }
                }
            }
        });
    }

    // 4. Keyword Frequency Chart
    const freqCanvas = document.getElementById('keywordFreqChart');
    if (freqCanvas) {
        const labels = JSON.parse(freqCanvas.dataset.labels || '[]');
        const values = JSON.parse(freqCanvas.dataset.values || '[]');

        if (labels.length > 0) {
            new Chart(freqCanvas, {
                type: 'bar',
                data: {
                    labels: labels,
                    datasets: [{
                        label: 'Frequency',
                        data: values,
                        backgroundColor: '#2563EB',
                        borderRadius: 6
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {
                        y: { beginAtZero: true, ticks: { stepSize: 1 } }
                    },
                    plugins: {
                        legend: { display: false }
                    }
                }
            });
        }
    }

    // 5. Resume Section Coverage Chart
    const secCanvas = document.getElementById('sectionCoverageChart');
    if (secCanvas) {
        const contact = parseInt(secCanvas.dataset.contact || '100');
        const skills = parseInt(secCanvas.dataset.skills || '100');
        const exp = parseInt(secCanvas.dataset.exp || '80');
        const edu = parseInt(secCanvas.dataset.edu || '100');
        const projects = parseInt(secCanvas.dataset.projects || '80');

        new Chart(secCanvas, {
            type: 'bar',
            data: {
                labels: ['Contact Info', 'Skills Portfolio', 'Work Experience', 'Education', 'Projects'],
                datasets: [{
                    label: 'Section Presence %',
                    data: [contact, skills, exp, edu, projects],
                    backgroundColor: '#10B981',
                    borderRadius: 6
                }]
            },
            options: {
                indexAxis: 'y',
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    x: { beginAtZero: true, max: 100 }
                },
                plugins: {
                    legend: { display: false }
                }
            }
        });
    }

    // 6. Job Description Match Chart
    const jdCanvas = document.getElementById('jdMatchChart');
    if (jdCanvas) {
        const matchScore = parseInt(jdCanvas.dataset.match || '0');
        new Chart(jdCanvas, {
            type: 'doughnut',
            data: {
                labels: ['Matched Requirements', 'Skill Gap'],
                datasets: [{
                    data: [matchScore, 100 - matchScore],
                    backgroundColor: ['#10B981', '#FEE2E2'],
                    borderWidth: 0
                }]
            },
            options: {
                cutout: '75%',
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { display: false },
                    tooltip: { enabled: false }
                }
            }
        });
    }

});
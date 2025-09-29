document.addEventListener('DOMContentLoaded', function () {
    // Função auxiliar para ler e parsear JSON de tags de script
    const getJsonFromScriptTag = (scriptTagId) => {
        const scriptTag = document.getElementById(scriptTagId);
        if (!scriptTag) {
            console.error(`Elemento script #${scriptTagId} não encontrado.`);
            return null;
        }
        try {
            return JSON.parse(scriptTag.textContent);
        } catch (e) {
            console.error(`Erro durante o parseamento JSON do script tag #${scriptTagId}:`, scriptTag.textContent, e);
            return null;
        }
    };

    // Objeto para rastrear gráficos renderizados
    const renderedCharts = {};

    // Função genérica para exibir mensagem de "sem dados"
    function displayNoDataMessage(chartId, message) {
        const canvas = document.getElementById(chartId);
        if (canvas) {
            const ctx = canvas.getContext('2d');
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            ctx.font = "14px Arial";
            ctx.fillStyle = "gray";
            ctx.textAlign = "center";
            ctx.fillText(message, canvas.width / 2, canvas.height / 2);
        }
        console.warn(message + " para " + chartId);
        renderedCharts[chartId] = true; // Marcar como tentado para não re-renderizar desnecessariamente
    }

    // Funções de renderização para cada gráfico
    function renderGraficoVoluntariosStatus() {
        const chartId = 'graficoVoluntariosStatus';
        if (renderedCharts[chartId] || !document.getElementById(chartId)) return;

        const labels = getJsonFromScriptTag('voluntario-status-labels-data');
        const data = getJsonFromScriptTag('voluntario-status-data-data');
        if (labels && data && Array.isArray(labels) && Array.isArray(data) && data.some(val => val > 0)) {
            const ctx = document.getElementById(chartId).getContext('2d');
            new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: labels,
                    datasets: [{
                        label: 'Número de Voluntários',
                        data: data,
                        backgroundColor: ['rgba(75, 192, 192, 0.7)', 'rgba(255, 99, 132, 0.7)'],
                        borderColor: ['rgba(75, 192, 192, 1)', 'rgba(255, 99, 132, 1)'],
                        borderWidth: 1
                    }]
                },
                options: { responsive: true, maintainAspectRatio: false, scales: { y: { beginAtZero: true, ticks: { stepSize: 1, precision: 0 } } }, plugins: { legend: { display: false } } }
            });
            renderedCharts[chartId] = true;
        } else {
            displayNoDataMessage(chartId, "Sem dados de status para voluntários.");
        }
    }

    function renderGraficoDisponibilidadeVoluntarios() {
        const chartId = 'graficoDisponibilidadeVoluntarios';
        if (renderedCharts[chartId] || !document.getElementById(chartId)) return;

        const labels = getJsonFromScriptTag('disp-labels-data');
        const datasetsRaw = getJsonFromScriptTag('disp-datasets-data');
        if (labels && datasetsRaw && Array.isArray(labels) && Array.isArray(datasetsRaw) && datasetsRaw.some(ds => ds.data && ds.data.some(val => val > 0))) {
            const turnosColors = [
                { bg: 'rgba(54, 162, 235, 0.5)', border: 'rgba(54, 162, 235, 1)' },
                { bg: 'rgba(255, 206, 86, 0.5)', border: 'rgba(255, 206, 86, 1)' },
                { bg: 'rgba(255, 99, 132, 0.5)', border: 'rgba(255, 99, 132, 1)' }
            ];
            const finalDatasets = datasetsRaw.map((dataset, index) => ({
                label: dataset.label,
                data: dataset.data,
                backgroundColor: turnosColors[index % turnosColors.length].bg,
                borderColor: turnosColors[index % turnosColors.length].border,
                borderWidth: 1
            }));
            const ctx = document.getElementById(chartId).getContext('2d');
            new Chart(ctx, {
                type: 'bar',
                data: { labels: labels, datasets: finalDatasets },
                options: { responsive: true, maintainAspectRatio: false, scales: { y: { beginAtZero: true, ticks: { stepSize: 1, precision: 0 } } }, plugins: { legend: { position: 'top' }, title: { display: true, text: 'Contagem de Voluntários Disponíveis por Dia e Turno' } } }
            });
            renderedCharts[chartId] = true;
        } else {
            displayNoDataMessage(chartId, "Sem dados de disponibilidade para voluntários.");
        }
    }

    function renderGraficoTarefasStatus() {
        const chartId = 'graficoTarefasStatus';
        if (renderedCharts[chartId] || !document.getElementById(chartId)) return;

        const labels = getJsonFromScriptTag('status-labels-data');
        const data = getJsonFromScriptTag('status-data-data');
        if (labels && data && Array.isArray(labels) && Array.isArray(data) && data.some(val => val > 0)) {
            const ctx = document.getElementById(chartId).getContext('2d');
            new Chart(ctx, {
                type: 'pie',
                data: {
                    labels: labels,
                    datasets: [{
                        label: 'Tarefas por Status',
                        data: data,
                        backgroundColor: ['rgba(255, 159, 64, 0.7)', 'rgba(54, 162, 235, 0.7)', 'rgba(75, 192, 192, 0.7)', 'rgba(153, 102, 255, 0.7)', 'rgba(255, 99, 132, 0.7)'],
                        borderColor: ['rgba(255, 159, 64, 1)', 'rgba(54, 162, 235, 1)', 'rgba(75, 192, 192, 1)', 'rgba(153, 102, 255, 1)', 'rgba(255, 99, 132, 1)'],
                        borderWidth: 1
                    }]
                },
                options: { responsive: true, maintainAspectRatio: false, plugins: { legend: { position: 'top' }, title: { display: false } } }
            });
            renderedCharts[chartId] = true;
        } else {
            displayNoDataMessage(chartId, "Sem dados de status para tarefas.");
        }
    }

    // --- Funções para Gráficos de Beneficiários ATIVOS ---
    function renderGraficoBeneficiariosGeneroAtivos() {
        const chartId = 'graficoBeneficiariosGeneroAtivos';
        if (renderedCharts[chartId] || !document.getElementById(chartId)) return;
        const labels = getJsonFromScriptTag('genero-labels-ativos-data');
        const data = getJsonFromScriptTag('genero-data-ativos-data');
        if (labels && data && Array.isArray(labels) && Array.isArray(data) && data.some(val => val > 0)) {
            const ctx = document.getElementById(chartId).getContext('2d');
            new Chart(ctx, {
                type: 'pie', data: { labels: labels, datasets: [{ label: 'Beneficiários Ativos por Gênero', data: data, backgroundColor: ['rgba(54, 162, 235, 0.7)', 'rgba(255, 99, 132, 0.7)', 'rgba(255, 206, 86, 0.7)', 'rgba(75, 192, 192, 0.7)', 'rgba(153, 102, 255, 0.7)'], borderWidth: 1 }] },
                options: { responsive: true, maintainAspectRatio: false, plugins: { legend: { position: 'top' } } }
            });
            renderedCharts[chartId] = true;
        } else { displayNoDataMessage(chartId, "Sem dados de gênero para beneficiários ativos."); }
    }

    function renderGraficoBeneficiariosEscolaridadeAtivos() {
        const chartId = 'graficoBeneficiariosEscolaridadeAtivos';
        if (renderedCharts[chartId] || !document.getElementById(chartId)) return;
        const labels = getJsonFromScriptTag('escolaridade-labels-ativos-data');
        const data = getJsonFromScriptTag('escolaridade-data-ativos-data');
        if (labels && data && Array.isArray(labels) && Array.isArray(data) && data.some(val => val > 0)) {
            const ctx = document.getElementById(chartId).getContext('2d');
            new Chart(ctx, {
                type: 'bar', data: { labels: labels, datasets: [{ label: 'Beneficiários Ativos por Escolaridade', data: data, backgroundColor: 'rgba(153, 102, 255, 0.7)', borderColor: 'rgba(153, 102, 255, 1)', borderWidth: 1 }] },
                options: { indexAxis: 'y', responsive: true, maintainAspectRatio: false, scales: { x: { beginAtZero: true, ticks: { stepSize: 1, precision: 0 } } }, plugins: { legend: { display: false } } }
            });
            renderedCharts[chartId] = true;
        } else { displayNoDataMessage(chartId, "Sem dados de escolaridade para beneficiários ativos."); }
    }
    
    function renderGraficoBeneficiariosFaixaEtariaAtivos() {
        const chartId = 'graficoBeneficiariosFaixaEtariaAtivos';
        if (renderedCharts[chartId] || !document.getElementById(chartId)) return;
        const labels = getJsonFromScriptTag('faixa-etaria-labels-ativos-data');
        const data = getJsonFromScriptTag('faixa-etaria-data-ativos-data');
        if (labels && data && Array.isArray(labels) && Array.isArray(data) && data.some(val => val > 0)) {
            const ctx = document.getElementById(chartId).getContext('2d');
            new Chart(ctx, {
                type: 'bar', data: { labels: labels, datasets: [{ label: 'Beneficiários Ativos por Faixa Etária', data: data, backgroundColor: 'rgba(75, 192, 192, 0.7)', borderColor: 'rgba(75, 192, 192, 1)', borderWidth: 1 }] },
                options: { responsive: true, maintainAspectRatio: false, scales: { y: { beginAtZero: true, ticks: { stepSize: 1, precision: 0 } } }, plugins: { legend: { display: false } } }
            });
            renderedCharts[chartId] = true;
        } else { displayNoDataMessage(chartId, "Sem dados de faixa etária para beneficiários ativos."); }
    }

    function renderGraficoBeneficiariosCidadeAtivos() {
        const chartId = 'graficoBeneficiariosCidadeAtivos';
        if (renderedCharts[chartId] || !document.getElementById(chartId)) return;
        const labels = getJsonFromScriptTag('cidade-labels-ativos-data');
        const data = getJsonFromScriptTag('cidade-data-ativos-data');
        if (labels && data && Array.isArray(labels) && Array.isArray(data) && data.some(val => val > 0)) {
            const ctx = document.getElementById(chartId).getContext('2d');
            new Chart(ctx, {
                type: 'bar', data: { labels: labels, datasets: [{ label: 'Top 10 Cidades (Beneficiários Ativos)', data: data, backgroundColor: 'rgba(255, 159, 64, 0.7)', borderColor: 'rgba(255, 159, 64, 1)', borderWidth: 1 }] },
                options: { indexAxis: 'y', responsive: true, maintainAspectRatio: false, scales: { x: { beginAtZero: true, ticks: { stepSize: 1, precision: 0 } } }, plugins: { legend: { display: false } } }
            });
            renderedCharts[chartId] = true;
        } else { displayNoDataMessage(chartId, "Sem dados de cidade para beneficiários ativos."); }
    }

    function renderGraficoBeneficiariosRendaAtivos() {
        const chartId = 'graficoBeneficiariosRendaAtivos';
        if (renderedCharts[chartId] || !document.getElementById(chartId)) return;
        const labels = getJsonFromScriptTag('renda-labels-ativos-data');
        const data = getJsonFromScriptTag('renda-data-ativos-data');
        if (labels && data && Array.isArray(labels) && Array.isArray(data) && data.some(val => val > 0)) {
            const ctx = document.getElementById(chartId).getContext('2d');
            new Chart(ctx, {
                type: 'pie', data: { labels: labels, datasets: [{ label: 'Beneficiários Ativos por Renda Familiar', data: data, backgroundColor: ['rgba(255, 99, 132, 0.7)', 'rgba(54, 162, 235, 0.7)', 'rgba(255, 206, 86, 0.7)', 'rgba(75, 192, 192, 0.7)', 'rgba(153, 102, 255, 0.7)'], borderWidth: 1 }] },
                options: { responsive: true, maintainAspectRatio: false, plugins: { legend: { position: 'top' } } }
            });
            renderedCharts[chartId] = true;
        } else { displayNoDataMessage(chartId, "Sem dados de renda para beneficiários ativos."); }
    }

    // --- Funções para Gráficos de TODOS os Beneficiários ---
    function renderGraficoBeneficiariosGeneroTodos() {
        const chartId = 'graficoBeneficiariosGeneroTodos';
        if (renderedCharts[chartId] || !document.getElementById(chartId)) return;
        const labels = getJsonFromScriptTag('genero-labels-todos-data');
        const data = getJsonFromScriptTag('genero-data-todos-data');
        if (labels && data && Array.isArray(labels) && Array.isArray(data) && data.some(val => val > 0)) {
            const ctx = document.getElementById(chartId).getContext('2d');
            new Chart(ctx, {
                type: 'pie', data: { labels: labels, datasets: [{ label: 'Todos os Beneficiários por Gênero', data: data, backgroundColor: ['rgba(54, 162, 235, 0.7)', 'rgba(255, 99, 132, 0.7)', 'rgba(255, 206, 86, 0.7)', 'rgba(75, 192, 192, 0.7)', 'rgba(153, 102, 255, 0.7)'], borderWidth: 1 }] },
                options: { responsive: true, maintainAspectRatio: false, plugins: { legend: { position: 'top' } } }
            });
            renderedCharts[chartId] = true;
        } else { displayNoDataMessage(chartId, "Sem dados de gênero para todos os beneficiários."); }
    }

    function renderGraficoBeneficiariosEscolaridadeTodos() {
        const chartId = 'graficoBeneficiariosEscolaridadeTodos';
        if (renderedCharts[chartId] || !document.getElementById(chartId)) return;
        const labels = getJsonFromScriptTag('escolaridade-labels-todos-data');
        const data = getJsonFromScriptTag('escolaridade-data-todos-data');
        if (labels && data && Array.isArray(labels) && Array.isArray(data) && data.some(val => val > 0)) {
            const ctx = document.getElementById(chartId).getContext('2d');
            new Chart(ctx, {
                type: 'bar', data: { labels: labels, datasets: [{ label: 'Todos os Beneficiários por Escolaridade', data: data, backgroundColor: 'rgba(153, 102, 255, 0.7)', borderColor: 'rgba(153, 102, 255, 1)', borderWidth: 1 }] },
                options: { indexAxis: 'y', responsive: true, maintainAspectRatio: false, scales: { x: { beginAtZero: true, ticks: { stepSize: 1, precision: 0 } } }, plugins: { legend: { display: false } } }
            });
            renderedCharts[chartId] = true;
        } else { displayNoDataMessage(chartId, "Sem dados de escolaridade para todos os beneficiários."); }
    }

    function renderGraficoBeneficiariosFaixaEtariaTodos() {
        const chartId = 'graficoBeneficiariosFaixaEtariaTodos';
        if (renderedCharts[chartId] || !document.getElementById(chartId)) return;
        const labels = getJsonFromScriptTag('faixa-etaria-labels-todos-data');
        const data = getJsonFromScriptTag('faixa-etaria-data-todos-data');
        if (labels && data && Array.isArray(labels) && Array.isArray(data) && data.some(val => val > 0)) {
            const ctx = document.getElementById(chartId).getContext('2d');
            new Chart(ctx, {
                type: 'bar', data: { labels: labels, datasets: [{ label: 'Todos os Beneficiários por Faixa Etária', data: data, backgroundColor: 'rgba(75, 192, 192, 0.7)', borderColor: 'rgba(75, 192, 192, 1)', borderWidth: 1 }] },
                options: { responsive: true, maintainAspectRatio: false, scales: { y: { beginAtZero: true, ticks: { stepSize: 1, precision: 0 } } }, plugins: { legend: { display: false } } }
            });
            renderedCharts[chartId] = true;
        } else { displayNoDataMessage(chartId, "Sem dados de faixa etária para todos os beneficiários."); }
    }

    function renderGraficoBeneficiariosCidadeTodos() {
        const chartId = 'graficoBeneficiariosCidadeTodos';
        if (renderedCharts[chartId] || !document.getElementById(chartId)) return;
        const labels = getJsonFromScriptTag('cidade-labels-todos-data');
        const data = getJsonFromScriptTag('cidade-data-todos-data');
        if (labels && data && Array.isArray(labels) && Array.isArray(data) && data.some(val => val > 0)) {
            const ctx = document.getElementById(chartId).getContext('2d');
            new Chart(ctx, {
                type: 'bar', data: { labels: labels, datasets: [{ label: 'Top 10 Cidades (Todos os Beneficiários)', data: data, backgroundColor: 'rgba(255, 159, 64, 0.7)', borderColor: 'rgba(255, 159, 64, 1)', borderWidth: 1 }] },
                options: { indexAxis: 'y', responsive: true, maintainAspectRatio: false, scales: { x: { beginAtZero: true, ticks: { stepSize: 1, precision: 0 } } }, plugins: { legend: { display: false } } }
            });
            renderedCharts[chartId] = true;
        } else { displayNoDataMessage(chartId, "Sem dados de cidade para todos os beneficiários."); }
    }

    function renderGraficoBeneficiariosRendaTodos() {
        const chartId = 'graficoBeneficiariosRendaTodos';
        if (renderedCharts[chartId] || !document.getElementById(chartId)) return;
        const labels = getJsonFromScriptTag('renda-labels-todos-data');
        const data = getJsonFromScriptTag('renda-data-todos-data');
        if (labels && data && Array.isArray(labels) && Array.isArray(data) && data.some(val => val > 0)) {
            const ctx = document.getElementById(chartId).getContext('2d');
            new Chart(ctx, {
                type: 'pie', data: { labels: labels, datasets: [{ label: 'Todos os Beneficiários por Renda Familiar', data: data, backgroundColor: ['rgba(255, 99, 132, 0.7)', 'rgba(54, 162, 235, 0.7)', 'rgba(255, 206, 86, 0.7)', 'rgba(75, 192, 192, 0.7)', 'rgba(153, 102, 255, 0.7)'], borderWidth: 1 }] },
                options: { responsive: true, maintainAspectRatio: false, plugins: { legend: { position: 'top' } } }
            });
            renderedCharts[chartId] = true;
        } else { displayNoDataMessage(chartId, "Sem dados de renda para todos os beneficiários."); }
    }

    function renderGraficoTarefasPrioridade() {
        const chartId = 'graficoTarefasPrioridade';
        if (renderedCharts[chartId] || !document.getElementById(chartId)) return;

        const labels = getJsonFromScriptTag('prioridade-labels-data');
        const data = getJsonFromScriptTag('prioridade-data-data');
        if (labels && data && Array.isArray(labels) && Array.isArray(data) && data.some(val => val > 0)) {
            const ctx = document.getElementById(chartId).getContext('2d');
            new Chart(ctx, {
                type: 'pie', // Ou 'bar' se preferir
                data: {
                    labels: labels,
                    datasets: [{
                        label: 'Tarefas Ativas por Prioridade',
                        data: data,
                        backgroundColor: [
                            'rgba(144, 238, 144, 0.7)', // Baixa - Verde claro
                            'rgb(255, 255, 0)',   // Média - Amarelo
                            'rgba(255, 165, 0, 0.7)',   // Alta - Laranja
                            'rgba(255, 0, 0, 0.7)'      // Urgente - Vermelho
                        ],
                        borderColor: [
                            'rgb(144, 238, 144)',       // Baixa
                            'rgb(255, 234, 0)',         // Média
                            'rgb(255, 165, 0)',         // Alta
                            'rgb(255, 0, 0)'            // Urgente
                        ],
                        borderWidth: 1
                    }]
                },
                options: { responsive: true, maintainAspectRatio: false, plugins: { legend: { position: 'top' } } }
            });
            renderedCharts[chartId] = true;
        } else {
            displayNoDataMessage(chartId, "Sem dados de prioridade para tarefas ativas.");
        }
    }

    function renderGraficoCertificadosPorCurso() {
        const chartId = 'graficoCertificadosPorCurso';
        if (renderedCharts[chartId] || !document.getElementById(chartId)) return;

        const labels = getJsonFromScriptTag('curso-cert-labels-data');
        const data = getJsonFromScriptTag('curso-cert-data-data');
        const noDataToDisplay = !labels || !data || !Array.isArray(labels) || !Array.isArray(data) || labels.length === 0 || data.length === 0 || data.every(val => val === 0);

        if (noDataToDisplay) {
            displayNoDataMessage(chartId, "Nenhum certificado encontrado para o período.");
        } else {
            const ctx = document.getElementById(chartId).getContext('2d');
            new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: labels,
                    datasets: [{
                        label: 'Certificados por Curso',
                        data: data,
                        backgroundColor: 'rgba(54, 162, 235, 0.7)',
                        borderColor: 'rgba(54, 162, 235, 1)',
                        borderWidth: 1
                    }]
                },
                options: { indexAxis: 'y', responsive: true, maintainAspectRatio: false, scales: { x: { beginAtZero: true, ticks: { stepSize: 1, precision: 0 } } }, plugins: { legend: { display: false } } }
            });
            renderedCharts[chartId] = true;
        }
    }

    // Determinar a aba ativa no carregamento da página e renderizar seus gráficos
    const activeTabButton = document.querySelector('#dashboardAbas .nav-link.active');
    if (activeTabButton) {
        const activeTabTarget = activeTabButton.getAttribute('data-bs-target');
        if (activeTabTarget === '#voluntarios-conteudo') {
            renderGraficoVoluntariosStatus();
            renderGraficoDisponibilidadeVoluntarios();
        } else if (activeTabTarget === '#tarefas-conteudo') {
            renderGraficoTarefasStatus();
            renderGraficoTarefasPrioridade();
        } else if (activeTabTarget === '#beneficiarios-ativos-conteudo') {
            renderGraficoBeneficiariosGeneroAtivos();
            renderGraficoBeneficiariosEscolaridadeAtivos();
            renderGraficoBeneficiariosFaixaEtariaAtivos();
            renderGraficoBeneficiariosCidadeAtivos();
            renderGraficoBeneficiariosRendaAtivos();
        } else if (activeTabTarget === '#beneficiarios-todos-conteudo') {
            renderGraficoBeneficiariosGeneroTodos();
            renderGraficoBeneficiariosEscolaridadeTodos();
            renderGraficoBeneficiariosFaixaEtariaTodos();
            renderGraficoBeneficiariosCidadeTodos();
            renderGraficoBeneficiariosRendaTodos();
        } else if (activeTabTarget === '#cursos-cert-conteudo') {
            renderGraficoCertificadosPorCurso();
        }
    } else {
        // Fallback se nenhuma aba estiver explicitamente ativa, renderiza a primeira (Voluntários)
        renderGraficoVoluntariosStatus();
        renderGraficoDisponibilidadeVoluntarios();
    }

    // Lidar com a troca de abas para renderizar outros gráficos
    const tabElements = document.querySelectorAll('#dashboardAbas .nav-link');
    tabElements.forEach(tabEl => {
        tabEl.addEventListener('shown.bs.tab', function (event) {
            const targetPaneId = event.target.getAttribute('data-bs-target');
            if (targetPaneId === '#voluntarios-conteudo') { // Adicionado para re-renderizar se necessário
                renderGraficoVoluntariosStatus();
                renderGraficoDisponibilidadeVoluntarios();
            } else if (targetPaneId === '#tarefas-conteudo') {
                renderGraficoTarefasStatus();
                renderGraficoTarefasPrioridade();
            } else if (targetPaneId === '#beneficiarios-ativos-conteudo') {
                renderGraficoBeneficiariosGeneroAtivos();
                renderGraficoBeneficiariosEscolaridadeAtivos();
                renderGraficoBeneficiariosFaixaEtariaAtivos();
                renderGraficoBeneficiariosCidadeAtivos();
                renderGraficoBeneficiariosRendaAtivos();
            } else if (targetPaneId === '#beneficiarios-todos-conteudo') {
                renderGraficoBeneficiariosGeneroTodos();
                renderGraficoBeneficiariosEscolaridadeTodos();
                renderGraficoBeneficiariosFaixaEtariaTodos();
                renderGraficoBeneficiariosCidadeTodos();
                renderGraficoBeneficiariosRendaTodos();
            } else if (targetPaneId === '#cursos-cert-conteudo') {
                renderGraficoCertificadosPorCurso();
            }
        });
    });
});

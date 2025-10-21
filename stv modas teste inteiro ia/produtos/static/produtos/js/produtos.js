// Função para adicionar nova cor via AJAX
function adicionarCor() {
    const form = document.getElementById('nova-cor-form');
    if (form) {
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const nomeCor = document.getElementById('nome-cor').value;
            
            fetch('/produtos/adicionar-cor-ajax/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
                },
                body: JSON.stringify({nome: nomeCor})
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    // Adicionar a nova cor a todos os selects de cor existentes
                    const corSelects = document.querySelectorAll('select[id$="-cor"]');
                    corSelects.forEach(select => {
                        const option = new Option(data.nome, data.id);
                        select.add(option);
                    });

                    // Fechar o modal
                    const modal = bootstrap.Modal.getInstance(document.getElementById('novaCorModal'));
                    if (modal) {
                        modal.hide();
                    }

                    // Limpar o formulário
                    document.getElementById('nova-cor-form').reset();

                    // Mostrar mensagem de sucesso
                    alert('Cor adicionada com sucesso!');
                } else {
                    alert('Erro ao adicionar cor: ' + data.error);
                }
            })
            .catch(error => {
                console.error('Erro:', error);
                alert('Erro ao adicionar cor');
            });
        });
    }
}

// Função para adicionar nova marca via AJAX
function adicionarMarca() {
    const form = document.getElementById('nova-marca-form');
    if (form) {
        form.addEventListener('submit', function(e) {
            e.preventDefault();

            const nomeMarca = document.getElementById('nome-marca').value;

            fetch('/produtos/adicionar-marca-ajax/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
                },
                body: JSON.stringify({nome: nomeMarca})
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    // Adicionar a nova marca ao select
                    const marcaSelect = document.querySelector('#id_marca');
                    if (marcaSelect) {
                        const option = new Option(data.nome, data.id);
                        marcaSelect.add(option);
                        marcaSelect.value = data.id;
                    }

                    // Fechar o modal
                    const modal = bootstrap.Modal.getInstance(document.getElementById('novaMarcaModal'));
                    if (modal) {
                        modal.hide();
                    }

                    // Limpar o formulário
                    document.getElementById('nova-marca-form').reset();

                    // Mostrar mensagem de sucesso
                    alert('Marca adicionada com sucesso!');
                } else {
                    alert('Erro ao adicionar marca: ' + data.error);
                }
            })
            .catch(error => {
                console.error('Erro:', error);
                alert('Erro ao adicionar marca');
            });
        });
    }
}

// Função para adicionar nova categoria via AJAX
function adicionarCategoria() {
    const form = document.getElementById('nova-categoria-form');
    if (form) {
        form.addEventListener('submit', function(e) {
            e.preventDefault();

            const nomeCategoria = document.getElementById('nome-categoria').value;

            fetch('/produtos/adicionar-categoria-ajax/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
                },
                body: JSON.stringify({nome: nomeCategoria})
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    // Adicionar a nova categoria ao select
                    const categoriaSelect = document.querySelector('#id_categoria');
                    if (categoriaSelect) {
                        const option = new Option(data.nome, data.id);
                        categoriaSelect.add(option);
                        categoriaSelect.value = data.id;
                    }

                    // Fechar o modal
                    const modal = bootstrap.Modal.getInstance(document.getElementById('novaCategoriaModal'));
                    if (modal) {
                        modal.hide();
                    }

                    // Limpar o formulário
                    document.getElementById('nova-categoria-form').reset();

                    // Mostrar mensagem de sucesso
                    alert('Categoria adicionada com sucesso!');
                } else {
                    alert('Erro ao adicionar categoria: ' + data.error);
                }
            })
            .catch(error => {
                console.error('Erro:', error);
                alert('Erro ao adicionar categoria');
            });
        });
    }
}

// Função para adicionar novo tamanho via AJAX
function adicionarTamanho() {
    const form = document.getElementById('novo-tamanho-form');
    if (form) {
        form.addEventListener('submit', function(e) {
            e.preventDefault();

            const nomeTamanho = document.getElementById('nome-tamanho').value;

            fetch('/produtos/adicionar-tamanho-ajax/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
                },
                body: JSON.stringify({nome: nomeTamanho})
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    // Adicionar o novo tamanho a todos os selects de tamanho existentes
                    const tamanhoSelects = document.querySelectorAll('select[id$="-tamanho"]');
                    tamanhoSelects.forEach(select => {
                        const option = new Option(data.nome, data.id);
                        select.add(option);
                    });

                    // Fechar o modal
                    const modal = bootstrap.Modal.getInstance(document.getElementById('novoTamanhoModal'));
                    if (modal) {
                        modal.hide();
                    }

                    // Limpar o formulário
                    document.getElementById('novo-tamanho-form').reset();

                    // Mostrar mensagem de sucesso
                    alert('Tamanho adicionado com sucesso!');
                } else {
                    alert('Erro ao adicionar tamanho: ' + data.error);
                }
            })
            .catch(error => {
                console.error('Erro:', error);
                alert('Erro ao adicionar tamanho');
            });
        });
    }
}

// Função para adicionar novas variações dinamicamente
function adicionarVariacao() {
    document.getElementById('add-variacao').addEventListener('click', function() {
        const formset = document.getElementById('variacoes-formset');
        const forms = formset.getElementsByClassName('variacao-form');
        const totalForms = document.getElementById('id_variacoes-TOTAL_FORMS');
        
        // Clonar o último formulário
        if (forms.length > 0) {
            const newForm = forms[forms.length - 1].cloneNode(true);
            
            // Atualizar os índices dos campos
            const formRegex = RegExp(`variacoes-(\\d){1}-`,'g');
            newForm.innerHTML = newForm.innerHTML.replace(formRegex, `variacoes-${forms.length}-`);
            
            // Limpar os valores dos campos
            const inputs = newForm.querySelectorAll('input, select, textarea');
            inputs.forEach(input => {
                if (input.type === 'checkbox' || input.type === 'radio') {
                    input.checked = false;
                } else {
                    input.value = '';
                }
            });
            
            // Adicionar o novo formulário ao formset
            formset.appendChild(newForm);
            
            // Atualizar o total de formulários
            totalForms.value = forms.length + 1;
        }
    });
}

// Função para adicionar novas imagens dinamicamente
function adicionarImagem() {
    document.getElementById('add-imagem').addEventListener('click', function() {
        const formset = document.getElementById('imagens-formset');
        const forms = formset.getElementsByClassName('imagem-form');
        const totalForms = document.getElementById('id_imagens-TOTAL_FORMS');
        
        // Clonar o último formulário
        if (forms.length > 0) {
            const newForm = forms[forms.length - 1].cloneNode(true);
            
            // Atualizar os índices dos campos
            const formRegex = RegExp(`imagens-(\\d){1}-`,'g');
            newForm.innerHTML = newForm.innerHTML.replace(formRegex, `imagens-${forms.length}-`);
            
            // Limpar os valores dos campos
            const inputs = newForm.querySelectorAll('input, select, textarea');
            inputs.forEach(input => {
                if (input.type === 'checkbox' || input.type === 'radio') {
                    input.checked = false;
                } else {
                    input.value = '';
                }
            });
            
            // Adicionar o novo formulário ao formset
            formset.appendChild(newForm);
            
            // Atualizar o total de formulários
            totalForms.value = forms.length + 1;
        }
    });
}

// Inicializar as funções quando o DOM estiver pronto
document.addEventListener('DOMContentLoaded', function() {
    adicionarCor();
    adicionarMarca();
    adicionarCategoria();
    adicionarTamanho(); // Adicionando a função para novo tamanho
    adicionarVariacao();
    adicionarImagem();
});

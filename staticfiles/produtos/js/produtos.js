// Função para adicionar nova cor via AJAX
function adicionarCor() {
    document.getElementById('nova-cor-form').addEventListener('submit', function(e) {
        e.preventDefault();
        
        const nomeCor = document.getElementById('nome-cor').value;
        
        fetch('{% url "produtos:adicionar_cor_ajax" %}', {
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
                // Adicionar a nova cor ao select
                const corSelect = document.querySelector('#id_variacoes-cor select');
                if (corSelect) {
                    const option = new Option(data.nome, data.id);
                    corSelect.add(option);
                    corSelect.value = data.id;
                }
                
                // Fechar o modal
                bootstrap.Modal.getInstance(document.getElementById('novaCorModal')).hide();
                
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

// Função para adicionar nova marca via AJAX
function adicionarMarca() {
    document.getElementById('nova-marca-form').addEventListener('submit', function(e) {
        e.preventDefault();
        
        const nomeMarca = document.getElementById('nome-marca').value;
        
        fetch('{% url "produtos:adicionar_marca_ajax" %}', {
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
                bootstrap.Modal.getInstance(document.getElementById('novaMarcaModal')).hide();
                
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
    adicionarVariacao();
    adicionarImagem();
});

(function($) {
    $(document).ready(function() {
        const itensContainer = $('#itens-group');
        const parcelasContainer = $('#parcelas-group');

        // Função para obter o valor total do pedido (do campo principal)
        const getValorTotalPedido = () => {
            const totalInputHidden = $('input[name="valor_total"]');
            return parseFloat(totalInputHidden.val() || 0) || 0;
        };

        // Função para recalcular o total dos itens e atualizar o campo principal
        const recalcularTotalItens = () => {
            let total = 0;
            itensContainer.find('.dynamic-form').each(function() {
                const row = $(this);
                const quantidadeInput = row.find('input[name$="-quantidade"]');
                const precoInput = row.find('input[name$="-preco_unitario"]');
                const deleteCheckbox = row.find('input[name$="-DELETE"]');

                if (quantidadeInput.length && precoInput.length && deleteCheckbox.length && !deleteCheckbox.prop('checked')) {
                    const quantidade = parseFloat(quantidadeInput.val()) || 0;
                    const preco = parseFloat(precoInput.val()) || 0;
                    total += quantidade * preco;
                }
            });
            const totalFieldDisplay = $('.field-valor_total .readonly');
            if (totalFieldDisplay.length) {
                totalFieldDisplay.text(total.toFixed(2));
            }
            const totalInputHidden = $('input[name="valor_total"]');
            if (totalInputHidden.length) {
                totalInputHidden.val(total.toFixed(2));
            }
        };

        // Funções para buscar dados da API
        const fetchVariacaoCompleta = async (variacaoId, variacaoInput, precoInput, quantidadeInput) => {
            if (variacaoId) {
                const response = await fetch(`/pedidos/api/get-variacao-completa/?variacao_id=${variacaoId}`);
                const data = await response.json();
                if (data.error) {
                    console.error(data.error);
                    variacaoInput.val('');
                    precoInput.val('');
                    quantidadeInput.prop('max', 0);
                    alert(data.error);
                    return;
                }
                variacaoInput.val(data.id); // Garante que o hidden input da variação tem o ID correto
                precoInput.val(data.preco);
                quantidadeInput.prop('max', data.estoque);

                let estoqueSpan = quantidadeInput.next('.estoque-display');
                if (!estoqueSpan.length) {
                    estoqueSpan = $('<span>').addClass('estoque-display').css('marginLeft', '10px');
                    quantidadeInput.after(estoqueSpan);
                }
                estoqueSpan.text(`(Estoque: ${data.estoque})`);

                validarEstoque(quantidadeInput);
                recalcularTotalItens();
            } else {
                variacaoInput.val('');
                precoInput.val('');
                quantidadeInput.prop('max', 0);
                quantidadeInput.next('.estoque-display').remove();
                recalcularTotalItens();
            }
        };

        const validarEstoque = (quantidadeInput) => {
            if (quantidadeInput.length) {
                const maxEstoque = parseInt(quantidadeInput.prop('max'));
                const quantidadeAtual = parseInt(quantidadeInput.val());
                if (quantidadeAtual > maxEstoque) {
                    alert(`A quantidade não pode ser maior que o estoque disponível (${maxEstoque}).`);
                    quantidadeInput.val(maxEstoque);
                }
                recalcularTotalItens();
            }
        };

        // Inicializa a lógica para uma linha de item de pedido
        const initializeItemRowLogic = (row) => {
            const variacaoAutocompleteHiddenInput = row.find('input[name$="-variacao_produto"]'); // Hidden input for autocomplete
            const quantidadeInput = row.find('input[name$="-quantidade"]');
            const precoInput = row.find('input[name$="-preco_unitario"]');

            if (variacaoAutocompleteHiddenInput.length) {
                // MutationObserver para detectar mudanças no valor do campo oculto do autocomplete
                const observer = new MutationObserver(() => {
                    const variacaoId = variacaoAutocompleteHiddenInput.val();
                    if (variacaoId) {
                        fetchVariacaoCompleta(variacaoId, variacaoAutocompleteHiddenInput, precoInput, quantidadeInput);
                    } else {
                        precoInput.val('');
                        quantidadeInput.val(0).prop('max', 0);
                        quantidadeInput.next('.estoque-display').remove();
                        recalcularTotalItens();
                    }
                });
                observer.observe(variacaoAutocompleteHiddenInput[0], { attributes: true, attributeFilter: ['value'] });
                
                // Trigger initial fetch if a product is already selected (e.g., on editing an existing item)
                if (variacaoAutocompleteHiddenInput.val()) {
                    observer.disconnect(); // Evita dupla execução
                    fetchVariacaoCompleta(variacaoAutocompleteHiddenInput.val(), variacaoAutocompleteHiddenInput, precoInput, quantidadeInput);
                }
            }

            if (quantidadeInput.length) {
                quantidadeInput.on('input', function() { validarEstoque($(this)); });
                quantidadeInput.on('change', recalcularTotalItens);
            }
            if (precoInput.length) {
                precoInput.on('change', recalcularTotalItens);
            }

            row.find('input[name$="-DELETE"]').on('change', recalcularTotalItens);
        };

        // Lógica para adicionar/remover linhas de formset manualmente
        const setupFormsetManagement = (container, prefix, initializeRowCallback) => {
            const totalFormsInput = $(`#id_${prefix}-TOTAL_FORMS`);
            const addRowButton = container.find('.add-row a');
            const emptyForm = container.find('.empty-form');

            // Inicializa as linhas existentes
            container.find('.dynamic-form').each(function() {
                initializeRowCallback($(this));
            });

            // Lógica para adicionar nova linha
            addRowButton.on('click', function(e) {
                e.preventDefault();
                const currentForms = parseInt(totalFormsInput.val());
                const newForm = emptyForm.clone(true); // Clone com eventos
                
                newForm.removeClass('empty-form').addClass('dynamic-form').attr('id', `${prefix}-${currentForms}`);
                newForm.html(newForm.html().replace(/__prefix__/g, currentForms));

                // Insere a nova linha antes do botão de adicionar
                newForm.insertBefore(emptyForm);
                totalFormsInput.val(currentForms + 1);

                // Inicializa a lógica para a nova linha
                initializeRowCallback(newForm);
                recalcularTotalItens(); // Recalcula o total ao adicionar item
            });

            // Lógica para remover linha (marcar DELETE)
            container.on('change', 'input[name$="-DELETE"]', function() {
                const row = $(this).closest('.dynamic-form');
                if ($(this).is(':checked')) {
                    row.hide();
                } else {
                    row.show();
                }
                recalcularTotalItens(); // Recalcula o total ao remover/restaurar item
            });
        };

        // Setup para itens
        setupFormsetManagement(itensContainer, 'itens', initializeItemRowLogic);
        
        // Lógica para Gerar Parcelas
        const gerarParcelasBtn = $('<button type="button" class="button">Gerar Parcelas</button>');
        gerarParcelasBtn.css('marginLeft', '10px');

        const numeroParcelasInput = $('<input type="number" placeholder="Nº de Parcelas" style="width: 100px; margin-left: 10px;">');
        const dataPrimeiraParcelaInput = $('<input type="date" placeholder="Primeiro Venc." style="margin-left: 10px;">');

        if (parcelasContainer.length) {
            const h2 = parcelasContainer.find('h2');
            if (h2.length) {
                h2.append(numeroParcelasInput);
                h2.append(dataPrimeiraParcelaInput);
                h2.append(gerarParcelasBtn);
            }
                $(this).find('input[name$="-DELETE"]').prop('checked', true).trigger('change');
            });

            const parcelasTotalForms = $(`#id_parcelas-TOTAL_FORMS`);
            let currentParcelaIndex = parseInt(parcelasTotalForms.val());


            if (isNaN(numParcelas) || numParcelas <= 0 || !dataPrimeiraStr || isNaN(valorTotal) || valorTotal <= 0) {
                alert('Por favor, preencha o número de parcelas, a data da primeira parcela e o valor total do pedido (que deve ser maior que zero).');
                return;
            }

            const dataPrimeira = new Date(dataPrimeiraStr + 'T00:00:00');
            const valorParcelaBase = valorTotal / numParcelas;
            
            // Limpar parcelas existentes marcando para deletar
            parcelasContainer.find('.dynamic-form').each(function() {
                $(this).find('input[name$="-DELETE"]').prop('checked', true).trigger('change');
            });

            // Adicionar novas parcelas e preencher
            const parcelasTotalForms = $(`#id_parcelas-TOTAL_FORMS`);
            let currentParcelaIndex = parseInt(parcelasTotalForms.val());

            for (let i = 0; i < numParcelas; i++) {
                const newForm = parcelasContainer.find('.empty-form').clone(true);
                
                newForm.removeClass('empty-form').addClass('dynamic-form').attr('id', `parcelas-${currentParcelaIndex}`);
                newForm.html(newForm.html().replace(/__prefix__/g, currentParcelaIndex));

                newForm.insertBefore(parcelasContainer.find('.empty-form'));

                parcelasTotalForms.val(currentParcelaIndex + 1);

                const numeroInput = newForm.find('input[name$="-numero_parcela"]');
                const valorInput = newForm.find('input[name$="-valor"]');
                const vencimentoInput = newForm.find('input[name$="-data_vencimento"]');
                
                numeroInput.val(i + 1);
                
                let valorParcela;
                if (i < numParcelas - 1) {
                    valorParcela = valorParcelaBase.toFixed(2);
                } else {
                    valorParcela = (valorTotal - (valorParcelaBase * (numParcelas - 1))).toFixed(2);
                }
                valorInput.val(valorParcela);

                const dataVencimento = new Date(dataPrimeira);
                dataVencimento.setMonth(dataVencimento.getMonth() + i);
                vencimentoInput.val(dataVencimento.toISOString().split('T')[0]);

                currentParcelaIndex++;
            }
        });
        
        // Dispara o cálculo inicial
        recalcularTotalItens();

        // Botão "Atualizar Valor Total"
        const updateValorTotalBtn = $('<button type="button" class="button">Atualizar Valor Total</button>');
        const valorTotalField = $('.field-valor_total');
        if (valorTotalField.length) {
            valorTotalField.append(updateValorTotalBtn);
            updateValorTotalBtn.on('click', recalcularTotalItens);
        }
    });
})(django.jQuery);

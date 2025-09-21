// Usamos o início do Django para garantir que o jQuery está carregado e pronto
window.addEventListener("load", function() {
    // Usamos django.jQuery em vez de $ para evitar conflitos com outras bibliotecas
    (function($) {

        // Função principal que atualiza uma linha de item de pedido
        function atualizarLinhaItemPedido(linha) {
            const produtoBaseSelect = linha.find('.item-produto-base');
            const corSelect = linha.find('.item-cor');
            const tamanhoSelect = linha.find('.item-tamanho');
            const quantidadeInput = linha.find('input[name$="-quantidade"]');
            const precoInput = linha.find('input[name$="-preco_unitario"]');
            const variacaoHiddenInput = linha.find('input[name$="-variacao_produto"]');
            
            const produtoId = produtoBaseSelect.val();

            // Limpa e desativa os selects de cor e tamanho enquanto os dados são carregados
            corSelect.empty().append('<option value="">---</option>').prop('disabled', true);
            tamanhoSelect.empty().append('<option value="">---</option>').prop('disabled', true);
            precoInput.val('');
            variacaoHiddenInput.val('');

            if (!produtoId) {
                atualizarTotalPedido();
                return;
            }

            // Faz a chamada à nossa API para buscar as variações
            $.ajax({
                url: '/produtos/api/buscar-variacoes/',
                data: { 'produto_id': produtoId },
                success: function(data) {
                    corSelect.prop('disabled', false);
                    linha.data('variacoes', data.cores); // Armazena os dados na própria linha

                    const cores = Object.values(data.cores);
                    cores.forEach(cor => {
                        corSelect.append(`<option value="${cor.nome}">${cor.nome}</option>`);
                    });

                    // Se só houver uma cor, seleciona-a automaticamente
                    if (cores.length === 1) {
                        corSelect.val(cores[0].nome).trigger('change');
                    }
                }
            });
        }

        // Função para atualizar os tamanhos baseados na cor selecionada
        function atualizarTamanhos(linha) {
            const corSelecionada = linha.find('.item-cor').val();
            const tamanhoSelect = linha.find('.item-tamanho');
            const variacoesData = linha.data('variacoes');
            
            tamanhoSelect.empty().append('<option value="">---</option>').prop('disabled', true);

            if (!corSelecionada || !variacoesData) return;

            const corData = Object.values(variacoesData).find(c => c.nome === corSelecionada);
            if (corData) {
                tamanhoSelect.prop('disabled', false);
                corData.tamanhos.forEach(tamanho => {
                    tamanhoSelect.append(`<option value="${tamanho.nome}">${tamanho.nome}</option>`);
                });

                // Se só houver um tamanho, seleciona-o automaticamente
                if (corData.tamanhos.length === 1) {
                    tamanhoSelect.val(corData.tamanhos[0].nome).trigger('change');
                }
            }
        }

        // Função para atualizar o preço e o ID da variação
        function atualizarPrecoEValidarStock(linha) {
            const corSelecionada = linha.find('.item-cor').val();
            const tamanhoSelecionado = linha.find('.item-tamanho').val();
            const precoInput = linha.find('input[name$="-preco_unitario"]');
            const quantidadeInput = linha.find('input[name$="-quantidade"]');
            const variacaoHiddenInput = linha.find('input[name$="-variacao_produto"]');
            const variacoesData = linha.data('variacoes');

            precoInput.val('');
            variacaoHiddenInput.val('');
            linha.data('stock-disponivel', 0);

            if (!corSelecionada || !tamanhoSelecionado || !variacoesData) return;

            const corData = Object.values(variacoesData).find(c => c.nome === corSelecionada);
            if (corData) {
                const tamanhoData = corData.tamanhos.find(t => t.nome === tamanhoSelecionado);
                if (tamanhoData) {
                    // Preenche o preço automaticamente
                    precoInput.val(tamanhoData.preco.toFixed(2));
                    // Guarda o stock disponível para validação
                    linha.data('stock-disponivel', tamanhoData.estoque);
                    // Preenche o campo escondido com o ID da variação, que será salvo
                    variacaoHiddenInput.val(tamanhoData.variacao_id);
                    
                    // Valida o stock atual
                    validarStock(linha);
                    // Recalcula o total do pedido
                    atualizarTotalPedido();
                }
            }
        }
        
        // Função de validação de stock
        function validarStock(linha) {
            const quantidade = parseInt(linha.find('input[name$="-quantidade"]').val()) || 0;
            const stock = linha.data('stock-disponivel') || 0;

            if (quantidade > stock) {
                alert(`Stock insuficiente! Apenas ${stock} unidades disponíveis.`);
                linha.find('input[name$="-quantidade"]').val(stock); // Corrige para o máximo
            }
            atualizarTotalPedido();
        }

        // Função para calcular o total geral do pedido
        function atualizarTotalPedido() {
            let totalPedido = 0;
            $('.dynamic-itempedido_set').each(function() {
                const linha = $(this);
                if (!linha.find('input[name$="-DELETE"]').prop('checked')) {
                    const quantidade = parseFloat(linha.find('input[name$="-quantidade"]').val()) || 0;
                    const preco = parseFloat(linha.find('input[name$="-preco_unitario"]').val()) || 0;
                    totalPedido += quantidade * preco;
                }
            });
            $('#id_valor_total').val(totalPedido.toFixed(2));
        }
        
        // --- Delegação de Eventos ---
        // Usamos delegação para que os eventos funcionem também em linhas novas
        
        // Quando um Produto Base é selecionado
        $('#itempedido_set-group').on('change', '.item-produto-base', function() {
            atualizarLinhaItemPedido($(this).closest('.dynamic-itempedido_set'));
        });

        // Quando uma Cor é selecionada
        $('#itempedido_set-group').on('change', '.item-cor', function() {
            atualizarTamanhos($(this).closest('.dynamic-itempedido_set'));
        });
        
        // Quando um Tamanho é selecionado
        $('#itempedido_set-group').on('change', '.item-tamanho', function() {
            atualizarPrecoEValidarStock($(this).closest('.dynamic-itempedido_set'));
        });
        
        // Quando a Quantidade é alterada
        $('#itempedido_set-group').on('change keyup', 'input[name$="-quantidade"]', function() {
            validarStock($(this).closest('.dynamic-itempedido_set'));
        });

    })(django.jQuery);
});
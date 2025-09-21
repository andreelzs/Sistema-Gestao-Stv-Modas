// Usamos o início do Django para garantir que o jQuery está carregado
window.addEventListener("load", function() {
    (function($) {
        // --- FUNÇÕES DE CÁLCULO ---
        function calcularTotal() {
            let total = 0;
            // Itera sobre cada linha de item do pedido
            $('#itempedido_set-group .dynamic-itempedido_set').each(function() {
                const quantidadeInput = $(this).find('input[name$="-quantidade"]');
                const precoInput = $(this).find('input[name$="-preco_unitario"]');
                
                const quantidade = parseFloat(quantidadeInput.val()) || 0;
                const preco = parseFloat(precoInput.val()) || 0;
                
                total += quantidade * preco;
            });
            
            // Atualiza o campo de valor total
            $('#id_valor_total').val(total.toFixed(2));
        }

        function gerarParcelas() {
            const valorTotal = parseFloat($('#id_valor_total').val()) || 0;
            const numParcelas = parseInt($('#id_numero_de_parcelas').val()) || 1;
            const dataPrimeiraStr = $('#id_data_primeira_parcela').val();

            if (valorTotal <= 0 || !dataPrimeiraStr) {
                alert('Por favor, defina um valor total e a data da primeira parcela.');
                return;
            }
            
            // Limpa parcelas antigas
            $('#parcela_set-group .dynamic-parcela_set').each(function() {
                $(this).find('input[name$="-DELETE"]').prop('checked', true);
                $(this).hide();
            });

            const valorParcela = (valorTotal / numParcelas).toFixed(2);
            let dataVencimento = new Date(dataPrimeiraStr + 'T00:00:00'); // Adiciona T00:00:00 para evitar problemas de fuso horário

            for (let i = 1; i <= numParcelas; i++) {
                // Adiciona uma nova linha de parcela
                $('#parcela_set-group .add-row a').click();
                
                // Preenche os campos da nova linha (a última que foi adicionada)
                const novaLinha = $('#parcela_set-group .dynamic-parcela_set').last();
                novaLinha.find('input[name$="-numero_parcela"]').val(i);
                novaLinha.find('input[name$="-valor"]').val(valorParcela);
                
                // Formata a data para YYYY-MM-DD
                const ano = dataVencimento.getFullYear();
                const mes = ('0' + (dataVencimento.getMonth() + 1)).slice(-2);
                const dia = ('0' + dataVencimento.getDate()).slice(-2);
                novaLinha.find('input[name$="-data_vencimento"]').val(`${ano}-${mes}-${dia}`);

                // Incrementa um mês para a próxima parcela
                dataVencimento.setMonth(dataVencimento.getMonth() + 1);
            }
        }

        // --- ADICIONAR BOTÕES E OUVINTES DE EVENTOS ---
        
        // Adiciona o botão de gerar parcelas
        $('#id_data_primeira_parcela').after('<button type="button" id="btn-gerar-parcelas" class="button">Gerar Parcelas</button>');
        
        // Ouve o clique no botão de gerar parcelas
        $('#btn-gerar-parcelas').on('click', gerarParcelas);

        // Ouve por mudanças nos campos de itens (quantidade e preço)
        $('#itempedido_set-group').on('change', 'input[name$="-quantidade"], input[name$="-preco_unitario"]', calcularTotal);
        
        // Calcula o total inicial ao carregar a página
        calcularTotal();

    })(django.jQuery);
});
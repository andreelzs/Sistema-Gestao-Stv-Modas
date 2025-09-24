document.addEventListener('DOMContentLoaded', function() {

    function aplicarMascara(elementId, funcaoMascara) {
        const elemento = document.getElementById(elementId);
        if (elemento) {
            elemento.addEventListener('input', function(e) {
                const valorFormatado = funcaoMascara(e.target.value);
                e.target.value = valorFormatado;
            });
        }
    }

    // Máscara para RG (formato XX.XXX.XXX-Y)
    function mascaraRG(valor) {
        let v = valor.replace(/[^0-9xX]/gi, '').toUpperCase(); 
        if (v.length > 9) v = v.slice(0, 9); 

        let resultado = "";
        for (let i = 0; i < v.length; i++) {
            resultado += v[i];
            if (i === 1 && v.length > 2) resultado += "."; 
            else if (i === 4 && v.length > 5) resultado += "."; 
            else if (i === 7 && v.length > 8) resultado += "-"; 
        }
        return resultado;
    }
    aplicarMascara('id_rg', mascaraRG);

    // Máscara para CPF (XXX.XXX.XXX-XX)
    function mascaraCPF(valor) {
        let v = valor.replace(/\D/g, ''); 
        if (v.length > 11) v = v.slice(0, 11);

        let resultado = "";
        for (let i = 0; i < v.length; i++) {
            resultado += v[i];
            if (i === 2 && v.length > 3) resultado += ".";
            else if (i === 5 && v.length > 6) resultado += ".";
            else if (i === 8 && v.length > 9) resultado += "-";
        }
        return resultado;
    }
    aplicarMascara('id_cpf', mascaraCPF);

    // Máscara para CEP (XXXXX-XXX)
    function mascaraCEP(valor) {
        let v = valor.replace(/\D/g, ''); // Remove tudo que não é dígito
        if (v.length > 8) v = v.slice(0, 8); // Limita a 8 dígitos

        let resultado = "";
        for (let i = 0; i < v.length; i++) {
            resultado += v[i];
            if (i === 4 && v.length > 5) resultado += "-";
        }
        return resultado;
    }
    aplicarMascara('id_cep', mascaraCEP);

    // Máscara para Telefone ((XX) XXXXX-XXXX ou (XX) XXXX-XXXX)
    function mascaraTelefone(valor) {
        let v = valor.replace(/\D/g, '');
        let len = v.length;

        if (len > 11) v = v.slice(0, 11);
        len = v.length;

        let resultado = "";
        if (len === 0) return ""; // Retorna vazio se não houver dígitos

        resultado = "(";
        for (let i = 0; i < len; i++) {
            resultado += v[i];
            if (i === 1 && len > 2) resultado += ") "; 
            else if (len === 11 && i === 6 && i < len -1) resultado += "-"; // Celular com 9º dígito
            else if (len === 10 && i === 5 && i < len -1) resultado += "-"; // Fixo ou celular antigo
        }
        return resultado;
    }
    
    aplicarMascara('id_telefone', mascaraTelefone); 
    aplicarMascara('id_telefone_principal', mascaraTelefone); 
    aplicarMascara('id_telefone_secundario', mascaraTelefone);

    // Função para formatar um campo específico no carregamento da página
    function formatarCampoAoCarregar(elementId, funcaoMascara) {
        const elemento = document.getElementById(elementId);
        if (elemento && elemento.value) {
            // Aplica a máscara apenas se o valor não estiver já formatado
            let precisaFormatar = true;
            if (elementId === 'id_rg' || elementId === 'id_cpf' || elementId === 'id_cep') {
                if (elemento.value.includes('.') || elemento.value.includes('-')) {
                    precisaFormatar = false;
                }
            } else if (elementId.includes('telefone')) {
                if (elemento.value.includes('(') || elemento.value.includes(')') || elemento.value.includes('-')) {
                    precisaFormatar = false;
                }
            }
            // A heurística acima é falha porque o valor que volta do backend é o limpo.
            // Então, sempre precisamos tentar formatar. A função de máscara deve ser idempotente
            // ou lidar bem com valores já parcialmente formatados (o que as atuais não fazem bem).
            // A melhor abordagem é que o backend envie o valor limpo, e o JS sempre formate.
            // As funções de máscara atuais já limpam o valor antes de formatar, então está OK.
            elemento.value = funcaoMascara(elemento.value);
        }
    }

    // Reaplicar máscaras aos valores existentes no carregamento da página
    formatarCampoAoCarregar('id_rg', mascaraRG);
    formatarCampoAoCarregar('id_cpf', mascaraCPF);
    formatarCampoAoCarregar('id_cep', mascaraCEP);
    formatarCampoAoCarregar('id_telefone', mascaraTelefone);
    formatarCampoAoCarregar('id_telefone_principal', mascaraTelefone);
    formatarCampoAoCarregar('id_telefone_secundario', mascaraTelefone);

    // Lógica para limpar máscaras antes do submit do formulário
    const todosOsFormularios = document.querySelectorAll('form');
    todosOsFormularios.forEach(function(form) {
        form.addEventListener('submit', function() {
            const campoRG = form.querySelector('#id_rg');
            if (campoRG) {
                campoRG.value = campoRG.value.replace(/[^0-9xX]/gi, '');
            }

            const campoCPF = form.querySelector('#id_cpf');
            if (campoCPF) {
                campoCPF.value = campoCPF.value.replace(/\D/g, '');
            }

            const campoCEP = form.querySelector('#id_cep');
            if (campoCEP) {
                campoCEP.value = campoCEP.value.replace(/\D/g, '');
            }

            const idsTelefone = ['id_telefone', 'id_telefone_principal', 'id_telefone_secundario'];
            idsTelefone.forEach(function(idTel) {
                const campoTel = form.querySelector(`#${idTel}`);
                if (campoTel) {
                    campoTel.value = campoTel.value.replace(/\D/g, '');
                }
            });
        });
    });
});

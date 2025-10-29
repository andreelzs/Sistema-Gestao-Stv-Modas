function setupCertificadoFormDynamicLabel(checkboxId, labelFor, initialLabelText) {
    const checkboxRecebido = document.getElementById(checkboxId);
    const labelDataEmissao = document.querySelector(`label[for="${labelFor}"]`);

    if (!checkboxRecebido || !labelDataEmissao) {
        console.warn("Elementos para label dinâmico do formulário de certificado não encontrados:", checkboxId, labelFor);
        return;
    }

    // Texto base sem "(Opcional)" e sem o asterisco
    const baseLabelText = initialLabelText.replace(" (Opcional)", "").replace(/ <span style="color:red;">\*<\/span>$/, '').trim();
    const opcionalText = " (Opcional)";
    const asteriscoHtml = ' <span style="color:red;">*</span>';

    function atualizarLabel() {
        if (checkboxRecebido.checked) {
            labelDataEmissao.innerHTML = baseLabelText + asteriscoHtml;
        } else {
            labelDataEmissao.innerHTML = baseLabelText + opcionalText;
        }
    }

    // Chama na carga da página para definir o estado inicial correto do label
    atualizarLabel();

    // Adiciona o listener para mudanças no checkbox
    checkboxRecebido.addEventListener('change', atualizarLabel);
}

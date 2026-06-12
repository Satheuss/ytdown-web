document.addEventListener('DOMContentLoaded', () => {
    const botao = document.getElementById('fb-enviar');
    const statusMsg = document.getElementById('feedback-status');
    if (!botao) return;

    botao.addEventListener('click', async () => {
        const nome = document.getElementById('fb-nome').value.trim();
        const nota = parseInt(document.getElementById('fb-nota').value, 10);
        const comentario = document.getElementById('fb-comentario').value.trim();

        if (!nome || !nota) {
            statusMsg.textContent = 'Preencha seu nome e escolha uma nota.';
            statusMsg.style.color = 'var(--crimson)';
            return;
        }

        statusMsg.textContent = 'Enviando...';
        statusMsg.style.color = 'var(--text-muted)';

        const { error } = await supabaseClient
            .from('feedbacks')
            .insert([{ nome, nota, comentario }]);

        if (error) {
            statusMsg.textContent = 'Erro ao enviar. Tente novamente.';
            statusMsg.style.color = 'var(--crimson)';
            console.error('[Feedback] Erro no insert:', error.message);
        } else {
            statusMsg.textContent = 'Obrigado pela sua avaliação! ✓';
            statusMsg.style.color = 'var(--success)';
            document.getElementById('fb-nome').value = '';
            document.getElementById('fb-nota').value = '';
            document.getElementById('fb-comentario').value = '';
            document.dispatchEvent(new CustomEvent('feedback-enviado'));
        }
    });
});

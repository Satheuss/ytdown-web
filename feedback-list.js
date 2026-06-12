// ============================================================
// Listagem de avaliações — lê feedbacks do Supabase (SELECT)
// Issue #6 — autor: Diogo
// ============================================================

async function carregarFeedbacks() {
    const lista = document.getElementById('feedback-list');
    if (!lista) return;

    const { data, error } = await supabaseClient
        .from('feedbacks')
        .select('*')
        .order('created_at', { ascending: false });

    if (error) {
        console.error('[Feedback] Erro ao ler:', error.message);
        return;
    }

    if (!data || data.length === 0) {
        lista.innerHTML = '<p style="text-align:center;color:var(--text-muted);">' +
            'Ainda não há avaliações. Seja o primeiro!</p>';
        return;
    }

    lista.innerHTML = data.map((fb) => {
        const estrelas = '★'.repeat(fb.nota) + '☆'.repeat(5 - fb.nota);
        const comentario = fb.comentario
            ? '<p style="margin:8px 0 0;color:var(--text);">' + escaparHtml(fb.comentario) + '</p>'
            : '';
        return '<div style="background:var(--bg-card);border:1px solid var(--border);' +
            'border-radius:10px;padding:16px;margin-bottom:12px;">' +
            '<div style="display:flex;justify-content:space-between;align-items:center;">' +
            '<strong style="color:var(--text);">' + escaparHtml(fb.nome) + '</strong>' +
            '<span style="color:var(--crimson);letter-spacing:2px;">' + estrelas + '</span>' +
            '</div>' + comentario + '</div>';
    }).join('');
}

// Protege contra HTML malicioso no conteúdo enviado pelo usuário
function escaparHtml(texto) {
    const div = document.createElement('div');
    div.textContent = texto;
    return div.innerHTML;
}

// Carrega ao abrir a página
document.addEventListener('DOMContentLoaded', carregarFeedbacks);

// Recarrega automaticamente quando um novo feedback é enviado (formulário do Fernando)
document.addEventListener('feedback-enviado', carregarFeedbacks);

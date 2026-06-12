// ============================================================
// Configuração do cliente Supabase — YTDown Web
// Banco de dados: PostgreSQL hospedado no Supabase (sa-east-1)
//
// A publishable key abaixo é segura para uso público no
// navegador: o acesso ao banco é controlado por Row Level
// Security (RLS), que permite apenas INSERT e SELECT na
// tabela `feedbacks`.
// ============================================================

const SUPABASE_URL = 'https://prnmbktgkqguzegcefow.supabase.co';
const SUPABASE_KEY = 'sb_publishable_9XIZn57O2AZWJuooTyA4tw_iQD0nyGW';

const supabaseClient = supabase.createClient(SUPABASE_URL, SUPABASE_KEY);

// Teste de conectividade — resultado visível no console do navegador (F12)
(async () => {
    const { error } = await supabaseClient
        .from('feedbacks')
        .select('id', { count: 'exact', head: true });

    if (error) {
        console.error('[Supabase] Falha na conexão:', error.message);
    } else {
        console.log('[Supabase] Conexão com o banco estabelecida ✓');
    }
})();

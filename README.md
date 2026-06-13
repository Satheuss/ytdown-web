# YTDown — YouTube Video Downloader

🔗 **Aplicação publicada (Deploy):** [https://satheuss.github.io/ytdown-web/](https://satheuss.github.io/ytdown-web/)

**Versão:** 1.2.0

### Equipe

- **Autor e responsável pelo projeto:** Matheus Sousa ([@Satheuss](https://github.com/Satheuss)) — criação do projeto, aplicativo, site, pipeline de CI, deploy e integração com o banco de dados.
- **Colaboradores (Etapa 3 — Bootcamp):**
  - Fernando Machado de Faria ([@iSgnik](https://github.com/iSgnik)) — formulário de avaliações dos usuários (escrita no banco).
  - Diogo Heberth de Sousa Silva — listagem de avaliações dos usuários (leitura do banco).

---

## O Problema e a Solução (Impacto Social)

**Problema:** Muitas pessoas, especialmente estudantes de áreas afastadas ou com recursos limitados, não possuem acesso constante e estável à internet. Isso dificulta o consumo de materiais educacionais, videoaulas e tutoriais disponíveis no YouTube. Como muitos não têm acesso ao download fornecido pelo YouTube Premium, acabam recorrendo a sites suspeitos, cheios de anúncios maliciosos que podem até trazer vírus ao usuário.

**Solução:** O YTDown é uma ferramenta simples, acessível e sem anúncios que permite baixar vídeos e áudios do YouTube para consumo offline. Isso democratiza o acesso à informação, permitindo que usuários montem suas bibliotecas de estudo locais sem depender de conexões instáveis.

## Estrutura do Projeto

Este repositório contém duas partes complementares:

1. **Aplicativo desktop (`app.py`)** — programa em Python com interface gráfica (Tkinter) que realiza os downloads.
2. **Site de apresentação (`index.html`, `styles.css`, `app.js`)** — landing page publicada no GitHub Pages que apresenta o projeto, disponibiliza os downloads e reúne as avaliações dos usuários.

## Funcionalidades do Aplicativo

- Interface gráfica (GUI) intuitiva e moderna.
- Download de vídeos em múltiplas qualidades (Melhor, 1080p, 720p, 480p).
- Extração direta de áudio (MP3).
- Barra de progresso e status em tempo real.
- Processamento em segundo plano para não congelar a interface.
- 💡 **Integração com API pública:** durante o download, o aplicativo consome a [Advice Slip API](https://api.adviceslip.com/) e exibe uma dica motivacional na interface, melhorando a experiência de espera do usuário.

## Funcionalidades do Site

- Apresentação do projeto e disponibilização dos downloads.
- ⭐ **Sistema de avaliações dos usuários** — visitantes podem deixar nome, nota (1 a 5) e comentário, persistidos em banco de dados na nuvem. As avaliações enviadas são exibidas na própria página, em tempo real, sem recarregamento.

## Banco de Dados em Nuvem

O sistema de avaliações é integrado ao **Supabase** (plataforma BaaS baseada em **PostgreSQL**), hospedado na nuvem (região São Paulo). A aplicação realiza operações reais de **escrita (INSERT)** e **leitura (SELECT)** sobre a tabela `feedbacks`, comunicando-se diretamente do navegador via biblioteca oficial `supabase-js`.

A segurança é garantida por **Row Level Security (RLS)**: políticas no banco permitem apenas inserção e consulta de avaliações pela chave pública (*publishable key*), bloqueando qualquer outra operação. Por isso, a chave utilizada no front-end é segura para uso público.

**Estrutura da tabela `feedbacks`:**

| Coluna | Tipo | Descrição |
|---|---|---|
| `id` | bigint | Identificador único (auto-gerado) |
| `created_at` | timestamptz | Data/hora do envio (auto) |
| `nome` | text | Nome do avaliador |
| `nota` | int (1–5) | Nota atribuída |
| `comentario` | text | Comentário (opcional) |

## Tecnologias Utilizadas

**Aplicativo:**
- Python 3.11+
- Tkinter — interface gráfica (GUI)
- yt-dlp & FFmpeg — core de download e conversão de mídia
- requests — consumo da API pública (Advice Slip)
- pytest — testes automatizados (unitários e de integração)
- flake8 — análise estática de código (linting)
- GitHub Actions — pipeline de Integração Contínua (CI)

**Site:**
- HTML5 semântico, CSS3 moderno (variáveis, grid, flexbox), JavaScript vanilla
- **Supabase (PostgreSQL)** — banco de dados em nuvem para o sistema de avaliações
- Design responsivo
- GitHub Pages — hospedagem (deploy)

## Estrutura de Colaboração (Etapa 3 — Bootcamp)

Nesta etapa, o trabalho foi desenvolvido em equipe utilizando o fluxo de **Pull Requests com revisão de código (Code Review)**. Cada integrante abriu ao menos um PR a partir de uma *branch* própria, que foi revisado e aprovado por **outro** membro antes do merge na `main`. A branch `main` é protegida, exigindo aprovação e aprovação do pipeline de CI antes de qualquer integração.

| PR | Contribuição | Autor | Revisado por |
|---|---|---|---|
| #7 | Integração com o banco Supabase | Matheus | Fernando |
| #8 | Formulário de avaliações (escrita) | Fernando | Matheus |
| #9 | Listagem de avaliações (leitura) | Diogo | Matheus |

## Como Instalar e Executar

1. Clone este repositório:

```bash
git clone https://github.com/Satheuss/ytdown-web.git
cd ytdown-web
```

2. Instale as dependências:

```bash
pip install -r requirements.txt
```

3. Execute o aplicativo:

```bash
python app.py
```

Alternativamente, baixe o executável para Windows na [página de Releases](https://github.com/Satheuss/ytdown-web/releases/latest) ou pelo botão de download do [site publicado](https://satheuss.github.io/ytdown-web/).

### Executando o site localmente

O site é estático. Basta abrir o arquivo `index.html` em um navegador, ou servir a pasta com um servidor local:

```bash
python -m http.server 8000
```

Em seguida, acesse `http://localhost:8000`. O sistema de avaliações já se conecta ao banco em nuvem, sem configuração adicional.

## Testes Automatizados

O projeto possui testes unitários (validação de URLs do YouTube, isolados em `core.py`) e um **teste de integração** que valida a comunicação com a API pública Advice Slip. Para executá-los:

```bash
pip install pytest
pytest test_app.py -v
```

## Integração Contínua (CI)

A cada push ou pull request, o pipeline do GitHub Actions (`.github/workflows/ci.yml`) executa automaticamente:

1. Análise estática com flake8 (linting);
2. Testes automatizados com pytest, incluindo o teste de integração com a API.

A branch `main` é protegida: PRs só podem ser integrados após aprovação em revisão e com o pipeline de CI aprovado (*verde*).

## Licença

MIT License — código aberto para uso educacional.

---

**Aviso legal:** ferramenta destinada ao download de conteúdo próprio ou livre de direitos autorais, para fins educacionais. Respeite os Termos de Serviço do YouTube.

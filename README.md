# YTDown — YouTube Video Downloader

🔗 **Aplicação publicada (Deploy):** [https://satheuss.github.io/ytdown-web/](https://satheuss.github.io/ytdown-web/)

**Versão:** 1.1.0
**Autor:** Matheus Sousa ([@Satheuss](https://github.com/Satheuss))

---

## O Problema e a Solução (Impacto Social)

**Problema:** Muitas pessoas, especialmente estudantes de áreas afastadas ou com recursos limitados, não possuem acesso constante e estável à internet. Isso dificulta o consumo de materiais educacionais, videoaulas e tutoriais disponíveis no YouTube. Como muitos não têm acesso ao download fornecido pelo YouTube Premium, acabam recorrendo a sites suspeitos, cheios de anúncios maliciosos que podem até trazer vírus ao usuário.

**Solução:** O YTDown é uma ferramenta simples, acessível e sem anúncios que permite baixar vídeos e áudios do YouTube para consumo offline. Isso democratiza o acesso à informação, permitindo que usuários montem suas bibliotecas de estudo locais sem depender de conexões instáveis.

## Estrutura do Projeto

Este repositório contém duas partes complementares:

1. **Aplicativo desktop (`app.py`)** — programa em Python com interface gráfica (Tkinter) que realiza os downloads.
2. **Site de apresentação (`index.html`, `styles.css`, `app.js`)** — landing page publicada no GitHub Pages que apresenta o projeto e disponibiliza os downloads.

## Funcionalidades do Aplicativo

- Interface gráfica (GUI) intuitiva e moderna.
- Download de vídeos em múltiplas qualidades (Melhor, 1080p, 720p, 480p).
- Extração direta de áudio (MP3).
- Barra de progresso e status em tempo real.
- Processamento em segundo plano para não congelar a interface.
- 💡 **Integração com API pública:** durante o download, o aplicativo consome a [Advice Slip API](https://api.adviceslip.com/) e exibe uma dica motivacional na interface, melhorando a experiência de espera do usuário.

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
- Design responsivo
- GitHub Pages — hospedagem (deploy)

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

## Testes Automatizados

O projeto possui testes unitários (validação de URLs do YouTube) e um **teste de integração** que valida a comunicação com a API pública Advice Slip. Para executá-los:

```bash
pip install pytest
pytest test_app.py -v
```

## Integração Contínua (CI)

A cada push ou pull request, o pipeline do GitHub Actions (`.github/workflows/ci.yml`) executa automaticamente:

1. Análise estática com flake8 (linting);
2. Testes automatizados com pytest, incluindo o teste de integração com a API.

## Licença

MIT License — código aberto para uso educacional.

---

**Aviso legal:** ferramenta destinada ao download de conteúdo próprio ou livre de direitos autorais, para fins educacionais. Respeite os Termos de Serviço do YouTube.

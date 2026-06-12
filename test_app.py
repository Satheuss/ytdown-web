# pip install pytest
import pytest
from core import is_valid_youtube_url

# Teste 1


def test_url_youtube_valida():
    url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    assert is_valid_youtube_url(url) == True

# Teste 2


def test_url_invalida_rejeitada():
    url = "https://www.google.com"
    assert is_valid_youtube_url(url) == False

# Teste 3


def test_url_shorts_valida():
    url = "https://www.youtube.com/shorts/abcdefghijk"
    assert is_valid_youtube_url(url) == True

# Novo Teste


def test_integracao_api_frases():
    import requests
    url_api = "https://api.adviceslip.com/advice"
    try:
        resposta = requests.get(url_api, timeout=5)
        assert resposta.status_code == 200
        dados = resposta.json()
        assert "slip" in dados
    except requests.exceptions.RequestException:
        assert False, "A API externa não pôde ser alcançada."

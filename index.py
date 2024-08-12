import os
import string
import nltk
import unicodedata
from nltk.corpus import stopwords
from nltk.probability import FreqDist
from wordcloud import WordCloud
from pypdf import PdfReader

# Construindo o caminho absoluto para o arquivo PDF
pdf_path = os.path.join(os.path.dirname(__file__), 'CURRICULO_CIÊNCIA_DA_INFORMAÇÃO_20161.pdf')

# criando um objeto PdfReader
reader = PdfReader(pdf_path)

# Extraindo todas as páginas do texto
textoInteiro = ''
for page in reader.pages :
    text = page.extract_text()
    textoInteiro += f'\n{text}'

textoInteiro = textoInteiro.lower()

# LIMPAR TEXTO RETIRANDO PONTUAÇÃO
textLimpeza = ''.join([p for p in textoInteiro if p not in string.punctuation])
# print(textLimpeza)

# LIMPAR TEXTO RETIRANDO números
textnumeros = ''.join([char for char in textLimpeza if not char.isdigit()])
# print(textnumeros)

# Remover acentos da string textoInteiro
def remover_acentos(texto):
    # Normaliza a string para decompôr caracteres acentuados em caracteres base e os acentos
    texto_normalizado = unicodedata.normalize('NFKD', texto) # Ex: 'á' para '´a'
    # Remove os acentos filtrando apenas os caracteres que não são marcas de combinação
    return ''.join([c for c in texto_normalizado if not unicodedata.combining(c)])

textoInteiroSemAcentos = remover_acentos(textnumeros)

# TOKENIZAÇÃO
nltk.download('punkt')
tokenPalavras = nltk.word_tokenize(textoInteiroSemAcentos)
# print(tokenPalavras)

# REMOÇÃO DE STOPWORDS
nltk.download('stopwords')
stopWords = stopwords.words('portuguese')

palavraSemStopWords = [p for p in tokenPalavras if p not in stopWords]
# print(stopWords)

# VERIFICANDO AS PALAVRAS COM MAIOR FREQUENCIA
freq = FreqDist(palavraSemStopWords)
freq = freq.most_common(10)
print(freq)

# GERANDO A NUVEM DE PALAVRAS
nuvemDePalavras = WordCloud(background_color = 'black', stopwords = stopWords, height = 1080, width = 1080, max_words = 100)
nuvemDePalavras.generate(' '.join(palavraSemStopWords))
nuvemDePalavras.to_file('nome-da-nuvem.png')
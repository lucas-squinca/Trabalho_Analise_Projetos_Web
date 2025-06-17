# Usa uma imagem Python oficial como base. A versão slim é menor.
FROM python:3.9-slim

# Define o diretório de trabalho dentro do container.
# Todos os comandos subsequentes serão executados a partir deste diretório.
WORKDIR /app

# Copia o arquivo de dependências para o diretório de trabalho.
# Isso é feito primeiro para aproveitar o cache de camadas do Docker.
# Se o requirements.txt não mudar, o Docker não reinstalará as dependências.
COPY requirements.txt .

# Instala as dependências listadas no requirements.txt.
# --no-cache-dir desabilita o cache do pip, reduzindo o tamanho da imagem.
RUN pip install --no-cache-dir -r requirements.txt

# Copia todo o conteúdo da pasta local `backend` para o diretório de trabalho `/app` no container.
COPY . .

# Expõe a porta 5000, que é a porta que a aplicação Flask usará dentro do container.
EXPOSE 5000

# O comando que será executado quando o container for iniciado.
# Inicia a aplicação Flask.
CMD ["python", "app.py"]

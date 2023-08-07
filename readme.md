Aplicativo Flask e Flask-RESTful
Este é um guia simples sobre como executar o aplicativo Flask e Flask-RESTful localmente em sua máquina.

Pré-requisitos
Certifique-se de ter o Python e o pip (gerenciador de pacotes Python) instalados em sua máquina.

Passos para Executar
Clone o repositório:

bash
Copy code
git clone https://github.com/leofnh/testeflask.git
Navegue até o diretório do aplicativo:

bash
Copy code
cd seu-app-flask
Crie e ative um ambiente virtual (opcional, mas recomendado):

No Windows:

bash
Copy code
python -m venv venv
venv\Scripts\activate
No macOS e Linux:

bash
Copy code
python3 -m venv venv
source venv/bin/activate
Instale as dependências:

bash
Copy code
pip install -r requirements.txt
Inicie o servidor:

bash
Copy code
python app.py
Acesse a API em seu navegador ou use ferramentas como cURL ou Postman:

Abra o navegador e vá para http://localhost:5000

Como Parar o Servidor
Para parar o servidor, pressione Ctrl + C no terminal onde o servidor está sendo executado. Certifique-se de desativar o ambiente virtual (se estiver usando) quando terminar:

bash
Copy code
deactivate
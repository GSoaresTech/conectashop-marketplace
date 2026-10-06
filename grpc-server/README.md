 ConectaShop — Servidor gRPC.

 Implementação do servidor gRPC da dinâmica IntegraLab — Interoperabilidade REST e gRPC orientada por contratos, para o cenário ConectaShop.



 1. Responsabilidade.


 
Este projeto implementa o serviço gRPC ShippingService, definido no contrato proto/shipping.proto, com os métodos:

- Health
- CalculateShipping

O servidor deve seguir exatamente o contrato fornecido pela atividade.



 2.  Pre-requisitos & Tecnologias.



- Python Python 3.13+ instalado e disponível no PATH.
- Windows ou outro sistema compatível com Python/gRPC.
- gRPC Python (grpcio)
- grpcio-tools para geração dos arquivos Python a partir do .proto
- Protocol Buffers (proto3)



 3. Criar e ativar o ambiente virtual.



 No Windows:

- Abrir o CMD na pasta do raiz servidor gRPC.
- Criar o ambiente virtual usando o comando "python -m venv .venv".
- Ativar o ambiente virtual ".venv\Scripts\activate".



4. Instalar as dependências.



- pip install -r requirements.txt



5. Gerar os arquivos Python do contrato



Com shipping.proto dentro de proto/, executar na pasta raiz do projeto:

python -m grpc_tools.protoc -I./proto --python_out=. --grpc_python_out=. ./proto/shipping.proto

Isso gera:

shipping_pb2.py
shipping_pb2_grpc.py

Esses arquivos são gerados automaticamente e não devem ser editados manualmente.



6. Configuração do servidor



O servidor usa as seguintes configurações padrão:

SERVER_TEAM=S01
GRPC_PORT=50051

"O código da equipe "S01" é provisório e deve ser substituído pelo código real da equipe quando definido".

O servidor faz bind em:

0.0.0.0:50051

Para integração, o destino informado aos clientes será no formato:

<IP-DO-SERVIDOR>:50051


Durante os testes realizados neste computador, o endereço de rede utilizado foi:

192.168.1.5:50051

"O endereço IP pode mudar conforme a rede utilizada. Confirmar o IP antes da integração".



7. Iniciar o servidor



Com o ambiente virtual ativado:

python server-gRPC.py

"O servidor permanece executando e aguardando chamadas gRPC".



8. Executar os testes locais



Com o servidor em execução, abrir outro terminal na pasta raiz do servidor, ativar o ambiente virtual e executar:

"python testes_grpc.py"



9. Logs



As chamadas recebidas pelo servidor são gravadas na pasta:

logs/server.log

"Os registros incluem informações como protocolo, servidor, cliente, Request ID, operação, parâmetros principais e resultado".








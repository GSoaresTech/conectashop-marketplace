import logging
import math
import os
import threading
from concurrent import futures

import grpc

import shipping_pb2
import shipping_pb2_grpc


# ============================================================
# Configuracoes do servidor
# ============================================================

# Codigo da equipe Servidor.
# Podemos alterar o codigo da equipe S01, para o codigo real da nossa equipe.

SERVER_TEAM = os.getenv("SERVER_TEAM", "S01")

# Porta do servidor gRPC.
# A porta 50051 e a porta sugerida pelo contrato.

PORT = int(os.getenv("GRPC_PORT", "50051"))


# ============================================================
# Configuracao dos logs
# ============================================================

# Cria a pasta de logs automaticamente, caso ela ainda nao exista.

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_DIR = os.path.join(BASE_DIR, "logs")
LOG_FILE = os.path.join(LOG_DIR, "server.log")
os.makedirs(LOG_DIR, exist_ok=True)

# Os logs tecnicos das chamadas ficam somente no arquivo.

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE, encoding="utf-8")
    ]
)


# ============================================================
# Interface do terminal
# ============================================================

# Garante que mensagens de clientes simultaneos nao se misturem.

console_lock = threading.Lock()


def console_status(status, message):
    """Exibe um status amigavel no terminal."""
    with console_lock:
        print(f"[{status}] {message}", flush=True)


class ShippingService(shipping_pb2_grpc.ShippingServiceServicer):
    """Implementacao do ShippingService definido no shipping.proto."""

    def _get_client_team(self, context):
        """Obtem o x-client-team enviado pelo cliente."""

        for key, value in context.invocation_metadata():
            if key.lower() == "x-client-team":
                return value

        # Metadata obrigatorio ausente.

        console_status(
            "FALHA",
            "Requisicao rejeitada: MISSING_CLIENT_TEAM"
        )

        logging.warning(
            "protocol=GRPC server=%s client=- requestId=- "
            "operation=UNKNOWN status=ERROR error=MISSING_CLIENT_TEAM",
            SERVER_TEAM
        )

        context.abort(
            grpc.StatusCode.INVALID_ARGUMENT,
            "MISSING_CLIENT_TEAM"
        )

    def Health(self, request, context):
        """Verifica se o servidor esta disponivel."""

        client_team = self._get_client_team(context)

        console_status(
            "RECEBENDO",
            f"Cliente: {client_team} | Operacao: Health"
        )
        console_status(
            "PROCESSANDO",
            "Verificando disponibilidade do servidor"
        )

        logging.info(
            "protocol=GRPC server=%s client=%s requestId=- "
            "operation=Health status=OK",
            SERVER_TEAM,
            client_team
        )

        response = shipping_pb2.HealthResponse(
            status="SERVING",
            server_team=SERVER_TEAM
        )

        console_status(
            "CONCLUIDA",
            f"Health respondido | server_team={SERVER_TEAM}"
        )
        console_status(
            "AGUARDANDO",
            "Aguardando nova requisicao..."
        )

        return response

    def CalculateShipping(self, request, context):
        """Calcula o preco e o prazo estimado do frete."""

        client_team = self._get_client_team(context)

        console_status(
            "RECEBENDO",
            f"Cliente: {client_team} | Operacao: CalculateShipping"
        )
        console_status(
            "PROCESSANDO",
            f"Request ID: {request.request_id or '(vazio)'}"
        )

        # ========================================================
        # Validacoes obrigatorias do contrato
        # ========================================================

        # request_id e obrigatorio e nao pode ser vazio.

        if not request.request_id:
            logging.warning(
                "protocol=GRPC server=%s client=%s requestId=- "
                "operation=CalculateShipping status=ERROR "
                "error=MISSING_REQUEST_ID",
                SERVER_TEAM,
                client_team
            )

            console_status(
                "FALHA",
                "MISSING_REQUEST_ID"
            )
            console_status(
                "AGUARDANDO",
                "Aguardando nova requisicao..."
            )

            context.abort(
                grpc.StatusCode.INVALID_ARGUMENT,
                "MISSING_REQUEST_ID"
            )

        # O peso deve estar entre 1 e 30000 gramas.

        if request.weight_grams < 1 or request.weight_grams > 30000:
            logging.warning(
                "protocol=GRPC server=%s client=%s requestId=%s "
                "operation=CalculateShipping status=ERROR "
                "error=INVALID_WEIGHT",
                SERVER_TEAM,
                client_team,
                request.request_id
            )

            console_status(
                "FALHA",
                f"Request ID: {request.request_id} | INVALID_WEIGHT"
            )
            console_status(
                "AGUARDANDO",
                "Aguardando nova requisicao..."
            )

            context.abort(
                grpc.StatusCode.INVALID_ARGUMENT,
                "INVALID_WEIGHT"
            )

        # A zona nao pode ser UNSPECIFIED.
        if request.zone == shipping_pb2.SHIPPING_ZONE_UNSPECIFIED:
            logging.warning(
                "protocol=GRPC server=%s client=%s requestId=%s "
                "operation=CalculateShipping status=ERROR "
                "error=INVALID_ZONE",
                SERVER_TEAM,
                client_team,
                request.request_id
            )

            console_status(
                "FALHA",
                f"Request ID: {request.request_id} | INVALID_ZONE"
            )
            console_status(
                "AGUARDANDO",
                "Aguardando nova requisicao..."
            )

            context.abort(
                grpc.StatusCode.INVALID_ARGUMENT,
                "INVALID_ZONE"
            )

        # O modo nao pode ser UNSPECIFIED.
        if request.mode == shipping_pb2.SHIPPING_MODE_UNSPECIFIED:
            logging.warning(
                "protocol=GRPC server=%s client=%s requestId=%s "
                "operation=CalculateShipping status=ERROR "
                "error=INVALID_MODE",
                SERVER_TEAM,
                client_team,
                request.request_id
            )

            console_status(
                "FALHA",
                f"Request ID: {request.request_id} | INVALID_MODE"
            )
            console_status(
                "AGUARDANDO",
                "Aguardando nova requisicao..."
            )

            context.abort(
                grpc.StatusCode.INVALID_ARGUMENT,
                "INVALID_MODE"
            )

        # ========================================================
        # Calculo do frete
        # ========================================================
        try:
            # Tarifas base em centavos.
            base_prices = {
                shipping_pb2.LOCAL: {
                    shipping_pb2.STANDARD: 1000,
                    shipping_pb2.EXPRESS: 1600,
                },
                shipping_pb2.REGIONAL: {
                    shipping_pb2.STANDARD: 1800,
                    shipping_pb2.EXPRESS: 2800,
                },
                shipping_pb2.NATIONAL: {
                    shipping_pb2.STANDARD: 3000,
                    shipping_pb2.EXPRESS: 4500,
                },
            }

            # Adicional por quilograma iniciado, em centavos.

            additional_per_kg = {
                shipping_pb2.STANDARD: 400,
                shipping_pb2.EXPRESS: 600,
            }

            # Prazo estimado em dias.

            estimated_days = {
                shipping_pb2.LOCAL: {
                    shipping_pb2.STANDARD: 2,
                    shipping_pb2.EXPRESS: 1,
                },
                shipping_pb2.REGIONAL: {
                    shipping_pb2.STANDARD: 4,
                    shipping_pb2.EXPRESS: 2,
                },
                shipping_pb2.NATIONAL: {
                    shipping_pb2.STANDARD: 7,
                    shipping_pb2.EXPRESS: 3,
                },
            }

            # Quilograma iniciado = teto(weight_grams / 1000).

            kilograms_charged = math.ceil(request.weight_grams / 1000)

            base_price = base_prices[request.zone][request.mode]
            additional = kilograms_charged * additional_per_kg[request.mode]
            price_cents = base_price + additional
            days = estimated_days[request.zone][request.mode]

            logging.info(
                "protocol=GRPC server=%s client=%s requestId=%s "
                "operation=CalculateShipping weight=%d zone=%s mode=%s "
                "status=OK priceCents=%d estimatedDays=%d",
                SERVER_TEAM,
                client_team,
                request.request_id,
                request.weight_grams,
                shipping_pb2.ShippingZone.Name(request.zone),
                shipping_pb2.ShippingMode.Name(request.mode),
                price_cents,
                days
            )

            response = shipping_pb2.ShippingResponse(
                request_id=request.request_id,
                price_cents=price_cents,
                estimated_days=days,
                server_team=SERVER_TEAM
            )

            console_status(
                "CONCLUIDA",
                f"Request ID: {request.request_id} | "
                f"Frete: {price_cents} centavos | Prazo: {days} dias"
            )
            console_status(
                "AGUARDANDO",
                "Aguardando nova requisicao..."
            )

            return response

        except grpc.RpcError:
            
            # Mantem intactos os erros gRPC ja tratados explicitamente.
            raise

        except Exception:

            # Qualquer falha inesperada deve virar INTERNAL/INTERNAL_ERROR.

            logging.exception(
                "protocol=GRPC server=%s client=%s requestId=%s "
                "operation=CalculateShipping status=ERROR "
                "error=INTERNAL_ERROR",
                SERVER_TEAM,
                client_team,
                request.request_id
            )

            console_status(
                "FALHA",
                f"Request ID: {request.request_id} | INTERNAL_ERROR"
            )
            console_status(
                "AGUARDANDO",
                "Aguardando nova requisicao..."
            )

            context.abort(
                grpc.StatusCode.INTERNAL,
                "INTERNAL_ERROR"
            )


def serve():
    """Cria e inicia o servidor gRPC."""

    server = grpc.server(
        futures.ThreadPoolExecutor(max_workers=10)
    )

    shipping_pb2_grpc.add_ShippingServiceServicer_to_server(
        ShippingService(),
        server
    )

    # 0.0.0.0 permite aceitar conexoes externas a maquina.

    address = f"0.0.0.0:{PORT}"
    server.add_insecure_port(address)
    server.start()

    # Painel visual de inicializacao.

    print()
    print("+----------------------------------------------------+")
    print("|              CONECTASHOP - gRPC SERVER             |")
    print("+----------------------------------------------------+")
    print(f"| Equipe : {SERVER_TEAM:<42}|")
    print(f"| Host   : {'0.0.0.0':<42}|")
    print(f"| Porta  : {PORT:<42}|")
    print("+----------------------------------------------------+")
    print()

    console_status(
        "ONLINE",
        f"Servidor iniciado em 0.0.0.0:{PORT} | server_team={SERVER_TEAM}"
    )
    console_status(
        "AGUARDANDO",
        "Aguardando requisicoes..."
    )

    # A inicializacao tambem fica registrada no arquivo de log.

    logging.info(
        "gRPC server iniciado em %s | server_team=%s",
        address,
        SERVER_TEAM
    )

    try:
        server.wait_for_termination()
    except KeyboardInterrupt:
        console_status("OFFLINE", "Servidor encerrado pelo usuario.")
        logging.info("Servidor encerrado.")
        server.stop(0)


if __name__ == "__main__":
    serve()

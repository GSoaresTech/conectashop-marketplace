import os

import grpc

import shipping_pb2
import shipping_pb2_grpc


# Para testar outra maquina: GRPC_TARGET=172.16.17.59:50051 python testes_grpc.py
ENDERECO = os.getenv("GRPC_TARGET", "localhost:50051")


def testar_health():
    canal = grpc.insecure_channel(ENDERECO)
    cliente = shipping_pb2_grpc.ShippingServiceStub(canal)

    resposta = cliente.Health(
        shipping_pb2.HealthRequest(),
        metadata=[
            ("x-client-team", "C01")
        ]
    )

    print("=== G1 - HEALTH ===")
    print("status:", resposta.status)
    print("server_team:", resposta.server_team)


def testar_g2():
    canal = grpc.insecure_channel(ENDERECO)
    cliente = shipping_pb2_grpc.ShippingServiceStub(canal)

    resposta = cliente.CalculateShipping(
        shipping_pb2.ShippingRequest(
            request_id="g2-001",
            weight_grams=1500,
            zone=shipping_pb2.LOCAL,
            mode=shipping_pb2.STANDARD
        ),
        metadata=[
            ("x-client-team", "C01")
        ]
    )

    print("=== G2 - CALCULATE SHIPPING ===")
    print("request_id:", resposta.request_id)
    print("price_cents:", resposta.price_cents)
    print("estimated_days:", resposta.estimated_days)
    print("server_team:", resposta.server_team)



def testar_g3():
    canal = grpc.insecure_channel(ENDERECO)
    cliente = shipping_pb2_grpc.ShippingServiceStub(canal)

    resposta = cliente.CalculateShipping(
        shipping_pb2.ShippingRequest(
            request_id="g3-001",
            weight_grams=2500,
            zone=shipping_pb2.REGIONAL,
            mode=shipping_pb2.EXPRESS
        ),
        metadata=[
            ("x-client-team", "C01")
        ]
    )

    print("=== G3 - CALCULATE SHIPPING ===")
    print("request_id:", resposta.request_id)
    print("price_cents:", resposta.price_cents)
    print("estimated_days:", resposta.estimated_days)
    print("server_team:", resposta.server_team)



def testar_g4():
    canal = grpc.insecure_channel(ENDERECO)
    cliente = shipping_pb2_grpc.ShippingServiceStub(canal)

    resposta = cliente.CalculateShipping(
        shipping_pb2.ShippingRequest(
            request_id="g4-001",
            weight_grams=1000,
            zone=shipping_pb2.NATIONAL,
            mode=shipping_pb2.STANDARD
        ),
        metadata=[
            ("x-client-team", "C01")
        ]
    )

    print("=== G4 - CALCULATE SHIPPING ===")
    print("request_id:", resposta.request_id)
    print("price_cents:", resposta.price_cents)
    print("estimated_days:", resposta.estimated_days)
    print("server_team:", resposta.server_team)


def testar_g5():
    canal = grpc.insecure_channel(ENDERECO)
    cliente = shipping_pb2_grpc.ShippingServiceStub(canal)

    try:
        cliente.CalculateShipping(
            shipping_pb2.ShippingRequest(
                request_id="g5-001",
                weight_grams=0,
                zone=shipping_pb2.LOCAL,
                mode=shipping_pb2.STANDARD
            ),
            metadata=[
                ("x-client-team", "C01")
            ]
        )

        print("=== G5 - ERRO ===")
        print("ERRO: o servidor aceitou um peso inválido")

    except grpc.RpcError as erro:
        print("=== G5 - INVALID WEIGHT ===")
        print("status:", erro.code())
        print("details:", erro.details())


if __name__ == "__main__":
    testar_health()
    testar_g2()
    testar_g3()
    testar_g4()
    testar_g5()
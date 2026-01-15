# Pomodoro

import subprocess
import os
import platform
import time
from datetime import datetime, timedelta

horarioAtual = datetime.now();

tempoDeWorkflow: str = "01:00:00"  # input("Tempo de trabalho: ")

def handlerTimeInput(input : str):
    try:
        #validar se está no FORMATO certo = 00:00:00 caso não => Error

        #validar se o horario está dentro da realidade caso não => Error



        result: int = int(input)





        return timedelta(minutes=result)
    except ValueError:
        print(f"Erro: O valor digitado não é um número válido.")



    return


so = platform.system()


def limparConsole() -> None:
    if so == "Windows":
        os.system("cls")
    else:
        os.system("clear")


def converterStrToDateTime(inputString: str) -> timedelta:
    """
    Retorna o tempo de trabalho em minutos.

    :param inputString: o tempo de trabalhado em minutos.
    :return: Uma datetime em minutos.
    """
    try:
        result: int = int(inputString)

        return timedelta(minutes=result)
    except ValueError:
        print(f"Erro: O valor digitado não é um número válido.")


horarioDePausa: datetime = horarioAtual + converterStrToDateTime(tempoDeWorkflow)

tempoDeDescanso: int = 5

while (horarioAtual <= horarioDePausa):
    os.system("cls")

    print(horarioAtual)
    print(horarioDePausa)

    horarioAtual = datetime.now()

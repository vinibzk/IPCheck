import os
import socket
import uuid
import click
import subprocess
from tabulate import tabulate

def obter_informacoes_ip(ip):
    try:
        hostname = socket.gethostbyaddr(ip)[0]
        endereco_mac_local = obter_endereco_mac()
        latencia = obter_latencia(ip)

        limpar_tela()
        click.secho("====================================", fg="cyan", bold=True)
        click.secho("    Informações do IP    ", fg="cyan", bold=True)
        click.secho("====================================", fg="cyan", bold=True)

        data = [
            ["IP", ip],
            ["Hostname", hostname],
            ["Endereço MAC Local", endereco_mac_local],
            ["Latência (ms)", latencia]
        ]

        # Filtra as informações e substitui os campos vazios por "N/A"
        for i in range(len(data)):
            if data[i][1] == "":
                data[i][1] = "N/A"

        table = tabulate(data, tablefmt="fancy_grid")
        click.echo(table)
    except socket.herror as e:
        limpar_tela()
        click.secho(f"Erro ao obter informações do IP: {e}", fg="red")
    except Exception as e:
        limpar_tela()
        click.secho(f"Ocorreu um erro: {e}", fg="red")

def obter_endereco_mac():
    try:
        endereco_mac = ':'.join(['{:02x}'.format((uuid.getnode() >> elements) & 0xff) for elements in range(0,2*6,2)][::-1])
        return endereco_mac
    except Exception as e:
        return "N/A"

def obter_latencia(ip):
    try:
        # Usar o comando de sistema ping
        result = subprocess.run(['ping', '-c', '4', ip], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output = result.stderr.decode('utf-8')
        latencia = float(output.splitlines()[-1].split('/')[5])
        return round(latencia, 2)
    except subprocess.CalledProcessError:
        return "Erro"
    except Exception as e:
        return "Erro"

def limpar_tela():
    subprocess.call("clear" if "posix" in os.name else "cls")

@click.command()
def main():
    while True:
        limpar_tela()
        click.secho("====================================", fg="yellow", bold=True)
        click.secho("    Monitor de Conexões IP    ", fg="yellow", bold=True)
        click.secho("====================================", fg="yellow", bold=True)
        click.echo("Escolha uma opção:")
        click.echo("1. Consultar Informações de um IP")
        click.echo("2. Sair do Programa")
        
        escolha = click.prompt("Opção", type=int)
        
        if escolha == 1:
            limpar_tela()
            ip_digitado = click.prompt("Digite um endereço IP", type=str)
            obter_informacoes_ip(ip_digitado)
            input("\nPressione Enter para continuar...")
        elif escolha == 2:
            limpar_tela()
            click.secho("Encerrando o programa.", fg="yellow")
            break
        else:
            limpar_tela()
            click.secho("Opção inválida. Por favor, escolha novamente.", fg="red")
            input("\nPressione Enter para continuar...")

if __name__ == "__main__":
    main()
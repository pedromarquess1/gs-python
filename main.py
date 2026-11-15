import subprocess
import sys
from cli import executar_cli


def iniciar():
    print("=" * 55)
    print("TEM AGUA? - CENTRAL DE MONITORAMENTO E ABASTECIMENTO")
    print("=" * 55)
    print("Selecione o modo de execucao:")
    print("1 - Modo Terminal (CLI puro)")
    print("2 - Modo Interface Web (Streamlit)")
    print("0 - Sair")

    escolha = input("\nOpcao: ").strip()

    match escolha:
        case "1":
            executar_cli()
        case "2":
            print("\nIniciando servidor Streamlit no navegador...")
            try:
                subprocess.run([sys.executable, "-m", "streamlit", "run", "app.py"], check=True)
            except FileNotFoundError:
                print("[ERRO] Streamlit nao instalado. Execute: pip install -r requirements.txt")
            except KeyboardInterrupt:
                print("\nServidor encerrado pelo usuario.")
        case "0":
            print("Encerrando...")
        case _:
            print("[AVISO] Opcao invalida.")


if __name__ == "__main__":
    iniciar()
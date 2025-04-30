from datetime import datetime
import colorama

colorama.init()

class Logs:
    def __init__(self):
        self.colors = {
            "INFO": colorama.Fore.BLUE,
            "SUCCESS": colorama.Fore.GREEN,
            "WARNING": colorama.Fore.YELLOW,
            "ERROR": colorama.Fore.RED,
            "MESSAGE": colorama.Fore.MAGENTA,
            "CRITICAL": colorama.Fore.RED,
            "RESET": colorama.Fore.RESET
        }

    def _log(self, tipo, mensagem):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cor = self.colors.get(tipo, self.colors["RESET"])
        
        # Console colorido
        print(f"{cor}[{timestamp}] [{tipo}] {mensagem}{self.colors['RESET']}")
        
        # Arquivo de log
        with open("bot.log", "a", encoding="utf-8") as f:
            f.write(f"[{timestamp}] [{tipo}] {mensagem}\n")

    # Métodos específicos
    def info(self, mensagem):
        self._log("INFO", mensagem)

    def warning(self, mensagem):
        self._log("WARNING", mensagem)

    def error(self, mensagem):
        self._log("ERROR", mensagem)

    def critical_error(self, mensagem):
        self._log("CRITICAL", mensagem)

    def new_message(self, remetente, texto):
        self._log("MESSAGE", f"Nova mensagem de {remetente}: {texto}")

    def login_attempt(self):
        self._log("INFO", "Tentando fazer login no Instagram...")

    def login_success(self):
        self._log("SUCCESS", "Login realizado com sucesso!")

    def login_failure(self, erro):
        self._log("ERROR", f"Falha no login: {erro}")

    def no_threads_found(self):
        self._log("WARNING", "Nenhuma conversa encontrada.")

    def monitoring_error(self, erro):
        self._log("ERROR", f"Erro durante monitoramento: {erro}")

    def shutdown(self):
        self._log("INFO", "Encerrando o bot...")
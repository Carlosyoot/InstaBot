from instagrapi import Client
from instagrapi.types import DirectMessage, DirectThread
import os
import json
from logs import Logs


logger = Logs()

SESSION_FILE = "session.json"

instagram = Client()
meu_id = None

UltimasMsg = {}


def login(username: str, password: str):
    global meu_id

    if os.path.exists(SESSION_FILE):
        try:
            instagram.load_settings(SESSION_FILE)
            instagram.login(username, password)
            meu_id = instagram.user_id
            print("Login com cache de sessão.")
            return {"user_id": meu_id, "cached": True}
        except Exception as e:
            print("Erro ao carregar sessão, tentando login limpo:", e)

    try:
        instagram.login(username, password)
        instagram.dump_settings(SESSION_FILE)
        meu_id = instagram.user_id
        print("Login feito e sessão salva.")
        return {"user_id": meu_id, "cached": False}
    except Exception as e:
        print("Erro ao logar:", e)
        raise Exception(str(e))

def ProcessarBusca() -> list:
    """
    Retorna lista de mensagens formatadas (sem salvar em arquivo)
    """
    try:
        threads = instagram.direct_threads(amount=10, thread_message_limit=20)
        
        if not threads:
            logger.no_threads_found()
            return []

        mensagens_formatadas = []

        for thread in threads:
            if not thread.messages:
                continue

            for mensagem in thread.messages:
                msg_data = {
                    "id_usuario": mensagem.user_id,
                    "usuario": ObterUsername(mensagem.user_id),
                    "hora": str(mensagem.timestamp),
                    "tipo_mensagem": None,
                    "conteúdo": None,
                    "thread_id": thread.id  # Adicionei para referência
                }

                if mensagem.text:
                    msg_data["tipo_mensagem"] = "text"
                    msg_data["conteúdo"] = mensagem.text

                elif hasattr(mensagem, 'reel_share') and mensagem.reel_share:
                    msg_data["tipo_mensagem"] = "reel"
                    msg_data["conteúdo"] = {
                        "id": mensagem.reel_share.media.id,
                        "share_url": f"https://www.instagram.com/reel/{mensagem.reel_share.media.id}/"
                    }

                elif hasattr(mensagem, 'clip') and mensagem.clip:
                    msg_data["tipo_mensagem"] = "clip"
                    msg_data["conteúdo"] = {
                        "id": mensagem.clip.pk,
                        "share_url": f"https://www.instagram.com/reel/{mensagem.clip.pk}/"
                    }

                elif hasattr(mensagem, 'media') and mensagem.media:
                    if mensagem.media.media_type == 1:
                        msg_data["tipo_mensagem"] = "image"
                        msg_data["conteúdo"] = {"id": mensagem.media.pk}
                    elif mensagem.media.media_type == 2:
                        msg_data["tipo_mensagem"] = "video"
                        msg_data["conteúdo"] = {"id": mensagem.media.pk}

                else:
                    msg_data["tipo_mensagem"] = "unknown"
                    msg_data["conteúdo"] = "Tipo não identificado"

                # Log opcional (se quiser manter)
                logger.new_message(
                    remetente=f"Usuário: {msg_data['usuario']}",
                    texto=f"[{msg_data['tipo_mensagem'].upper()}] {msg_data['conteúdo']}"
                )

                mensagens_formatadas.append(msg_data)

        return mensagens_formatadas

    except Exception as e:
        logger.monitoring_error(f"Erro ao processar threads: {str(e)}")
        raise  # Re-lança a exceção para ser tratada no FastAPI


def ObterUsername(id):
    response = instagram.user_info_v1(id)

    User = response.username
    return User

def ObterVideo(media_id: str, path: str = ".", download: bool = False) -> str:
    result = instagram.media_info(media_id)
    
    if download:
        instagram.clip_download(media_id, path)
        print(f"Vídeo baixado em: {path}")
    else:
        shortcode = result.code
        link = f"https://www.instagram.com/reel/{shortcode}/"
        print(f"Link de compartilhamento: {link}")
        return link

if __name__ == "__main__":
    # Substitua pelas suas credenciais do Instagram
    USERNAME = "Iter.yoot"
    PASSWORD = "23092005"

    try:
        # 1. Login
        login(USERNAME, PASSWORD)
        #logger.login_success()
        
        ObterVideo("3592136403455302979", download=False)  # retorna o link 
        

        
       

        # 2. Processar mensagens
        #ProcessarBusca()

    except Exception as e:
        logger.critical_error(f"Erro no script principal: {e}")
    finally:
        logger.shutdown()
from flask import session, flash, redirect, url_for
import functools

# Função para verificar se existe uma viagem ativa
def is_session_active():
    return "viagens" in session and len(session.get("viagens", [])) > 0

# Middleware para verificar se existe uma viagem ativa
def session_required(func):
    @functools.wraps(func)
    def check_session(*args, **kwargs):
        if not is_session_active():
            flash("Você precisa adicionar uma viagem para acessar o diário!", "error")
            return redirect(url_for("cadastro"))
        return func(*args, **kwargs)

    return check_session
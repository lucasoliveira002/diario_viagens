from flask import (
    session,
    flash,
    redirect,
    url_for,
    make_response,
    render_template,
    request,
)
from controllers.middleware import session_required, is_session_active
import functools
from models.viagem import Viagem
from datetime import datetime, timedelta

#funçao para pegar as viagens
def get_viagens():
    viagens_dicts = session.get("viagens", [])
    return [Viagem.from_dict(viagem) for viagem in viagens_dicts]

#função para adicionar uma viagem
def add_viagem(viagem):
    viagens = get_viagens()
    viagens.append(viagem)
    session["viagens"] = [viagem.to_dict() for viagem in viagens]

#funçao para atualizar uma viagem
def update_viagem(index, updated_viagem):
    viagens = get_viagens()
    if 0 <= index < len(viagens):
        viagens[index] = updated_viagem
        session["viagens"] = [viagem.to_dict() for viagem in viagens]

#funçao para remover uma viagem
def remove_viagem(index):
    viagens = get_viagens()
    if 0 <= index < len(viagens):
        del viagens[index]
        session["viagens"] = [viagem.to_dict() for viagem in viagens]

#limpa as viagens
def clear_viagens():
    session["viagens"] = []

#retorna o total de viagens
def get_total_viagens():
    return len(get_viagens())

# Função para definir o cookie do total de viagens
def set_cookie_total_viagens(response):
    total_viagens = get_total_viagens()
    response.set_cookie("total_viagens", str(total_viagens))
    return response

#rota para página principal 
@session_required
def index():
    viagens = get_viagens()
    response = make_response(render_template("index.html", viagens=viagens, total_viagens=get_total_viagens()))
    return set_cookie_total_viagens(response)

#rota para limpar o diário
@session_required
def clear_diary():
    clear_viagens()
    flash("Diário limpo com sucesso!", "success")
    response = redirect(url_for("index"))
    return set_cookie_total_viagens(response)

#rota para deletar uma viagem
@session_required
def delete_viagem(index):
    remove_viagem(index)
    flash('Viagem removida com sucesso!', 'success')
    response = redirect(url_for('index'))
    return set_cookie_total_viagens(response)

#rota para cadastro de viagens
def cadastro():
    if request.method == "POST":
        destino = request.form["destino"]
        data = request.form["data"]
        descricao = request.form["descricao"]
        nota = request.form["nota"]

        if not destino or not data or not descricao or not nota:
            flash("Todos os campos precisam ser preenchidos!", "error")
            return render_template("cadastro.html")

        try:
            date_obj = datetime.strptime(data, '%Y-%m-%d')
        except ValueError:
            flash("Formato de data inválido!", "error")
            return render_template("cadastro.html")

        min_date = datetime.now() - timedelta(days=365 * 100) # Calcula a data mínima (100 anos atrás)
        if date_obj < min_date:
            flash("Não é possível cadastrar viagens com mais de 100 anos!", "error")
            return render_template("cadastro.html")
        
        max_date = datetime.now() + timedelta(days=365 * 10) # Calcula a data máxima (10 anos no futuro)
        if date_obj > max_date:
            flash("Não é possível cadastrar viagens com mais de 10 anos no futuro!", "error")
            return render_template("cadastro.html")
            
        try:
            nota = int(nota)
            if nota < 1 or nota > 5:
                flash("A nota deve ser entre 1 e 5!", "error")
                return render_template("cadastro.html")
        except ValueError:
            flash("A nota deve ser um número inteiro!", "error")
            return render_template("cadastro.html")

        viagem = Viagem(destino, data, descricao, nota)
        add_viagem(viagem)

        flash("Viagem adicionada com sucesso!", "success")
        response = redirect(url_for("index"))
        return set_cookie_total_viagens(response)

    return render_template("cadastro.html")

#rota para editar uma viagem
@session_required
def edit_viagem(index):
    viagens = get_viagens()
    if index < 0 or index >= len(viagens):
       flash('Viagem não encontrada!', 'error')
       return redirect(url_for('index'))

    viagem = viagens[index]
    if request.method == 'POST':
        destino = request.form['destino']
        data = request.form['data']
        descricao = request.form['descricao']
        nota = request.form['nota']

        if not destino or not data or not descricao or not nota:
           flash("Todos os campos precisam ser preenchidos!", "error")
           return render_template('edicao.html', viagem=viagem, index=index)

        try:
             date_obj = datetime.strptime(data, '%Y-%m-%d')
        except ValueError:
            flash("Formato de data inválido!", "error")
            return render_template('edicao.html', viagem=viagem, index=index)

        min_date = datetime.now() - timedelta(days=365 * 100)
        if date_obj < min_date:
           flash("Não é possível editar viagens com mais de 100 anos!", "error")
           return render_template('edicao.html', viagem=viagem, index=index)

        max_date = datetime.now() + timedelta(days=365*10)
        if date_obj > max_date:
              flash("Não é possível editar viagens com mais de 10 anos no futuro!", "error")
              return render_template('edicao.html', viagem=viagem, index=index)

        try:
            nota = int(nota)
            if nota < 1 or nota > 5:
                flash("A nota deve ser entre 1 e 5!", "error")
                return render_template('edicao.html', viagem=viagem, index=index)
        except ValueError:
            flash("A nota deve ser um número inteiro!", "error")
            return render_template('edicao.html', viagem=viagem, index=index)

        updated_viagem = Viagem(destino, data, descricao, nota)
        update_viagem(index, updated_viagem)
        flash('Viagem editada com sucesso!', 'success')
        response = redirect(url_for('index'))
        return set_cookie_total_viagens(response)
    
    return render_template('edicao.html', viagem=viagem, index=index)
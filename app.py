from flask import Flask, session
from controllers.viagem_controller import (
    index,
    cadastro,
    edit_viagem,
    delete_viagem,
    clear_diary,
    render_template,
)
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)

#Rotassss 
app.add_url_rule("/", view_func=index, methods=['GET'])
app.add_url_rule("/cadastro", view_func=cadastro, methods=['GET', 'POST'])
app.add_url_rule("/edit/<int:index>", view_func=edit_viagem, methods=['GET', 'POST'])
app.add_url_rule("/delete/<int:index>", view_func=delete_viagem, methods=['POST'])
app.add_url_rule("/clear", view_func=clear_diary, methods=['POST'])


#gerenciamento de erros
@app.errorhandler(404) 
def page_not_found(e):
   return render_template('erros/404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('erros/500'), 500


if __name__ == "__main__":
    app.run(debug=True)
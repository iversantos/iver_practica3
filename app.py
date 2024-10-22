from flask import Flask, render_template, request, session, redirect, url_for
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'supersecreto'  

@app.route('/', methods=['GET', 'POST'])
def registro_seminarios():
    if request.method == 'POST':
        fecha = request.form['fecha']
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        turno = request.form['turno']
        seminarios = request.form.getlist('seminarios') 

        inscrito = {
            'fecha': fecha,
            'nombre': nombre,
            'apellido': apellido,
            'turno': turno,
            'seminarios': seminarios
        }

        if 'inscritos' not in session:
            session['inscritos'] = []

        session['inscritos'].append(inscrito)
        session.modified = True 
        return redirect(url_for('lista_inscritos'))

    return render_template('registro_seminarios.html')

@app.route('/lista_inscritos')
def lista_inscritos():
    inscritos = session.get('inscritos', [])
    return render_template('lista_inscritos.html', inscritos=inscritos, enumerate=enumerate)

@app.route('/eliminar/<int:index>')
def eliminar_inscrito(index):
    if 'inscritos' in session:
        inscritos = session['inscritos']
        if 0 <= index < len(inscritos):
            inscritos.pop(index)
            session.modified = True  
    return redirect(url_for('lista_inscritos'))

@app.route('/editar/<int:index>', methods=['GET', 'POST'])
def editar_inscrito(index):
    if 'inscritos' not in session or index < 0 or index >= len(session['inscritos']):
        return redirect(url_for('lista_inscritos'))

    if request.method == 'POST':
        fecha = request.form['fecha']
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        turno = request.form['turno']
        seminarios = request.form.getlist('seminarios')

        inscrito = {
            'fecha': fecha,
            'nombre': nombre,
            'apellido': apellido,
            'turno': turno,
            'seminarios': seminarios
        }

        session['inscritos'][index] = inscrito 
        session.modified = True  

        return redirect(url_for('lista_inscritos'))

    inscrito = session['inscritos'][index] 
    return render_template('editar_inscrito.html', inscrito=inscrito, index=index)

if __name__ == '__main__':
    app.run(debug=True)
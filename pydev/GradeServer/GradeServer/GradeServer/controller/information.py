from flask import render_template
from GradeServer.GradeServer_blueprint import GradeServer

@GradeServer.route('/manual', methods=['GET', 'POST'])
def manual_page():
    return  render_template('/manual.html')
  
@GradeServer.route('/admin_manual', methods=['GET', 'POST'])
def admin_manual_page():
    return render_template('admin_manual.html')
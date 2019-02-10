from flask import Flask, render_template, request, redirect, url_for, flash
import os
import subprocess

app = Flask(__name__)

#To keep session alive through page redirects
app.secret_key = 'mysecretkey123'

@app.route('/')
def index():
        with open('/opt/myapp/squid/whitelist.txt','r') as file:
                file_content = file.readlines()
        return render_template('index.html', exceptions = file_content)

@app.route('/add_exception', methods=['POST'])
def add_exception():
    if request.method == 'POST':
        fqdn_add = request.form['fqdn_add']
        with open('/opt/myapp/squid/whitelist.txt','a') as file:
                file.writelines(fqdn_add + "\n")

        warningmsg = "%s add successfully from the whitelist!" % fqdn_add
        flash(warningmsg)
        return redirect(url_for('index'))

@app.route('/remove_exception', methods=['POST'])
def remove_exception():
    if request.method == 'POST':
        fqdn_remove = request.form['fqdn_remove']
        with open('/opt/myapp/squid/whitelist.txt','r') as file:
                whitelist = [line.strip() for line in file]
        
        if fqdn_remove in whitelist:
                whitelist.remove(fqdn_remove)
                with open('/opt/myapp/squid/whitelist.txt', 'w') as file:
                        file.writelines("%s\n" % line for line in whitelist)
        
                warning = "%s removed successfully from the whitelist!" % fqdn_remove
                flash(warning)
                return redirect(url_for('index'))
        else:
                warning = "%s was not found in the current whitelist!" % fqdn_remove
                flash(warning)
                return redirect(url_for('index'))   


@app.route('/squid_reload', methods=['POST'])
def squid_reload():
    if request.method == 'POST':
        status_command="service hwclock.sh restart"
        #status_command="sudo systemctl restart squid"
        run_command = subprocess.Popen(status_command, stdout=subprocess.PIPE, shell=True)
        (output, err) = run_command.communicate()
        command_status = run_command.wait()
        warning = "Return code %s: \n Output: %s" % (command_status,output)
        flash(warning)
        return redirect(url_for('index'))       



@app.route('/squid_status', methods=['POST'])
def squid_status():
    if request.method == 'POST':
        status_command="service --status-all"
        #status_command="sudo systemctl status squid"
        run_command = subprocess.Popen(status_command, stdout=subprocess.PIPE, shell=True)
        (output, err) = run_command.communicate()
        command_status = run_command.wait()
        warning = "Return code %s: \n Output: %s" % (command_status,output)
        flash(warning)
        return redirect(url_for('index'))

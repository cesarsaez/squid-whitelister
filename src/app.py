from flask import Flask, render_template, request, redirect, url_for, flash
import os
import subprocess

app = Flask(__name__)
#To keep session alive through page redirects
app.secret_key = 'mysessionsecret1234'

whitelist_path = "/opt/myapp/squid/whitelist.txt"
#whitelist_path = "squid/whitelist.txt"
squid_status_command="service hwclock.sh restart"
#squid_status_command="sudo systemctl status squid"
squid_reload_command="service hwclock.sh status"
#squid_reload_command="sudo systemctl restart squid"


@app.route('/')
def index():
        with open(whitelist_path,'r') as file:
                file_content = file.readlines()
        return render_template('index.html', exceptions = file_content)

@app.route('/add_exception', methods=['POST'])
def add_exception():
    if request.method == 'POST':
        fqdn_add = request.form['fqdn_add']

        if len(fqdn_add) > 4:
                with open(whitelist_path,'a') as file:
                        file.writelines(fqdn_add + "\n")

                warningmsg = "%s added successfully to the whitelist!" % fqdn_add
                flash(warningmsg)
                return redirect(url_for('index'))
        else:
                warningmsg = "%s is not a valid FQDN" % fqdn_add
                flash(warningmsg)
                return redirect(url_for('index'))


@app.route('/remove_exception', methods=['POST'])
def remove_exception():
    if request.method == 'POST':
        fqdn_remove = request.form['fqdn_remove']
        with open(whitelist_path,'r') as file:
                whitelist = [line.strip() for line in file]
        
        if fqdn_remove in whitelist:
                whitelist.remove(fqdn_remove)
                with open(whitelist_path, 'w') as file:
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
        run_command = subprocess.Popen(squid_reload_command, stdout=subprocess.PIPE, shell=True)
        (output, err) = run_command.communicate()
        command_status = run_command.wait()
        warning = "Return code %s: \n Output: %s" % (command_status,output)
        flash(warning)
        return redirect(url_for('index'))       



@app.route('/squid_status', methods=['POST'])
def squid_status():
    if request.method == 'POST':
        run_command = subprocess.Popen(squid_status_command, stdout=subprocess.PIPE, shell=True)
        (output, err) = run_command.communicate()
        command_status = run_command.wait()
        warning = "Return code %s: \n Output: %s" % (command_status,output)
        flash(warning)
        return redirect(url_for('index'))

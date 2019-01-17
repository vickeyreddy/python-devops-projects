import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('cihcisdapp835.corporate.ge.com',
            username='de575352',
            password=raw_input("Enter Password: "))
stdin, stdout, stderr = ssh.exec_command("uptime;ls -l;")
stdin.flush()
data = stdout.read().splitlines()
for line in data:
    print line
#ssh.close()

import subprocess

subprocess.call("echo \"This is a test email from the app server\" | mail -s \"Python Test Email\" agentry@magswitch.com.au")


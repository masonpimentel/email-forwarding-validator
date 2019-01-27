To start, you'll need two Gmail accounts: one that will 

crontab -e
*/10 * * * * /home/snxfz-app/email-validator/cronjob

See cron logs:
grep CRON /var/log/syslog

`./kill` to kill send and recieve
This lets the cronjob automatically start send and recieve again

`./clear` to clear the output.txt logs

To configure send:

cd email-validator/src

receive/config
send/config



Run config script in send and receive to create a token.json if it already hasn't been
Running start in send and recieve will run a nohup instance so the process isn't killed when the terminal session is closed

Installing relevant tools

pip install --upgrade google-api-python-client oauth2client

TODO
1. move send and receive out of src
2. prevent token and config from being version controlled
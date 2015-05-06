#/bin/sh

# space separated list of emails to send reports to
EMAILS=""
cd /opt/carlyle_sync && /opt/carlyle_sync/env/bin/python /opt/carlyle_sync/run_new.py > /opt/carlyle_sync/log/cron.log 2>&1
/opt/carlyle_sync/env/bin/python /opt/carlyle_sync/stripcolor.py /opt/carlyle_sync/log/cron.log | mail -s "Carlyle Sync Results `date +%Y-%m-%d:%H:%M`" $EMAILS

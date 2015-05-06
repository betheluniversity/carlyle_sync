import colorama, fileinput, sys;
colorama.init(strip=True);

# for line in fileinput.input(["log/cron.log"]):
for line in fileinput.input():
    sys.stdout.write(line)

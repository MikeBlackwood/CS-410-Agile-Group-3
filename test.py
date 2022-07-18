from ftplib import FTP

#————————————————————————————————————————————————————————————————————————
# This is just an experiment. We should delete it as soon as we get
# something connecting and doing something interesting.
#————————————————————————————————————————————————————————————————————————
    
# Connect to Debian's FTP site as Guest
ftp = FTP('ftp.us.debian.org')
ftp.login()

# Set the remote working directory to 'debian'
result = ftp.cwd('debian')
print(result)

# List the files here
result = ftp.retrlines('LIST')
print(result)

# Transfer a file into the local working directory
with open('README', 'wb') as fp:
    result = ftp.retrbinary('RETR README', fp.write)
    print(result)

# Disconnect
ftp.quit()

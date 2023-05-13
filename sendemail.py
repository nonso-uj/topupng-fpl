import smtplib, ssl

port = 587
password = 'pflhoyxhjdroofcj'

context = ssl.create_default_context()

with smtplib.SMTP("smtp.gmail.com", port) as server:
    server.ehlo()
    server.starttls(context=context)
    server.ehlo()
    server.login("nonso.udonne@gmail.com", password)
    server.sendmail("nonso.udonne@gmail.com", "casamamigos@gmail.com", "sup man testing testing")
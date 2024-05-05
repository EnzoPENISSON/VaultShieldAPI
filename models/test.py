import smtplib
content="Hello World"
mail=smtplib.SMTP('10.193.190.100', 587)
mail.ehlo()
mail.starttls()
sender='contact@vaultshield.com'
recipient='enzopenisson25@orange.fr'
mail.login('username','password')
header='To:'+recipient+'\n'+'From:' \
+sender+'\n'+'subject:testmail\n'
content=header+content
mail.sendmail(sender, recipient, content)
mail.close()


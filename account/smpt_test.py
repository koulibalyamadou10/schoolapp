import smtplib

try:
    smtp_server = smtplib.SMTP_SSL('smtp-fr.securemail.pro', 465)
    smtp_server.login('schoolapp@stock-manager.store', 'a.u3BZ+GDERzdcp')
    print("Connexion SMTP réussie !")
    smtp_server.quit()
except Exception as e:
    print(f"Erreur SMTP : {e}")
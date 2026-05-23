from pyngrok import ngrok

public_url = ngrok.connect(5000)

print("🔥 OPEN THIS LINK ON PHONE:")
print(public_url)
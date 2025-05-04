import requests

url = "https://impala-inviting-amoeba.ngrok-free.app/generate-text-to-voice/en"
headers = {
  "Content-Type": "application/json",
  "X-API-Key": "AAAA-BBBB-CCCC-DDD"
}

text = """
[S1] Why did the scarecrow win an award?  
[S2] (sighs) I'll bite…  
[S1] Because he was *outstanding* in his field!  
[S2] You're really *crop*-ping these puns today.  
[S1] (laughs) Don't be so *corn*y—it's a-maize-ing!  
[S2] I need oxygen.  
[S1] Relax, I'll *leaf* you alone.  
[S2] Thank. You.
"""
resp = requests.post(url, json={"text":text}, headers=headers)
print(resp.status_code)
with open("speech.mp3","wb") as f:
    f.write(resp.content)
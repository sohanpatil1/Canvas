import twilio
from twilio.rest import Client 
 
account_sid = 'ACb42ed908ae21638215f40879f07ae965' 
auth_token = '3c2741fb94ec782a64cd2e830183d653' 
client = Client(account_sid, auth_token) 
 
message = client.messages.create(  
                              messaging_service_sid='MGb50838bc488cfdd79a2eb3ab55e31b42', 
                              body='Hello',      
                              to='+16694547233' 
                          ) 
 
print(message.sid)
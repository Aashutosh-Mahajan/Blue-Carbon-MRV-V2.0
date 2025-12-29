from api.models import Purchase
from django.core.mail import EmailMessage
p=Purchase.objects.filter(pk=20).first()
print('purchase:', p)
buyer = p.corporate
print('buyer username:', buyer.username, 'email:', repr(buyer.email))
try:
    msg=EmailMessage('Test from Blue Carbon MRV', 'This is a test email from the app.', to=[buyer.email or buyer.username])
    res = msg.send()
    print('send returned', res)
except Exception as e:
    import traceback; traceback.print_exc()

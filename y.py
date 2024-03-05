import http.cookies

cookie_string = "route=54647b57aa98c4a29d34d582d156df6c; _gid=GA1.2.1733765669.1709372763; g_state={\"i_l\":0}; _got=1; ferizy=31rq170hk2j7uo3fqn1a7dqt4214qpg3; _gat_gtag_UA_145471306_1=1; _ga=GA1.1.809876557.1707222765; _ga_1RVG45K2YV=GS1.1.1709372763.22.1.1709376076.9.0.0"

cookie = http.cookies.SimpleCookie()
cookie.load(cookie_string)

# Mengambil nilai dari cookie tertentu, misalnya "route"
route_value = cookie.get("route").value

print("Token dari cookie 'route':", route_value)

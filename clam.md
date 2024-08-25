# Skolportalen Authentication (requires username/password)

## GET -> https://skolportal.uppsala.se/wa/auth/wil/?authmech=Elever%20och%20l%C3%A4rare%20p%C3%A5%20skolan

- Raw: Provides `hag_cookies`
- With `hag_cookies`
- With `hag_cookies` and NTLM authentication (comes as two requests due to NTLM authentication)

# Skola24 Authentication (requires Skolportalen `hag_cookies`)

## GET -> https://uppsala-sso.skola24.se/

- Raw: Provides `skola_cookies`

## GET -> https://skolportal.uppsala.se/?c=1

- With `skola_cookies`

## GET -> https://skolportal.uppsala.se/

- With `skola_cookies`

## GET -> https://service-sso1.novasoftware.se/saml-2.0/authenticate?customer=https%3a%2f%2fskolfederation.uppsala.se%2fidp&targetsystem=Skola24

- Raw: Provides `saml_data1`

## POST -> https://skolfederation.uppsala.se/wa/auth/saml/

- With `hag_cookies` and `saml_data1`: Provides `saml_data`

## POST -> https://service-sso1.novasoftware.se/saml-2.0/response

- With `saml_data2`: Provides `sign_in_url`

## GET -> `sign_in_url`

- With `skola_cookies`

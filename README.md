
# IGNInterage
Modulo para interagir no forum IGN boards, loga usando cookies do firefox, cria topico, comenta, edita, react etc. (win)

## requerimentos
- Windows
- Navegador Firefox
- geckodriver.exe: https://github.com/mozilla/geckodriver/releases
- python >=3.6

## instalação
   TODO

## uso
- Primeiro realize o login no Firefox.

 
        From igninterage import IGNinterage

        driver_location = r'C:\Users\User\user\geckodriver.exe'
        cookie_file = 'cache.session'
        ign = IGNInterage(driver_location, cookie_file)
        if not ign.check_login():
            ign.ign_login()
        ign.novo_topico('teste', 'som som teste', 'vale-tudo.80331/')    
        ign.editar_topico('teste editado', '[edit] ei ei som', '123456789', '17')
        ign.comentar(text='isso foi postado com a "API" rsrsrsrs', thread='123456789')
        ign.editar_comentario('[EDITt] e agora foi editado usando a "API"', '123456789')
        ign.react(react_id='1', post_id='123456789')
## TODO:
O modulo em si.

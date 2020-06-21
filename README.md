
# IGNInterage
Modulo para interagir no forum IGN boards, loga usando cookies do firefox, comenta, edita, react etc. (win)

## requirementos
- Windows
- Navegador Firefox
- geckodriver.exe: https://github.com/mozilla/geckodriver/releases
- python >=3.6

## instalation
   TODO

## usage
- Primeiro realize o login no Firefox.

 
        From igninterage import IGNinterage

        driver_location = r'C:\Users\User\user\geckodriver.exe'
        cookie_file = 'cache.session'
        ign = IGNInterage(driver_location, cookie_file)
        if not ign.check_login():
            ign.ign_login()

        ign.comentar(text='isso foi postado com a "API" rsrsrsrs', thread='123456789')
        ign.editar_comentario('[EDITt] e agora foi editado usando a "API"', '123456789')
        ign.react(text='1', post_id='123456789')
## TODO:
O modulo em si.

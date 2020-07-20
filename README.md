
# inginterage
Modulo para interagir no forum IGN boards, loga usando cookies do firefox, cria topico, comenta, edita, react etc.

## requerimentos
- Windows
- Navegador Firefox
- python >=3.6

## instalação
    pip3 install git+git://github.com/psychodinae/IGNInterage.git
    ou
    pip3 install --upgrade https://github.com/psychodinae/IGNInterage/tarball/master

## uso
- Primeiro realize o login no forum no Firefox.

 
        From igninterage import IGNinterage

        cookie_file = 'cache.session'
        url = 'https://www.ignboards.com/'
        header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/70.0.3538.77 Safari/537.36',
                 }
        ign.ign_login()
        
        ign.novo_topico('teste', 'som som teste', 'vale-tudo.80331/')    
        ign.editar_topico('teste editado', '[edit] ei ei som', '123456789', '17')
        ign.comentar(text='isso foi postado com a "API" rsrsrsrs', thread='123456789')
        ign.editar_comentario('[EDITt] e agora foi editado usando a "API"', '123456789')
        ign.react(react_id='1', post_id='123456789')

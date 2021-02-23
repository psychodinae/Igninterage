
# inginterage
Modulo para interagir no forum IGN boards, loga usando cookies dos navegadores Firefox (default) e Chrome, cria topico, comenta, edita, react e mensagem privada.

## requerimentos
- Navegador Chrome/Firefox
- python >=3.6

## instalação
    pip install igninterage
    
    ou instale a última versão:
    pip install --upgrade https://github.com/psychodinae/igninterage/tarball/master

## uso
- Primeiro realize o login no forum usando o navegador e feche-o.

 
        from igninterage import Igninterage


        ign = Igninterage('https://www.ignboards.com/')
        ign.ign_login()
        
        ign.novo_topico('teste', 'som som teste', 'vale-tudo.80331/')    
        ign.editar_topico('teste editado', '[edit] ei ei som', '123456789', '17')
        ign.comentar(text='isso foi postado com a "API" rsrsrsrs', thread='123456789')
        ign.editar_comentario('[EDITt] e agora foi editado usando a "API"', '123456789')
        ign.react(react_id='1', post_id='123456789')
        ign.msg_privada('meu assunto', 'minha conversa', 'NickdoUsuario')
        ign.msg_privada('meu outro assunto', 'minha outra conversa', 'NickdoUsuario', 'NickdeOutroUsuario')
        
        
- uma vez recuperado os cokies usando o navegador é possivel armazena-los no formato json por exemplo:
 
        import json
        from igninterage import Igninterage

        ign = Igninterage('https://www.ignboards.com/', navegador='chrome')
        ign.ign_login()
        cookies_salvos = json.dumps(ign.get_cookies_as_dict())
        > {"xf_user": "4345353535-etertagabayata3665a643634b6b6b6", "xf_csrf": "tetETn54778", "xf_..."}

-  Posteriormente:
  
        import json
        from igninterage import Igninterage
        
        ign = Igninterage('https://www.ignboards.com/')
        ign.set_cookie(json.loads(cookies_salvos))
        ign.comentar(text='isso foi postado com a "API" rsrsrsrs', thread='123456789')
        > logado ok! 
        > postou no topico...

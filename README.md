
# inginterage
Modulo para interagir no forum IGN boards, loga usando cookies do firefox, cria topico, comenta, edita, react e mensagem privada.

## requerimentos
- Windows
- Navegador Firefox
- python >=3.6

## instalação
    pip install igninterage
    
    ou instale a última versão:
    pip3 install --upgrade https://github.com/psychodinae/IGNInterage/tarball/master

## uso
- Primeiro realize o login no forum usando o navegador Firefox.

 
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

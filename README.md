# Diario de viagens

Este projeto faz o uso do MVC e nele pode-se adicionar, editar e excluir registros de viagens

# Importante

- como funcionalidade extra foi implementado um datetime que valida o ano da viagem, ou seja,
se a viagem for muito antiga (100 anos atrás) ela é inválida e uma flash message de aviso é mostrada,
para datas é um pouco diferente, optei por permitir adicionar viagens que não conteceram (até 10 anos no futuro), 
o motivo é para que os usários possam registrar viagens que GOSTARIAM de fazer num futuro próximo. 

- As telas de erro são as mesmas de um outro trabalho, apenas mudei a cor, mas até os GIFS são os mesmos

- O número total de viagens na tela após uma exclusão deve ser atualizado após rearregar a página, não é instantaneo

- O css ele tenta fazer com que o site seja no modo escuro, eu acho mais confortável
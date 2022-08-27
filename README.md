# Backend da aplicação e arquivo responsável pela atualização do banco

O frontend pode ser encontrado [aqui](https://github.com/MarceloRocha98/sum_frontend)

A demonstração pode ser observada aqui: [https://www.loom.com/share/f10ff5588d68489f845d915f25323da3](https://www.loom.com/share/f10ff5588d68489f845d915f25323da3)
# Observações

1) O programa responsável pela atualização automática do banco através do "blotter_generator.py" é o "blotter_service.py"

2) O "blotter_service.py" considera, para fins de exemplo, a inserção dos dados de trading somente para o user_id = 1

3) O arquivo "blotter_service.py" gera um .txt chamado "cursor.txt", que armazenará a ultima linha salva para salvar o estado do programa, caso seja reiniciado

4) Na implementação do "blotter_service.py", optou-se pelo uso do SQLAlchemy, por atualizar o banco mais rapidamente do que os requests por conta da quantidade de dados, no entanto, deve-se alterar o path do arquivo "db.sqlite3" do django para rodar na maquina local (na versão aqui postada o path do banco corresponde ao da minha máquina local)

5) O email de usuário é único


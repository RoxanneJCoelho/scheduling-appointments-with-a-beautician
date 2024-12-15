import datetime as dt

# Função responsavel por registar os erros que ocorrem no programa num ficheiro destinado para registar erros
def registar_erro(mensagem):
  with open ('ficheiro_log.txt','a') as f_log:
      f_log.write(str(dt.datetime.now())+'\n')
      f_log.write(str(mensagem)+'\n')
      f_log.write('\n\n') 
    
# Função responsavel por apagar o conteudo que  existe dentro do ficheiro de erro
def reiniciar_f_log():
  with open('ficheiro_log.txt','w') as f_log:
      f_log.write('')


# Esta função emprime todos os erros que ocorreram bem como a respectiva data, hora, minuto e segundo
def ler_f_log():
  with open('ficheiro_log.txt','r') as f_log:
      print(f_log.read())
  





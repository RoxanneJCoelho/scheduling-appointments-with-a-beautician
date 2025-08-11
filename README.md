# [PT] Agendamento de sessões de estética 💅 - Python e SQLite
**Autora**: Roxanne Coelho

### Descrição
Este projeto consiste numa aplicação **Python** integrada com **SQLite** para gerir marcações de sessões de estética.
Permite:
- Registo de clientes
- Gestão de serviços disponíveis
- Agendamento, cancelamento e reagendamento de marcações
- Consulta das marcações existentes

O sistema funciona em **modo consola** e utiliza um menu interativo para que o cliente possa aceder ao seu espaço, consultar serviços e gerir as suas marcações.

---

### Tecnologias usadas
- Python 3
- SQLite3 (base de dados local)
- Módulo *datetime* (validação de datas e horas)

---

### Estrutura do Projeto
```plaintext
 📦 scheduling-appointments-with-a-beautician
┣ 📜 trabalho final de python estética.py           # Código principal da aplicação
┣ 📜 LOG.py                                         # Funções de registo de erros (referenciado no código)
┣ 📜 estetica.db                                    # Base de dados SQLite (gerada automaticamente)
┗ 📜 README.md                                      # Documentação do projeto
```

---

### Instalação e Utilização
1. Clonar o repositório
 ```bash
https://github.com/RoxanneJCoelho/scheduling-appointments-with-a-beautician.git                                
```

2. Aceder a pasta do projeto
  ```bash
cd scheduling-appointments-with-a-beautician                              
```
   
3. Executar o programa
  ```bash
python "trabalho final de python estética.py"                         
```

---

### Notas
- A base de dados (estetica.db) é criada automaticamente na primeira execução.
- É necessário ter o ficheiro LOG.py com a função registar_erro para registo de erros.
- Este projeto é para fins didáticos e pode ser adaptado para ambientes reais

---
# [EN] Scheduling appointments with a beautician 💅 - Python and SQLite  
**Author**: Roxanne Coelho  

### Description  
This project is a **Python** application integrated with **SQLite** to manage beauty session appointments.  
It allows:  
- Client registration  
- Management of available services  
- Scheduling, cancellation, and rescheduling of appointments  
- Viewing existing appointments  

The system runs in **console mode** and uses an interactive menu so clients can access their area, check services, and manage their appointments.  

---  

### Technologies Used  
- Python 3  
- SQLite3 (local database)  
- *datetime* module (for date and time validation)  

---  

### Project Structure  
```plaintext
 📦 scheduling-appointments-with-a-beautician
┣ 📜 trabalho final de python estética.py           # Main application code
┣ 📜 LOG.py                                         # Error logging functions (referenced in code)
┣ 📜 estetica.db                                    # SQLite database (auto-generated)
┗ 📜 README.md                                      # Project documentation
```

### Installation and Use
1. Clone the repository
```bash
https://github.com/RoxanneJCoelho/scheduling-appointments-with-a-beautician.git
```

2. Access the project folder
```bash
cd scheduling-appointments-with-a-beautician
```

3. Run the program
```bash
python "trabalho final de python estética.py"
```

---

### Notes
- The database (estetica.db) is created automatically on the first run.
- You must have the LOG.py file with the registar_erro function for error logging.
- This project is for educational purposes and can be adapted to real environments.

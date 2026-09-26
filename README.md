# ⚡ Monitor de Recursos do Sistema (Python + GUI Moderna)

Um painel de controle estilo "dashboard" que monitora CPU, Memória RAM e Disco em tempo real.
Projeto criado para demonstrar como criar interfaces modernas com Python e converter para `.exe`.

## 🛠️ Tecnologias Usadas

*   **Python 3.x**
*   **CustomTkinter**: Para a interface gráfica moderna (Modo Escuro nativo).
*   **Psutil**: Para capturar métricas do hardware (CPU, Memória, Disco).
*   **PyInstaller** ou **Nuitka**: Para transformar o script em um executável standalone.

## 🚀 Como Rodar o Projeto

### 1. Clone o repositório
```bash
git clone https://github.com/leandrohirt-dev/converter_para_exe.git
cd converter_para_exe
```

### 2. Crie um ambiente virtual (Recomendado)
Para não misturar as bibliotecas com seu Python global:

```bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 3. Instale as dependências
```bash
pip install -r requirements.txt
```

### 4. Execute o programa
```bash
python main.py
```

---

## 📦 Como Gerar o Executável (.exe)

Você tem duas opções excelentes para criar o executável: **PyInstaller** (mais famoso) ou **Nuitka** (mais otimizado).

### Opção A: Usando PyInstaller
Rápido e fácil, gera um executável padrão.

1.  Certifique-se de que o **ambiente virtual está ativado**.
2.  Rode o comando:

```bash
pyinstaller --noconsole --onefile main.py
```
*   O arquivo final estará na pasta **`dist`**.

### Opção B: Usando Nuitka (Recomendado para performance)
O Nuitka compila o Python para C, o que pode deixar o programa mais rápido e difícil de fazer engenharia reversa.

1.  Certifique-se de que o **ambiente virtual está ativado**.
2.  Rode o comando:

```bash
nuitka --onefile --enable-plugin=tk-inter --windows-console-mode=disable main.py
```

*   `--onefile`: Gera um único arquivo `.exe`.
*   `--enable-plugin=tk-inter`: Garante que a interface gráfica funcione corretamente.
*   `--windows-console-mode=disable`: Remove a janela preta do terminal.

3.  O executável será gerado na **raiz do projeto** ou na pasta de saída (dependendo da versão).
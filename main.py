"""
Monitor de Recursos do Sistema
Monitora CPU, Memória RAM e Disco com uma interface moderna.
"""

import customtkinter as ctk
import psutil
import platform
import time
from datetime import datetime


# Configuração do tema
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# Cores do Dashboard
CORES = {
    "fundo_escuro": "#0d1117",
    "fundo_card": "#161b22",
    "borda_card": "#30363d",
    "texto_principal": "#e6edf3",
    "texto_secundario": "#8b949e",
    "destaque_ciano": "#58a6ff",
    "destaque_verde": "#3fb950",
    "destaque_amarelo": "#d29922",
    "destaque_vermelho": "#f85149",
    "destaque_roxo": "#bc8cff",
    "trilha_barra": "#21262d",
}


def cor_por_valor(valor: float) -> str:
    """Retorna a cor baseada na porcentagem de uso."""
    if valor < 50:
        return CORES["destaque_verde"]
    elif valor < 75:
        return CORES["destaque_amarelo"]
    elif valor < 90:
        return CORES["destaque_vermelho"]
    else:
        return "#ff4040"


class WidgetMedidor(ctk.CTkFrame):
    """Widget estilizado que mostra a porcentagem em barra + texto."""

    def __init__(self, master, titulo: str, icone: str, cor_destaque: str, **kwargs):
        super().__init__(master, fg_color=CORES["fundo_card"], corner_radius=16, **kwargs)

        self.titulo = titulo
        self.cor_destaque = cor_destaque

        # Cabeçalho do card
        cabecalho = ctk.CTkFrame(self, fg_color="transparent")
        cabecalho.pack(fill="x", padx=20, pady=(18, 5))

        ctk.CTkLabel(
            cabecalho,
            text=icone,
            font=ctk.CTkFont(size=22),
            text_color=cor_destaque,
        ).pack(side="left")

        ctk.CTkLabel(
            cabecalho,
            text=f"  {titulo}",
            font=ctk.CTkFont(family="Segoe UI", size=15, weight="bold"),
            text_color=CORES["texto_principal"],
        ).pack(side="left")

        # Valor principal
        self.rotulo_valor = ctk.CTkLabel(
            self,
            text="0 %",
            font=ctk.CTkFont(family="Consolas", size=42, weight="bold"),
            text_color=cor_destaque,
        )
        self.rotulo_valor.pack(pady=(5, 2))

        # Barra de progresso
        self.progresso = ctk.CTkProgressBar(
            self,
            width=220,
            height=14,
            corner_radius=7,
            progress_color=cor_destaque,
            fg_color=CORES["trilha_barra"],
        )
        self.progresso.pack(pady=(0, 5))
        self.progresso.set(0)

        # Detalhes extras
        self.rotulo_detalhe = ctk.CTkLabel(
            self,
            text="",
            font=ctk.CTkFont(family="Segoe UI", size=12),
            text_color=CORES["texto_secundario"],
        )
        self.rotulo_detalhe.pack(pady=(0, 18))

    def atualizar_valor(self, porcentagem: float, detalhe: str = ""):
        """Atualiza o medidor com novo valor e detalhes."""
        cor = cor_por_valor(porcentagem)
        self.rotulo_valor.configure(text=f"{porcentagem:.1f} %", text_color=cor)
        self.progresso.configure(progress_color=cor)
        self.progresso.set(porcentagem / 100)
        if detalhe:
            self.rotulo_detalhe.configure(text=detalhe)


class CardInfo(ctk.CTkFrame):
    """Card simples para informações do sistema."""

    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color=CORES["fundo_card"], corner_radius=16, **kwargs)
        self.rotulos: dict[str, ctk.CTkLabel] = {}

    def adicionar_linha(self, chave: str, texto_rotulo: str, texto_valor: str = ""):
        linha = ctk.CTkFrame(self, fg_color="transparent")
        linha.pack(fill="x", padx=20, pady=3)

        ctk.CTkLabel(
            linha,
            text=texto_rotulo,
            font=ctk.CTkFont(family="Segoe UI", size=12),
            text_color=CORES["texto_secundario"],
            anchor="w",
        ).pack(side="left")

        valor = ctk.CTkLabel(
            linha,
            text=texto_valor,
            font=ctk.CTkFont(family="Consolas", size=12, weight="bold"),
            text_color=CORES["texto_principal"],
            anchor="e",
        )
        valor.pack(side="right")
        self.rotulos[chave] = valor

    def definir_valor(self, chave: str, texto: str):
        if chave in self.rotulos:
            self.rotulos[chave].configure(text=texto)


def formatar_bytes(b: float) -> str:
    """Formata bytes para uma unidade legível."""
    for unidade in ("B", "KB", "MB", "GB", "TB"):
        if b < 1024:
            return f"{b:.1f} {unidade}"
        b /= 1024
    return f"{b:.1f} PB"


class Aplicacao(ctk.CTk):
    """Janela principal do Monitor de Recursos."""

    def __init__(self):
        super().__init__()

        # Configuração da janela
        self.title("⚡ Monitor do Sistema - Dashboard")
        self.geometry("820x620")
        self.minsize(780, 580)
        self.configure(fg_color=CORES["fundo_escuro"])

        self._construir_interface()
        self._loop_atualizacao()

    def _construir_interface(self):
        # Barra superior
        barra_topo = ctk.CTkFrame(self, fg_color="transparent", height=50)
        barra_topo.pack(fill="x", padx=24, pady=(18, 0))

        ctk.CTkLabel(
            barra_topo,
            text="⚡  MONITOR DO SISTEMA",
            font=ctk.CTkFont(family="Segoe UI", size=20, weight="bold"),
            text_color=CORES["destaque_ciano"],
        ).pack(side="left")

        self.rotulo_relogio = ctk.CTkLabel(
            barra_topo,
            text="",
            font=ctk.CTkFont(family="Consolas", size=14),
            text_color=CORES["texto_secundario"],
        )
        self.rotulo_relogio.pack(side="right")

        # Container dos medidores (CPU, RAM, DISCO)
        quadro_medidores = ctk.CTkFrame(self, fg_color="transparent")
        quadro_medidores.pack(fill="x", padx=24, pady=(18, 0))
        quadro_medidores.columnconfigure((0, 1, 2), weight=1, uniform="medidor")

        self.medidor_cpu = WidgetMedidor(
            quadro_medidores, "CPU", "🔲", CORES["destaque_ciano"]
        )
        self.medidor_cpu.grid(row=0, column=0, padx=(0, 8), sticky="nsew")

        self.medidor_ram = WidgetMedidor(
            quadro_medidores, "MEMÓRIA", "💾", CORES["destaque_roxo"]
        )
        self.medidor_ram.grid(row=0, column=1, padx=8, sticky="nsew")

        self.medidor_disco = WidgetMedidor(
            quadro_medidores, "DISCO", "📀", CORES["destaque_verde"]
        )
        self.medidor_disco.grid(row=0, column=2, padx=(8, 0), sticky="nsew")

        # Titulo da seção de informações
        rotulo_info = ctk.CTkLabel(
            self,
            text="📋  INFORMAÇÕES DO SISTEMA",
            font=ctk.CTkFont(family="Segoe UI", size=14, weight="bold"),
            text_color=CORES["texto_secundario"],
            anchor="w",
        )
        rotulo_info.pack(fill="x", padx=28, pady=(22, 6))

        # Card de informações do sistema
        self.card_info = CardInfo(self)
        self.card_info.pack(fill="x", padx=24, pady=(0, 8))

        info_sistema = platform.uname()
        self.card_info.adicionar_linha("so", "Sistema Operacional", f"{info_sistema.system} {info_sistema.release}")
        self.card_info.adicionar_linha("maquina", "Máquina", info_sistema.node)
        self.card_info.adicionar_linha("processador", "Processador", info_sistema.processor or "N/A")
        self.card_info.adicionar_linha("nucleos", "Núcleos (lóg / fís)", f"{psutil.cpu_count()} / {psutil.cpu_count(logical=False)}")
        self.card_info.adicionar_linha("ram_total", "RAM Total", formatar_bytes(psutil.virtual_memory().total))
        self.card_info.adicionar_linha("tempo_ligado", "Tempo ligado", "")

        # Rodapé
        ctk.CTkLabel(
            self,
            text="Feito com Python 🐍 + CustomTkinter",
            font=ctk.CTkFont(size=11),
            text_color=CORES["texto_secundario"],
        ).pack(side="bottom", pady=(0, 12))

    def _loop_atualizacao(self):
        # CPU
        porcentagem_cpu = psutil.cpu_percent(interval=0)
        frequencia = psutil.cpu_freq()
        texto_freq = f"{frequencia.current:.0f} MHz" if frequencia else "N/A"
        self.medidor_cpu.atualizar_valor(porcentagem_cpu, f"Frequência: {texto_freq}")

        # RAM
        memoria = psutil.virtual_memory()
        detalhe_ram = f"{formatar_bytes(memoria.used)}  /  {formatar_bytes(memoria.total)}"
        self.medidor_ram.atualizar_valor(memoria.percent, detalhe_ram)

        # Disco
        disco = psutil.disk_usage("/")
        detalhe_disco = f"{formatar_bytes(disco.used)}  /  {formatar_bytes(disco.total)}"
        self.medidor_disco.atualizar_valor(disco.percent, detalhe_disco)

        # Relógio
        self.rotulo_relogio.configure(text=datetime.now().strftime("%H:%M:%S"))

        # Tempo ligado
        inicio_sistema = psutil.boot_time()
        segundos_ligado = time.time() - inicio_sistema
        horas, resto = divmod(int(segundos_ligado), 3600)
        minutos, segundos = divmod(resto, 60)
        self.card_info.definir_valor("tempo_ligado", f"{horas}h {minutos}m {segundos}s")

        # Repetir a cada 1 segundo
        self.after(1000, self._loop_atualizacao)


# Ponto de entrada
if __name__ == "__main__":
    app = Aplicacao()
    app.mainloop()

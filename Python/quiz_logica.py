import sys
import os
from PyQt5 import QtCore, uic
from PyQt5.QtGui import QPixmap, QFont, QColor
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QMessageBox, QLabel, QGraphicsDropShadowEffect,
    QTableWidget, QTableWidgetItem, QHeaderView
)
from PyQt5.QtCore import QTimer

from quiz_logica import QuizLogic
import styles


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(BASE_DIR)
IMAGENS_DIR = os.path.join(PROJECT_ROOT, "imagens")
QTDESIGNER_DIR = os.path.join(PROJECT_ROOT, "Qtdesigner")

class QuizApp(QMainWindow):
    TEMPO_POR_PERGUNTA = 30  

    def __init__(self):
        super().__init__()
        
        ui_path = os.path.join(QTDESIGNER_DIR, "quiz.ui")
        uic.loadUi(ui_path, self)
        
        self.logic = QuizLogic()
        self.botoes_opcoes = [self.btn_opcao1, self.btn_opcao2, self.btn_opcao3, self.btn_opcao4]
        
        self.setWindowTitle("Quiz de Futebol")
        self.aplicar_estilos_e_textos()
        self.conectar_sinais()
        self.setup_cronometro()
        self.setup_menu_background()
        self.setup_placar_table()
        
        self.stackedWidget.setCurrentWidget(self.menu_page)
        shadow_effect = QGraphicsDropShadowEffect(blurRadius=8, xOffset=4, yOffset=4, color=QColor(0,0,0,160))
        self.title_menu.setGraphicsEffect(shadow_effect)

    def setup_cronometro(self):
        self.tempo_restante = 0
        self.cronometro = QTimer(self)
        self.cronometro.timeout.connect(self.atualizar_cronometro)

    def setup_menu_background(self):
        self.background_label_menu = QLabel(self.menu_page)
        pixmap_path = os.path.join(IMAGENS_DIR, "campo.jpg")
        if os.path.exists(pixmap_path):
            pixmap = QPixmap(pixmap_path)
            self.background_label_menu.setPixmap(pixmap)
        self.background_label_menu.setScaledContents(True)
        self.background_label_menu.lower()
        
    def setup_placar_table(self):
        self.placar_table.setColumnCount(3)
        self.placar_table.setHorizontalHeaderLabels(["Posição", "Nome", "Pontuação"])
        self.placar_table.verticalHeader().setVisible(False)
        self.placar_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.placar_table.setAlternatingRowColors(True) 
        self.placar_table.setStyleSheet(self.placar_table.styleSheet() + "QTableWidget::item { padding: 5px; } QTableView::item:alternate { background-color: #1a2f38; }")
        
        header = self.placar_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.Stretch)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)

       
        header.setStyleSheet("QHeaderView::section { color: white; background-color: #1a2f38; font-size: 16pt; font-weight: bold; }")

    def resizeEvent(self, event):
        super().resizeEvent(event)
        if hasattr(self, 'background_label_menu'):
            self.background_label_menu.resize(self.size())

    def aplicar_estilos_e_textos(self):
        botoes_padrao = [
            self.btn_jogar, self.btn_instrucoes, self.btn_placar_menu, 
            self.btn_facil, self.btn_medio, self.btn_dificil, 
            self.btn_ver_placar, self.btn_voltar_menu_instrucoes, 
            self.btn_voltar_menu_dificuldade, self.btn_voltar_menu_final, 
            self.btn_voltar_menu_placar
        ]
        for btn in botoes_padrao:
            btn.setFixedSize(350, 60)
            btn.setFont(QFont("Arial", 20, QFont.Bold))
            btn.setStyleSheet(styles.STYLE_PADRAO_BUTTON)

        for btn in self.botoes_opcoes:
            btn.setMinimumHeight(60)
            btn.setFont(QFont("Arial", 16, QFont.Bold))
            btn.setStyleSheet(styles.STYLE_OPTION_BUTTON)

        botoes_filtro_placar = [self.btn_placar_facil, self.btn_placar_medio, self.btn_placar_dificil]
        for btn in botoes_filtro_placar:
            btn.setMinimumHeight(45)
            btn.setFont(QFont("Arial", 14, QFont.Bold))
            btn.setStyleSheet(styles.STYLE_PLACAR_FILTER)
        
        self.btn_ajuda_5050.setText("50/50")
        self.btn_ajuda_5050.setFixedSize(100, 40)
        self.btn_ajuda_5050.setFont(QFont("Arial", 14, QFont.Bold))
        self.btn_ajuda_5050.setStyleSheet(styles.STYLE_AJUDA_5050)

        self.btn_jogar.setText("Jogar")
        self.btn_instrucoes.setText("Instruções")
        self.btn_placar_menu.setText("Placar de Líderes")
        self.btn_facil.setText("Fácil")
        self.btn_medio.setText("Médio")
        self.btn_dificil.setText("Difícil")
        self.btn_ver_placar.setText("Ver Placar de Líderes")
        self.btn_voltar_menu_instrucoes.setText("Voltar ao Menu")
        self.btn_voltar_menu_dificuldade.setText("Voltar ao Menu")
        self.btn_voltar_menu_final.setText("Voltar ao Menu")
        self.btn_voltar_menu_placar.setText("Voltar ao Menu")
        self.btn_placar_facil.setText("Fácil")
        self.btn_placar_medio.setText("Médio")
        self.btn_placar_dificil.setText("Difícil")

        self.nome_input.setPlaceholderText("Seu nome aqui")
        self.nome_input.setFixedSize(350, 50)
        self.nome_input.setFont(QFont("Arial", 16))
        self.nome_input.setStyleSheet("background-color: rgba(255, 255, 255, 0.9); border-radius: 10px; padding: 10px;")

    def conectar_sinais(self):
        self.btn_jogar.clicked.connect(lambda: self.switch_page(self.dificuldade_page))
        self.btn_instrucoes.clicked.connect(lambda: self.switch_page(self.instrucoes_page))
        self.btn_placar_menu.clicked.connect(lambda: self.mostrar_pontuacoes())

        self.btn_facil.clicked.connect(lambda: self.iniciar_quiz("facil"))
        self.btn_medio.clicked.connect(lambda: self.iniciar_quiz("medio"))
        self.btn_dificil.clicked.connect(lambda: self.iniciar_quiz("dificil"))
        
        self.btn_ver_placar.clicked.connect(lambda: self.mostrar_pontuacoes(self.logic.dificuldade_atual))
        self.btn_placar_facil.clicked.connect(lambda: self.atualizar_lista_placar("facil"))
        self.btn_placar_medio.clicked.connect(lambda: self.atualizar_lista_placar("medio"))
        self.btn_placar_dificil.clicked.connect(lambda: self.atualizar_lista_placar("dificil"))

        self.btn_voltar_menu_final.clicked.connect(self.voltar_ao_menu)
        self.btn_voltar_menu_placar.clicked.connect(self.voltar_ao_menu)
        self.btn_voltar_menu_instrucoes.clicked.connect(self.voltar_ao_menu)
        self.btn_voltar_menu_dificuldade.clicked.connect(self.voltar_ao_menu)
        
        for botao in self.botoes_opcoes:
            botao.clicked.connect(self.verificar_resposta)
        
        self.btn_ajuda_5050.clicked.connect(self.usar_ajuda_5050)

    def switch_page(self, page):
        self.stackedWidget.setCurrentWidget(page)

    def iniciar_quiz(self, dificuldade):
        nome_jogador = self.nome_input.text()
        if not nome_jogador:
            QMessageBox.warning(self, "Erro", "Digite seu nome.")
            return

        if self.logic.iniciar_quiz(dificuldade, nome_jogador):
            self.switch_page(self.quiz_page)
            self.carregar_pergunta()
        else:
            QMessageBox.warning(self, "Erro", f"Nenhuma pergunta encontrada para a dificuldade '{dificuldade}'.")

    def carregar_pergunta(self):
        if not self.logic.tem_proxima_pergunta():
            self.finalizar_quiz()
            return

        pergunta = self.logic.obter_pergunta_atual()
        
        if self.logic.ajudas_5050 > 0:
            self.btn_ajuda_5050.setVisible(True)
            self.btn_ajuda_5050.setEnabled(True)
        else:
            self.btn_ajuda_5050.setVisible(False)

        self.label_feedback.setText("")
        self.label_progresso.setText(f"Pergunta: {self.logic.indice_pergunta + 1}/{len(self.logic.perguntas_do_quiz)}")
        self.label_streak.setText(f"🔥 Sequência: {self.logic.streak_atual}")
        self.label_streak.setStyleSheet(styles.STYLE_STREAK_RESETADO)
        self.label_pergunta_titulo.setText(pergunta["texto"])
        
        img_filename = os.path.basename(pergunta["imagem"])
        img_path = os.path.join(IMAGENS_DIR, img_filename)

        if os.path.exists(img_path):
            self.label_imagem.setPixmap(QPixmap(img_path).scaled(500, 250, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation))
        else:
            self.label_imagem.setText("Imagem não encontrada")
            
        for i, opcao_texto in enumerate(pergunta["opcoes"]):
            self.botoes_opcoes[i].setText(opcao_texto)
            self.botoes_opcoes[i].setEnabled(True)
            self.botoes_opcoes[i].setStyleSheet(styles.STYLE_OPTION_BUTTON)
            
        self.label_pontuacao.setText(f"Pontuação: {self.logic.pontuacao}")
        
        self.tempo_restante = self.TEMPO_POR_PERGUNTA
        self.label_cronometro.setText(f"Tempo: {self.tempo_restante}")
        self.cronometro.start(1000)

    def verificar_resposta(self):
        self.cronometro.stop()
        self.btn_ajuda_5050.setEnabled(False)
        
        sender_btn = self.sender()
        foi_correto, resposta_certa, bonus = self.logic.verificar_resposta(sender_btn.text())

        for btn in self.botoes_opcoes: 
            btn.setEnabled(False)

        if foi_correto:
            sender_btn.setStyleSheet(styles.STYLE_BOTAO_CORRETO)
            self.label_feedback.setText("Correto!")
            self.label_feedback.setStyleSheet(styles.STYLE_FEEDBACK_CORRETO)
            
            self.label_streak.setText(f"🔥 Sequência: {self.logic.streak_atual}")
            self.label_streak.setStyleSheet(styles.STYLE_STREAK_ATIVO)

            if bonus > 0:
                self.label_feedback.setText(f"BÔNUS DE SEQUÊNCIA! +{bonus} Pontos!")
                self.label_feedback.setStyleSheet(styles.STYLE_FEEDBACK_BONUS)
        else:
            sender_btn.setStyleSheet(styles.STYLE_BOTAO_INCORRETO)
            self.label_feedback.setText("Incorreto!")
            self.label_feedback.setStyleSheet(styles.STYLE_FEEDBACK_INCORRETO)
            self.label_streak.setText("🔥 Sequência: 0")
            self.label_streak.setStyleSheet(styles.STYLE_STREAK_RESETADO)
            for btn in self.botoes_opcoes:
                if btn.text() == resposta_certa:
                    btn.setStyleSheet(styles.STYLE_BOTAO_CORRETO)
        
        self.label_pontuacao.setText(f"Pontuação: {self.logic.pontuacao}")
        QTimer.singleShot(1500, self.proxima_pergunta)

    def proxima_pergunta(self):
        self.logic.avancar_pergunta()
        self.carregar_pergunta()

    def usar_ajuda_5050(self):
        opcoes_para_remover = self.logic.usar_ajuda_5050()
        if opcoes_para_remover:
            for btn in self.botoes_opcoes:
                if btn.text() in opcoes_para_remover:
                    btn.setEnabled(False)
                    btn.setStyleSheet(styles.STYLE_BOTAO_DESABILITADO_5050)
            self.btn_ajuda_5050.setVisible(False)

    def atualizar_cronometro(self):
        self.tempo_restante -= 1
        self.label_cronometro.setText(f"Tempo: {self.tempo_restante}")
        if self.tempo_restante <= 0:
            self.cronometro.stop()
            self.tempo_esgotado()

    def tempo_esgotado(self):
        self.label_feedback.setText("Tempo Esgotado!")
        self.label_feedback.setStyleSheet(styles.STYLE_FEEDBACK_INCORRETO)
        
        self.logic.streak_atual = 0
        self.label_streak.setText("🔥 Sequência: 0")
        self.label_streak.setStyleSheet(styles.STYLE_STREAK_RESETADO)

        resposta_correta = self.logic.perguntas_do_quiz[self.logic.indice_pergunta]["correta"]
        for btn in self.botoes_opcoes:
            btn.setEnabled(False)
            if btn.text() == resposta_correta:
                btn.setStyleSheet(styles.STYLE_BOTAO_CORRETO)
        
        QTimer.singleShot(1500, self.proxima_pergunta)
        
    def finalizar_quiz(self):
        self.cronometro.stop()
        self.score_label.setText(f"Parabéns, {self.logic.nome_jogador}! Sua pontuação final foi: {self.logic.pontuacao}")
        self.logic.salvar_pontuacao()
        self.switch_page(self.final_page)
    
    def mostrar_pontuacoes(self, dificuldade="facil"):
        self.switch_page(self.placar_page)
        self.atualizar_lista_placar(dificuldade)

    def atualizar_lista_placar(self, dificuldade):
        botoes_placar = {
            "facil": self.btn_placar_facil,
            "medio": self.btn_placar_medio,
            "dificil": self.btn_placar_dificil
        }
        for dif, btn in botoes_placar.items():
            if dif == dificuldade:
                btn.setStyleSheet(styles.STYLE_PLACAR_SELECIONADO)
            else:
                btn.setStyleSheet(styles.STYLE_PLACAR_FILTER)
        
        placar_ordenado = self.logic.obter_placar(dificuldade)
        self.placar_table.setRowCount(0)

        if not placar_ordenado:
            self.placar_table.setRowCount(1)
            msg_item = QTableWidgetItem(f"Nenhuma pontuação na dificuldade '{dificuldade.capitalize()}'.")
            msg_item.setTextAlignment(QtCore.Qt.AlignCenter)
            self.placar_table.setSpan(0, 0, 1, 3)
            self.placar_table.setItem(0, 0, msg_item)
        else:
            self.placar_table.setRowCount(len(placar_ordenado))
            medalhas = ["🏆", "🥈", "🥉"]
            for i, entrada in enumerate(placar_ordenado[:15]): 
                prefixo = medalhas[i] if i < 3 else f"{i+1}º"
                
                pos_item = QTableWidgetItem(prefixo)
                pos_item.setForeground(QColor("gold"))
                pos_item.setFont(QFont("Arial", 14))

                nome_item = QTableWidgetItem(entrada['nome'])
                nome_item.setForeground(QColor("white"))
                nome_item.setFont(QFont("Arial", 14))

                pontuacao_item = QTableWidgetItem(str(entrada['pontuacao']))
                pontuacao_item.setForeground(QColor("#00ff88"))
                pontuacao_item.setFont(QFont("Arial", 14, QFont.Bold))
                
                
                pos_item.setTextAlignment(QtCore.Qt.AlignCenter)
                nome_item.setTextAlignment(QtCore.Qt.AlignCenter) 
                pontuacao_item.setTextAlignment(QtCore.Qt.AlignCenter)
                
                self.placar_table.setItem(i, 0, pos_item)
                self.placar_table.setItem(i, 1, nome_item)
                self.placar_table.setItem(i, 2, pontuacao_item)
    
    def voltar_ao_menu(self):
        self.nome_input.clear()
        self.switch_page(self.menu_page)

if __name__ == "__main__": 
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    janela = QuizApp()
    janela.show()
    sys.exit(app.exec_())
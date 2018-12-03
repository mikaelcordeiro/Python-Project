from numpy import *
import matplotlib.pyplot as plt
import sys
import webbrowser
import tkinter as tk
import tkinter.messagebox as message
import tkinter.filedialog as filedialog
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import algoritmo_osc as alg

# =======================================================================

class PlotaGrafico_GUI:
    
    ''' Classe GUI para plotar as soluções da
    equação do Oscilador de van der Pol e que
    contém um painel lateral com controles e
    uma barra de menu diversas funções
    '''
    
    def __init__(self):
        ''' função de inicialização'''
        
        self.Monta_GUI()
            
    def __call__(self, f =1, xmin = 0, xmax = 0.5, ymin = 0, ymax = 25.133, N = 500, cor = 'Azul'):
        '''
            método especial para abrir a janela 
        '''
        
				# chama a função de inicialização da janela
        self.Inicia_GUI(f, float(xmin), float(xmax), float(ymin), float(ymax), N, cor)
				# abre a janela
        self.root.mainloop()
    
    def Monta_GUI(self):
        
        ##########
        # Janela principal
        
        root = tk.Tk()
        root.title('Solução da equação do oscilador de van der Pol')
        
        
        ##########
        # Barra de menu
        
        # barra principal
        menubar = tk.Menu(root)

        # cria um pulldown menu na barra principal
        filemenu = tk.Menu(menubar, tearoff=0)
        # adicionando comandos
        filemenu.add_command(label="Abrir...", command=self.AbreArquivo)
        filemenu.add_command(label="Salvar", command=self.Salva)
        filemenu.add_command(label="Salvar como...", command=self.SalvaComo)
        filemenu.add_separator()
        filemenu.add_command(label="Sair", command=self.Destroy)
        # adicionando o menu à barra
        menubar.add_cascade(label="Arquivo", menu=filemenu)
        
        # cria um pulldown menu na barra principal
        figmenu = tk.Menu(menubar, tearoff=0)
        # adicionando comandos
        figmenu.add_command(label="Atualizar", command=self.Plot)
        figmenu.add_command(label="Exportar...", command=self.SalvaVet)
        # adicionando o menu à barra
        menubar.add_cascade(label="Figura", menu=figmenu)
        
        # cria outro menu
        helpmenu = tk.Menu(menubar, tearoff=0)
        # adicionando comandos
        helpmenu.add_command(label="Manual...", command=self.Help)
        helpmenu.add_command(label="Manual Online...", command= self.Github)
        helpmenu.add_command(label="Sobre...", command=self.About)
        # adicionando o menu à barra
        menubar.add_cascade(label="Help", menu=helpmenu)

        # adicionando a barra à janela
        root.config(menu=menubar)
        
        
        ##########
        # Organizando a janela
        
        # Frame superior que vai conter Controles + Gráfico 1
        FRAME_UP = tk.Frame()
        FRAME_UP.pack(side = 'left', fill = 'y')
        
        # Frame inferior que vai conter Gráfico 2 + Gráfico 3
        FRAME_DOWN = tk.Frame()
        FRAME_DOWN.pack(side = 'right')
        
        
        ##########
        # Controles
        
        f_frame = tk.Frame(FRAME_UP)
        f_frame.pack()
        
        controles_text = tk.Label(f_frame, text='Área de controle')
        controles_text.pack()
        
        # Constante do Oscilador 
        
        e_frame = tk.Frame(f_frame)
        e_frame.pack()
        
        f_text = tk.Label(e_frame, text='e: ')
        f_text.pack(side='left')
        
        self.f_var = tk.StringVar()
        f_entry = tk.Entry(e_frame, textvariable=self.f_var)
        f_entry.pack()
        
        # limites
        
        xlim_frame = tk.Frame(f_frame)
        xlim_frame.pack()
        
        xmin_text = tk.Label(xlim_frame, text="x(0): ")
        xmin_text.pack(side='left')
        
        self.xmin_var = tk.StringVar()
        xmin_entry = tk.Entry(xlim_frame, textvariable=self.xmin_var, width=5)
        xmin_entry.pack(side='left')
        
        xmax_text = tk.Label(xlim_frame, text="x'(0): ")
        xmax_text.pack(side='left')
        
        self.xmax_var = tk.StringVar()
        xmax_entry = tk.Entry(xlim_frame, textvariable=self.xmax_var, width=5)
        xmax_entry.pack(side='left')
        
        # 
        
        ylim_frame = tk.Frame(f_frame)
        ylim_frame.pack()
        
        ymin_text = tk.Label(ylim_frame, text='tmin: ')
        ymin_text.pack(side='left')
        
        self.ymin_var = tk.StringVar()
        ymin_entry = tk.Entry(ylim_frame, textvariable=self.ymin_var, width=5)
        ymin_entry.pack(side='left')
        
        ymax_text = tk.Label(ylim_frame, text='tmax: ')
        ymax_text.pack(side='left')
        
        self.ymax_var = tk.StringVar()
        ymax_entry = tk.Entry(ylim_frame, textvariable=self.ymax_var, width=5)
        ymax_entry.pack(side='left')
        
        # no. de pontos
        
        N_frame = tk.Frame(f_frame)
        N_frame.pack()
        
        N_text = tk.Label(N_frame, text='nº de pontos: ')
        N_text.pack(side='left')
        
        self.N_var = tk.IntVar()
        N_entry = tk.Entry(N_frame, textvariable=self.N_var, width=5)
        N_entry.pack(side='left')
        
        # cor do gráfico
        
        cor_frame = tk.Frame(f_frame, relief='sunken', borderwidth=1)
        cor_frame.pack()
        
        cor_text = tk.Label(cor_frame, text='Cor da linha:')
        cor_text.pack()
        
        self.cores = {'Vermelho':'r', 'Azul':'b', 'Verde':'g', 'Preto':'k'}
        
        self.cor = tk.StringVar()
        for opt in self.cores:
            cor_opt = tk.Radiobutton(cor_frame, text=opt, variable=self.cor, value=self.cores[opt], command=self.MudaCor)
            cor_opt.pack(anchor='w')
        
        
        ##########
        # Botões
        
        # frame
        bts_frame = tk.Frame(f_frame)
        bts_frame.pack(side='bottom')
        
        # botão para atualizar o gráfico
        plot_bt = tk.Button(bts_frame, text='Atualizar', command=self.Plot)
        plot_bt.pack(side='left')

        # botão para exportar o gráfico como figura
        salva_bt = tk.Button(bts_frame, text='Exportar...', command=self.SalvaVet)
        salva_bt.pack(side='left')

        # botão para sair
        quit_bt = tk.Button(bts_frame, text='Sair', command=self.Destroy)
        quit_bt.pack(side='left')
        
        
        ##########
        # Gráfico
      
        # Gráfico 1
        # objeto gráfico
        self.fig_1 = plt.figure()
        self.ax_1 = plt.axes()
        plt.title('Gráfico de x(t) vs. t')
        self.line_1, =  self.ax_1.plot([], [])

        # frame
        grafico1_frame = tk.Frame(FRAME_DOWN)
        grafico1_frame.pack()

        # canvas
        canvas1 = FigureCanvasTkAgg(self.fig_1, master=grafico1_frame)
        canvas1.get_tk_widget().pack()
        
        # Gráfico 2
        # objeto gráfico
        self.fig_2 = plt.figure()
        self.ax_2 = plt.axes()
        plt.title("Gráfico de x'(t) vs. t")
        self.line_2, =  plt.plot([],[])

        # frame
        grafico2_frame = tk.Frame(FRAME_UP)
        grafico2_frame.pack(side = 'bottom')

        # canvas
        canvas2 = FigureCanvasTkAgg(self.fig_2, master=grafico2_frame)
        canvas2.get_tk_widget().pack()
        
        # Gráfico 3
        # objeto gráfico
        self.fig_3 = plt.figure()
        self.ax_3 = plt.axes()
        plt.title("Gráfico de x'(t) vs. x(t)")
        self.line_3, =  plt.plot([], [])

        # frame
        grafico3_frame = tk.Frame(FRAME_DOWN)
        grafico3_frame.pack()

        # canvas
        canvas3 = FigureCanvasTkAgg(self.fig_3, master=grafico3_frame)
        canvas3.get_tk_widget().pack()
        
                
        ##########
        # Geometria
        
        root.withdraw() # minimiza temporariamente a janela
        root.update_idletasks() # atualiza propriedades
        
        L = root.winfo_reqwidth()            # largura da janela
        A = root.winfo_reqheight()           # altura da janela
        LT = root.winfo_screenwidth()        # largura da tela
        AT = root.winfo_screenheight()       # altura da tela
        Px = int( ( LT - L ) // 2 )           # posição horizontal do canto superior esquerdo
        Py = int( ( AT - A ) // 2 )           # posição vertical do canto superior esquerdo
        root.geometry('+%d+%d' % (Px, Py))   # ajustando a posição da janela
        root.resizable(True, False)         # só permite ao usuário modificar o tamanho horizontal da janela
        
        root.deiconify()                     # retorna a janela após ajustar sua posição 
        
        ##########
        # Propriedades e keybindings

        # roda a função self.Destroy ao clicar no botão 'x'
        root.protocol("WM_DELETE_WINDOW", self.Destroy)
        
        # Atualiza o grafico automaticamente ao perder o foco
        # as funções usadas não aceitam argumentos, então usei lambda pra isso
        f_entry.bind("<FocusOut>", lambda event: self.Plot())
        xmin_entry.bind("<FocusOut>", lambda event: self.Plot())
        xmax_entry.bind("<FocusOut>", lambda event: self.Plot())
        ymin_entry.bind("<FocusOut>", lambda event: self.Plot())
        ymax_entry.bind("<FocusOut>", lambda event: self.Plot())
        N_entry.bind("<FocusOut>", lambda event: self.Plot())
        # Atualiza o grafico automaticamente ao pressionar Enter
        f_entry.bind("<Return>", lambda event: self.Plot())
        xmin_entry.bind("<Return>", lambda event: self.Plot())
        xmax_entry.bind("<Return>", lambda event: self.Plot())
        ymin_entry.bind("<Return>", lambda event: self.Plot())
        ymax_entry.bind("<Return>", lambda event: self.Plot())
        N_entry.bind("<Return>", lambda event: self.Plot())
        # Atualiza o grafico automaticamente ao pressionar Enter do keypad
        f_entry.bind("<KP_Enter>", lambda event: self.Plot())
        xmin_entry.bind("<KP_Enter>", lambda event: self.Plot())
        xmax_entry.bind("<KP_Enter>", lambda event: self.Plot())
        ymin_entry.bind("<KP_Enter>", lambda event: self.Plot())
        ymax_entry.bind("<KP_Enter>", lambda event: self.Plot())
        N_entry.bind("<KP_Enter>", lambda event: self.Plot())
        
        # Usa Control-s para salvar a figura
        root.bind("<Control-s>", lambda event: self.SalvaFig())
        
        # termina o programa ao pressionar ESC
        root.bind('<Escape>', lambda event: self.Destroy())
        
#        W = grafico3_frame.winfo_width()
#        f_frame['width'] = W
#        f_frame['fill'] = 'x'
        
        self.root = root # permite que outras funções acessem a página principal    
    
    ##########
    # Funções ligadas aos widgets
    
    def Inicia_GUI(self, f, xmin, xmax, ymin, ymax, N, cor):
        
        self.f_var.set(f)
        self.xmin_var.set(xmin)
        self.xmax_var.set(xmax)
        self.ymin_var.set(ymin)
        self.ymax_var.set(ymax)
        self.N_var.set(N)
        self.cor.set(self.cores[cor])
        self.line_1.set_color(self.cores[cor])
        self.line_2.set_color(self.cores[cor])
        self.line_3.set_color(self.cores[cor])
        self.Plot()
    
    def AbreArquivo(self):
        
        
        abre_arquivo = filedialog.askopenfilename(defaultextension = ".txt", initialdir = "./",title = "Importando parâmetros...")
        abre_arquivo = open("%s" %(abre_arquivo), "r")
        dados = []
        for linha in abre_arquivo:
            valores = linha.split()
            dados.append(valores[1])
        self.f_var.set(dados[0])
        self.xmin_var.set(dados[1])
        self.xmax_var.set(dados[2])
        self.ymin_var.set(dados[3])
        self.ymax_var.set(dados[4])
        self.N_var.set(dados[5])            
        abre_arquivo.close()
        
    
    def Salva(self):

        
        if self.sc == 1:
            salva_arquivo = open("%s" %(self.filename), "w")
            salva_arquivo.write('e: \t %f \n' %(self.E))
            salva_arquivo.write('x(0): \t %f \n' %(self.xmin))
            salva_arquivo.write("x'(0): \t %f \n" %(self.xmax))
            salva_arquivo.write('tmin: \t %f \n' %(self.ymin))
            salva_arquivo.write('tmax: \t %f \n' %(self.ymax))
            salva_arquivo.write('nº_de_pontos: \t %f \n' %(self.N))
            salva_arquivo.close()            
        
        
    def SalvaVet(self):
    
        filename = filedialog.asksaveasfilename(defaultextension = ".txt", initialdir = "./",title = "Exportando parâmetros...")
        if filename is not '' and filename is not ():
            salva_arquivo = open("%s" %(filename), "w")
            salva_arquivo.write('Espaço \t Velocidade \t Tempo \n')
            for i in range(len(self.s)):
                salva_arquivo.write('%f \t %f \t %f \n' %(self.s[i],self.v[i],self.t[i]))
        
    
    def SalvaComo(self):
        

        self.filename = filedialog.asksaveasfilename(defaultextension = ".txt", initialdir = "./",title = "Exportando parâmetros...")
        if self.filename is not '' and self.filename is not ():
            salva_arquivo = open("%s" %(self.filename), "w")
            salva_arquivo.write('e: \t %f \n' %(self.E))
            salva_arquivo.write('x(0): \t %f \n' %(self.xmin))
            salva_arquivo.write("x'(0): \t %f \n" %(self.xmax))
            salva_arquivo.write('tmin: \t %f \n' %(self.ymin))
            salva_arquivo.write('tmax: \t %f \n' %(self.ymax))
            salva_arquivo.write('nº_de_pontos: \t %f \n' %(self.N))
            salva_arquivo.close()
        self.sc=1
        return self.sc
    
    
    def Help(self):
        
        filename = 'manual.pdf'        
        webbrowser.open_new(filename)

    def About(self):
        
        about_text = '''
        
              van der Pol Oscilator Solver 0.1
        
              LOM3260 - Computação Científica em Python
        
              Engenharia Física!
        
              EEL-USP 2018
             '''
             
        message.showinfo('Info', about_text)
        
    def Github(self):
        webbrowser.open_new("https://github.com/mikaelcordeiro/Python-Project/blob/master/manual.pdf")
 
    
    def Plot(self):

        try:
            
            self.xmin, self.xmax = float(self.xmin_var.get()), float(self.xmax_var.get())
            self.ymin, self.ymax = float(self.ymin_var.get()), float(self.ymax_var.get())
            self.N = int(self.N_var.get())
            self.E = float(self.f_var.get())
            
        except(ValueError):
            
            message.showinfo('Erro!', 'Insira um número inteiro.')
        
        self.s,self.v,self.t = alg.oscilador_de_van_der_Pol(self.E,self.xmin,self.xmax,self.ymin,self.ymax,self.N)
        
        print(self.s,self.v,self.t)
        
        self.line_1.set_data(self.t,self.s)
        self.line_2.set_data(self.t,self.v)
        self.line_3.set_data(self.s,self.v)
    
        #self.ax_1.autoscale(enable=True, axis='both')
        self.ax_1.set_xlim(self.t.min(), self.t.max())
        self.ax_1.set_ylim(self.s.min(), self.s.max())
        
        self.ax_2.set_xlim(self.t.min(), self.t.max())
        self.ax_2.set_ylim(self.v.min(), self.v.max())
        
        self.ax_3.set_xlim(self.s.min(), self.s.max())
        self.ax_3.set_ylim(self.v.min(), self.v.max())
        
        self.fig_1.canvas.draw_idle()
        self.fig_2.canvas.draw_idle()
        self.fig_3.canvas.draw_idle()
        
    def MudaCor(self):
        
        cor = self.cor.get()
        self.line_1.set_color(cor)
        self.line_2.set_color(cor)
        self.line_3.set_color(cor)
        self.fig_1.canvas.draw_idle()
        self.fig_2.canvas.draw_idle()
        self.fig_3.canvas.draw_idle()
                
    def SalvaFig(self):
    
        formatos = ( ("formato png","*.png"), ('formato pdf', '*.pdf'), ("formato jpg","*.jpg") )
        filename = filedialog.asksaveasfilename(initialdir = "./",title = "Exportando a figura...",filetypes = formatos)
        if filename is not '' and filename is not ():
            plt.savefig(filename)
        
    def Destroy(self):
            
        y = message.askyesno('Sair', 'Deseja realmente sair? Você pode perder informações!')
        if y is True:
            self.root.quit()
            if 'win' in sys.platform: 
                self.root.destroy() # Precisa disso no Windows

# =======================================================================

# cria uma instância apenas se rodar diretamente este arquivo
# se for importado em outro código, não roda a não ser que o usuário crie uma instância                
if __name__ == '__main__':
    
        gui = PlotaGrafico_GUI() # cria a instância do objeto e roda a função __init__
        gui(ymin=0, ymax=26) # roda a função __call__

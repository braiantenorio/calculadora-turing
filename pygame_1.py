import pygame
import sys
from typing import Dict, Tuple, List

# Inicializar Pygame
pygame.init()

# Colores modernos
COLORS = {
    'bg': (15, 23, 42),           # Fondo oscuro
    'surface': (30, 41, 59),      # Superficie
    'primary': (59, 130, 246),    # Azul brillante
    'secondary': (139, 92, 246),  # Púrpura
    'success': (34, 197, 94),     # Verde
    'warning': (251, 146, 60),    # Naranja
    'text': (248, 250, 252),      # Texto claro
    'text_dim': (148, 163, 184),  # Texto dim
    'cell': (51, 65, 85),         # Celda
    'cell_active': (59, 130, 246),# Celda activa
    'cell_border': (71, 85, 105), # Borde celda
}

class MaquinaTuringVisual:
    def __init__(self, cinta_inicial: str, transiciones: Dict, estado_inicial: str, estado_final: str):
        self.width = 1400
        self.height = 900
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Máquina de Turing - Incrementador Binario")
        
        # Estado de la máquina
        self.cinta = list(cinta_inicial)
        self.transiciones = transiciones
        self.estado = estado_inicial
        self.estado_final = estado_final
        self.cabezal = 0
        self.pasos = 0
        self.historial = []
        
        # Control
        self.ejecutando = False
        self.velocidad = 500  # ms
        self.ultimo_paso = 0
        
        # UI
        self.fuente_grande = pygame.font.Font(None, 48)
        self.fuente_mediana = pygame.font.Font(None, 36)
        self.fuente_pequena = pygame.font.Font(None, 28)
        self.fuente_mono = pygame.font.Font(None, 40)
        
        # Botones
        self.botones = self.crear_botones()
        
        # Scroll para la cinta
        self.scroll_offset = 0
        
    def crear_botones(self) -> List[Dict]:
        y_base = self.height - 150
        botones = [
            {
                'rect': pygame.Rect(50, y_base, 180, 60),
                'texto': 'EJECUTAR',
                'color': COLORS['success'],
                'accion': 'toggle_run',
                'icono': ''
            },
            {
                'rect': pygame.Rect(250, y_base, 150, 60),
                'texto': 'PASO',
                'color': COLORS['primary'],
                'accion': 'step',
                'icono': ''
            },
            {
                'rect': pygame.Rect(420, y_base, 150, 60),
                'texto': 'RESET',
                'color': COLORS['warning'],
                'accion': 'reset',
                'icono': ''
            },
            {
                'rect': pygame.Rect(590, y_base, 80, 60),
                'texto': '+',
                'color': COLORS['secondary'],
                'accion': 'speed_up',
                'icono': ''
            },
            {
                'rect': pygame.Rect(690, y_base, 80, 60),
                'texto': '-',
                'color': COLORS['secondary'],
                'accion': 'speed_down',
                'icono': ''
            },
        ]
        return botones
    
    def paso(self) -> bool:
        """Ejecuta un paso de la máquina"""
        if self.estado == self.estado_final:
            self.ejecutando = False
            return False
        
        simbolo = self.cinta[self.cabezal]
        clave = (self.estado, simbolo)
        
        if clave not in self.transiciones:
            self.ejecutando = False
            return False
        
        # Guardar historial
        self.historial.append({
            'cinta': self.cinta.copy(),
            'cabezal': self.cabezal,
            'estado': self.estado
        })
        
        nuevo_estado, escribir, mover = self.transiciones[clave]
        
        # Escribir
        if escribir != 'n':
            self.cinta[self.cabezal] = escribir
        
        # Cambiar estado
        self.estado = nuevo_estado
        
        # Mover cabezal
        if mover == 'R':
            self.cabezal += 1
            if self.cabezal >= len(self.cinta):
                self.cinta.append(' ')
        elif mover == 'L':
            self.cabezal -= 1
            if self.cabezal < 0:
                self.cinta.insert(0, ' ')
                self.cabezal = 0
        
        self.pasos += 1
        
        # Auto-scroll para seguir el cabezal
        self.ajustar_scroll()
        
        return True
    
    def ajustar_scroll(self):
        """Ajusta el scroll para mantener el cabezal visible"""
        cell_width = 70
        visible_cells = 16
        pos_cabezal = self.cabezal - self.scroll_offset
        
        if pos_cabezal > visible_cells - 3:
            self.scroll_offset = self.cabezal - visible_cells + 3
        elif pos_cabezal < 2 and self.scroll_offset > 0:
            self.scroll_offset = max(0, self.cabezal - 2)
    
    def reset(self):
        self.cinta = ['1', '1', '1', ' ']
        self.cabezal = 0
        self.estado = 's0'
        self.pasos = 0
        self.historial = []
        self.ejecutando = False
        self.scroll_offset = 0
    
    def dibujar_cinta(self):
        cell_width = 70
        cell_height = 90
        start_x = 100
        start_y = 250
        
        # Título
        titulo = self.fuente_mediana.render("CINTA", True, COLORS['text_dim'])
        self.screen.blit(titulo, (start_x, start_y - 60))
        
        # Dibujar celdas visibles
        visible_cells = 16
        for i in range(visible_cells):
            idx = i + self.scroll_offset
            if idx >= len(self.cinta):
                break
            
            x = start_x + i * (cell_width + 5)
            
            # Color de la celda
            if idx == self.cabezal:
                color = COLORS['cell_active']
                border_width = 4
            else:
                color = COLORS['cell']
                border_width = 2
            
            # Dibujar celda
            pygame.draw.rect(self.screen, color, 
                           (x, start_y, cell_width, cell_height), 
                           border_radius=12)
            pygame.draw.rect(self.screen, COLORS['cell_border'], 
                           (x, start_y, cell_width, cell_height), 
                           border_width, border_radius=12)
            
            # Símbolo
            simbolo = self.cinta[idx] if self.cinta[idx] != ' ' else '□'
            texto = self.fuente_mono.render(simbolo, True, COLORS['text'])
            texto_rect = texto.get_rect(center=(x + cell_width//2, start_y + cell_height//2))
            self.screen.blit(texto, texto_rect)
            
            # Indicador de cabezal
            if idx == self.cabezal:
                pygame.draw.polygon(self.screen, COLORS['cell_active'], [
                    (x + cell_width//2 - 15, start_y + 110),
                    (x + cell_width//2 + 15, start_y + 110),
                    (x + cell_width//2, start_y +95)
                ])
    
    def dibujar_estado(self):
        """Dibuja el estado actual"""
        x = 100
        y = 100
        
        # Estado
        texto_label = self.fuente_mediana.render("ESTADO:", True, COLORS['text_dim'])
        self.screen.blit(texto_label, (x, y))
        
        color = COLORS['success'] if self.estado == self.estado_final else COLORS['primary']
        pygame.draw.rect(self.screen, color, (x + 150, y - 10, 120, 60), border_radius=12)
        
        texto_estado = self.fuente_grande.render(self.estado, True, COLORS['text'])
        texto_rect = texto_estado.get_rect(center=(x + 210, y + 20))
        self.screen.blit(texto_estado, texto_rect)
        
        # Pasos
        texto_pasos = self.fuente_mediana.render(f"Pasos: {self.pasos}", True, COLORS['text_dim'])
        self.screen.blit(texto_pasos, (x + 320, y + 5))
        
        # Estado final
        if self.estado == self.estado_final:
            texto_final = self.fuente_grande.render("✓ FINALIZADO", True, COLORS['success'])
            self.screen.blit(texto_final, (x + 520, y + 5))
    
    def dibujar_botones(self):
        """Dibuja los botones de control"""
        mouse_pos = pygame.mouse.get_pos()
        
        for boton in self.botones:
            # Color hover
            color = boton['color']
            if boton['rect'].collidepoint(mouse_pos):
                color = tuple(min(c + 30, 255) for c in color)
            
            # Botón ejecutar cambia de color
            if boton['accion'] == 'toggle_run' and self.ejecutando:
                color = COLORS['warning']
                boton['texto'] = 'PAUSAR'
                boton['icono'] = ''
            elif boton['accion'] == 'toggle_run':
                boton['texto'] = 'EJECUTAR'
                boton['icono'] = ''
            
            # Dibujar botón
            pygame.draw.rect(self.screen, color, boton['rect'], border_radius=12)
            
            # Texto
            if boton['icono']:
                texto_icono = self.fuente_grande.render(boton['icono'], True, COLORS['text'])
                self.screen.blit(texto_icono, (boton['rect'].x + 20, boton['rect'].y + 10))
                texto = self.fuente_pequena.render(boton['texto'], True, COLORS['text'])
                self.screen.blit(texto, (boton['rect'].x + 60, boton['rect'].y + 18))
            else:
                texto = self.fuente_grande.render(boton['texto'], True, COLORS['text'])
                texto_rect = texto.get_rect(center=boton['rect'].center)
                self.screen.blit(texto, texto_rect)
        
        # Velocidad
        texto_vel = self.fuente_pequena.render(f"Velocidad: {self.velocidad}ms", True, COLORS['text_dim'])
        self.screen.blit(texto_vel, (800, self.height - 130))
    
    def dibujar_transiciones(self):
        """Dibuja la tabla de transiciones"""
        x = 100
        y = 400
        
        titulo = self.fuente_mediana.render("TRANSICIONES", True, COLORS['text_dim'])
        self.screen.blit(titulo, (x, y))
        
        y += 50
        col_width = 150
        
        # Headers
        headers = ["Estado", "Símbolo", "→ Estado", "Escribir", "Mover"]
        for i, header in enumerate(headers):
            texto = self.fuente_pequena.render(header, True, COLORS['text_dim'])
            self.screen.blit(texto, (x + i * col_width, y))
        
        y += 40
        
        # Transiciones (primeras 8)
        count = 0
        for (estado, simbolo), (nuevo_estado, escribir, mover) in self.transiciones.items():
            if count >= 8:
                break
            
            # Highlight transición actual
            if estado == self.estado and simbolo == self.cinta[self.cabezal]:
                pygame.draw.rect(self.screen, COLORS['surface'], 
                               (x - 10, y - 5, 750, 35), border_radius=8)
            
            simbolo_display = '□' if simbolo == ' ' else simbolo
            escribir_display = '-' if escribir == 'n' else escribir
            
            datos = [estado, simbolo_display, nuevo_estado, escribir_display, mover]
            for i, dato in enumerate(datos):
                color = COLORS['primary'] if estado == self.estado else COLORS['text']
                texto = self.fuente_pequena.render(str(dato), True, color)
                self.screen.blit(texto, (x + i * col_width, y))
            
            y += 35
            count += 1
    
    def manejar_click(self, pos):
        """Maneja los clicks en botones"""
        for boton in self.botones:
            if boton['rect'].collidepoint(pos):
                if boton['accion'] == 'toggle_run':
                    self.ejecutando = not self.ejecutando
                elif boton['accion'] == 'step':
                    self.paso()
                elif boton['accion'] == 'reset':
                    self.reset()
                elif boton['accion'] == 'speed_up':
                    self.velocidad = max(100, self.velocidad - 100)
                elif boton['accion'] == 'speed_down':
                    self.velocidad = min(2000, self.velocidad + 100)
    
    def ejecutar(self):
        """Loop principal"""
        clock = pygame.time.Clock()
        running = True
        
        while running:
            current_time = pygame.time.get_ticks()
            
            # Eventos
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.manejar_click(event.pos)
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.ejecutando = not self.ejecutando
                    elif event.key == pygame.K_RIGHT:
                        self.paso()
                    elif event.key == pygame.K_r:
                        self.reset()
            
            # Ejecución automática
            if self.ejecutando and current_time - self.ultimo_paso > self.velocidad:
                self.paso()
                self.ultimo_paso = current_time
            
            # Dibujar
            self.screen.fill(COLORS['bg'])
            self.dibujar_estado()
            self.dibujar_cinta()
            self.dibujar_botones()
            #self.dibujar_transiciones()
            
            # Instrucciones
            texto_help = self.fuente_pequena.render("ESPACIO: Pausar | →: Paso | R: Reset", 
                                                     True, COLORS['text_dim'])
            self.screen.blit(texto_help, (self.width - 450, self.height - 50))
            
            pygame.display.flip()
            clock.tick(60)
        
        pygame.quit()
        sys.exit()


# Configuración de la máquina
transiciones_incrementador = {
    ('s0', '0'): ('s0', 'n', 'R'),
    ('s0', '1'): ('s0', 'n', 'R'),
    ('s0', ' '): ('s1', 'n', 'L'),
    ('s1', '0'): ('s2', '1', 'N'),
    ('s1', '1'): ('s3', '0', 'L'),
    ('s3', '0'): ('s1', 'n', 'N'),
    ('s3', '1'): ('s1', 'n', 'N'),
    ('s3', ' '): ('s2', '1', 'L'),
}

if __name__ == "__main__":
    # Crear y ejecutar el visualizador
    mt_visual = MaquinaTuringVisual("111 ", transiciones_incrementador, "s0", "s2")
    mt_visual.ejecutar()

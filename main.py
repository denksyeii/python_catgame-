import pygame
import sys
import random
import os

# --- Configuración Principal ---
N = 8
TAMANO_CELDA = 70
ANCHO_VENTANA = N * TAMANO_CELDA
ALTO_VENTANA = N * TAMANO_CELDA

# --- Colores Base ---
COLOR_FONDO = (250, 250, 250)
COLOR_LINEA = (90, 90, 90)

# --- generación procedural con solución ---
class GeneradorNivel:
    def __init__(self, n):
        self.n = n

    def generar_solucion_base(self):
        """Usa Backtracking para colocar N gatos válidos en secreto."""
        solucion = []

        def es_seguro(r, c):
            for gr, gc in solucion:
                if c == gc: return False # Misma columna
                # Verifica adyacencia (las 8 celdas alrededor)
                if abs(r - gr) <= 1 and abs(c - gc) <= 1: return False 
            return True

        def resolver_fila(r):
            if r == self.n:
                return True 
          
            columnas = list(range(self.n))
            random.shuffle(columnas)
            
            for c in columnas:
                if es_seguro(r, c):
                    solucion.append((r, c))
                    if resolver_fila(r + 1):
                        return True
                    solucion.pop() #por si se equivoca xd
            return False

        resolver_fila(0)
        return solucion

    def generar_regiones_desde_solucion(self, solucion):
        """Hace crecer las regiones de color usando la solución como semillas."""
        matriz_regiones = [[0 for _ in range(self.n)] for _ in range(self.n)]
        celdas_por_procesar = []
        
        for rid, (r, c) in enumerate(solucion, 1):
            matriz_regiones[r][c] = rid
            celdas_por_procesar.append((r, c, rid))
            
        random.shuffle(celdas_por_procesar)

        while celdas_por_procesar:
            idx = random.randint(0, len(celdas_por_procesar) - 1)
            r, c, region_id = celdas_por_procesar.pop(idx)
            
            for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nr, nc = r + dr, c + dc
                if 0 <= nr < self.n and 0 <= nc < self.n and matriz_regiones[nr][nc] == 0:
                    matriz_regiones[nr][nc] = region_id
                    celdas_por_procesar.append((nr, nc, region_id))
        return matriz_regiones

    def obtener_paleta_colores(self):
        paleta = []
        salto_contraste = 3 
        for i in range(self.n):
            hue = ((i * salto_contraste) / self.n * 360) % 360
            color = pygame.Color(0)
            color.hsla = (hue, 100, 75, 100)
            paleta.append((color.r, color.g, color.b))
        return paleta
    
# --- motor de logica matematica ---
class Validador:
    def __init__(self, n, mapa_regiones):
        self.n = n
        self.mapa_regiones = mapa_regiones

    def comprobar_reglas(self, tablero):
        gatos = []
        for f in range(self.n):
            for c in range(self.n):
                if tablero[f][c] == 1:
                    gatos.append((f, c))

        gatos_con_error = set()

        # reglas 1 y 2: Filas y Columnas
        conteo_filas = [0] * self.n
        conteo_cols = [0] * self.n
        for f, c in gatos:
            conteo_filas[f] += 1
            conteo_cols[c] += 1
            
        for f, c in gatos:
            if conteo_filas[f] > 1 or conteo_cols[c] > 1:
                gatos_con_error.add((f, c))

        # regla 3: color
        conteo_regiones = {}
        for f, c in gatos:
            region_id = self.mapa_regiones[f][c]
            conteo_regiones[region_id] = conteo_regiones.get(region_id, 0) + 1
            
        for f, c in gatos:
            region_id = self.mapa_regiones[f][c]
            if conteo_regiones[region_id] > 1:
                gatos_con_error.add((f, c))

        # rwgla 4: adyacencia (gatos no pueden tocarse)
        for f, c in gatos:
            for df in [-1, 0, 1]:
                for dc in [-1, 0, 1]:
                    if df == 0 and dc == 0:
                        continue 
                    
                    nf, nc = f + df, c + dc
                    if 0 <= nf < self.n and 0 <= nc < self.n:
                        if tablero[nf][nc] == 1:
                            gatos_con_error.add((f, c))
                            gatos_con_error.add((nf, nc))

        return gatos_con_error

# --- Inicialización del Nivel ---
generador = GeneradorNivel(N)

solucion_oculta = generador.generar_solucion_base()

mapa_regiones = generador.generar_regiones_desde_solucion(solucion_oculta)

paleta_regiones = generador.obtener_paleta_colores()

validador = Validador(N, mapa_regiones)
tablero = [[0 for _ in range(N)] for _ in range(N)]

# --- Función de Dibujo ---
def dibujar_cuadricula(pantalla, sprite_gato, sprite_gato_error, sprite_cruz, gatos_erroneos): # Añadido sprite_cruz
    pantalla.fill(COLOR_FONDO)
    
    # Capa Inferior: Colores (Se mantiene igual)
    for fila in range(N):
        for col in range(N):
            region_id = mapa_regiones[fila][col]
            color = paleta_regiones[region_id - 1]
            pygame.draw.rect(pantalla, color, (col * TAMANO_CELDA, fila * TAMANO_CELDA, TAMANO_CELDA, TAMANO_CELDA))

    # Capa Media: Gatos y Cruces
    for fila in range(N):
        for col in range(N):
            pos_x_base = col * TAMANO_CELDA
            pos_y_base = fila * TAMANO_CELDA
            
            if tablero[fila][col] == 1:
                
                if (fila, col) in gatos_erroneos:
                    pantalla.blit(sprite_gato_error, (pos_x_base + 5, pos_y_base + 5))
                else:
                    pantalla.blit(sprite_gato, (pos_x_base + 5, pos_y_base + 5))
            elif tablero[fila][col] == 2:
                
                pantalla.blit(sprite_cruz, (pos_x_base + 5, pos_y_base + 5))

    for x in range(0, ANCHO_VENTANA, TAMANO_CELDA):
        pygame.draw.line(pantalla, COLOR_LINEA, (x, 0), (x, ALTO_VENTANA), 2)
    for y in range(0, ALTO_VENTANA, TAMANO_CELDA):
        pygame.draw.line(pantalla, COLOR_LINEA, (0, y), (ANCHO_VENTANA, y), 2)


# --- Bucle Principal ---
def main():
    pygame.init()
    pygame.font.init() # NUEVO: Iniciar el motor de fuentes
    fuente_victoria = pygame.font.SysFont("Arial", 50, bold=True)
    reloj = pygame.time.Clock()
    FPS = 60
    pantalla = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))
    pygame.display.set_caption("juego gatos")

    gatos_erroneos = set()

    # --- carga de sprites ---
    ruta_base = os.path.dirname(os.path.abspath(__file__))
    ruta_gato = os.path.join(ruta_base, "gato_normal.png")
    ruta_error = os.path.join(ruta_base, "gato_error.png")
    ruta_cruz = os.path.join(ruta_base, "equis.png")

    if os.path.exists(ruta_gato):
        sprite_gato_bruto = pygame.image.load(ruta_gato).convert_alpha()
        sprite_gato = pygame.transform.smoothscale(sprite_gato_bruto, (TAMANO_CELDA - 10, TAMANO_CELDA - 10))
    else:
        sprite_gato = pygame.Surface((TAMANO_CELDA - 10, TAMANO_CELDA - 10))
        sprite_gato.fill((0, 0, 0))
        print(f"Aviso: 'gato_normal.png' no encontrado en {ruta_base}")

    if os.path.exists(ruta_error):
        sprite_error_bruto = pygame.image.load(ruta_error).convert_alpha()
        sprite_gato_error = pygame.transform.smoothscale(sprite_error_bruto, (TAMANO_CELDA - 10, TAMANO_CELDA - 10))
    else:
        sprite_gato_error = pygame.Surface((TAMANO_CELDA - 10, TAMANO_CELDA - 10))
        sprite_gato_error.fill((255, 0, 0))
        print(f"Aviso: 'gato_error.png' no encontrado en {ruta_base}")
    if os.path.exists(ruta_cruz):
        sprite_cruz_bruto = pygame.image.load(ruta_cruz).convert_alpha()
        sprite_cruz = pygame.transform.smoothscale(sprite_cruz_bruto, (TAMANO_CELDA - 10, TAMANO_CELDA - 10))
    else:
        sprite_cruz = pygame.Surface((TAMANO_CELDA - 10, TAMANO_CELDA - 10))
        sprite_cruz.fill((100, 100, 100)) # Gris oscuro temporal si falla
        print(f"Aviso: 'equis.png' no encontrado en {ruta_base}")
    # ---------------------------------
    tiempo_inicio_clic = 0
    celda_presionada = None
    ejecutando = True
    while ejecutando:
        reloj.tick(FPS)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                ejecutando = False
            
            #baja el dedo
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if evento.button == 1: # Clic izquierdo / Toque en pantalla
                    tiempo_inicio_clic = pygame.time.get_ticks()
                    x, y = pygame.mouse.get_pos()
                    celda_presionada = (y // TAMANO_CELDA, x // TAMANO_CELDA)

            #levanta el dedo
            elif evento.type == pygame.MOUSEBUTTONUP:
                if evento.button == 1 and celda_presionada is not None:
                    x, y = pygame.mouse.get_pos()
                    fila_actual = y // TAMANO_CELDA
                    col_actual = x // TAMANO_CELDA
                    
                    if (fila_actual, col_actual) == celda_presionada:
                        fila, col = fila_actual, col_actual
                        # toque corto
                        if tablero[fila][col] != 2:
                            tablero[fila][col] = 2
                        else:
                            tablero[fila][col] = 0
                        
                        gatos_erroneos = validador.comprobar_reglas(tablero)
                    
                    celda_presionada = None # Reseteamos la celda

        if celda_presionada is not None:
            tiempo_actual = pygame.time.get_ticks()
            # logica de mantener presionado
            if (tiempo_actual - tiempo_inicio_clic) >= 300:
                fila, col = celda_presionada
                
                # TOQUE LARGO: pone el gatp 
                if tablero[fila][col] != 1:
                    tablero[fila][col] = 1
                else:
                    tablero[fila][col] = 0
                
                gatos_erroneos = validador.comprobar_reglas(tablero)
                
                celda_presionada = None 
        total_gatos = sum(fila.count(1) for fila in tablero)
        
        if total_gatos == N and len(gatos_erroneos) == 0:
            juego_ganado = True
        else:
            juego_ganado = False

        dibujar_cuadricula(pantalla, sprite_gato, sprite_gato_error, sprite_cruz, gatos_erroneos)

        # pantalla d victoria
        if juego_ganado:
            # fondo negropara oscurecer el tablero
            fondo_oscuro = pygame.Surface((ANCHO_VENTANA, ALTO_VENTANA))
            fondo_oscuro.set_alpha(160) # Nivel de transparencia (0 a 255)
            fondo_oscuro.fill((0, 0, 0))
            pantalla.blit(fondo_oscuro, (0, 0))
            
            #texto 
            texto = fuente_victoria.render("¡NIVEL COMPLETADO!", True, (255, 215, 0))
            rect_texto = texto.get_rect(center=(ANCHO_VENTANA // 2, ALTO_VENTANA // 2))
            
            #fondo negro para el texto
            pygame.draw.rect(pantalla, (20, 20, 20), rect_texto.inflate(40, 40), border_radius=10)
            pygame.draw.rect(pantalla, (255, 215, 0), rect_texto.inflate(40, 40), 3, border_radius=10)
            
            pantalla.blit(texto, rect_texto)

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
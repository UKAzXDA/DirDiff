import math
import os
from PIL import Image

def gerar_tabela_cores():
    """
    Gera uma tabela de consulta (LUT) com 256 cores correspondentes
    à transição do Frio Absoluto (Blue) ao Quente Absoluto (Red).
    """
    lut = []
    for val in range(256):
        if val < 51:       # 1. Azul Puro para Ciano
            r = 0
            g = int((val / 51) * 255)
            b = 255
        elif val < 102:    # 2. Ciano para Verde
            r = 0
            g = 255
            b = int(255 - ((val - 51) / 51) * 255)
        elif val < 153:    # 3. Verde para Amarelo
            r = int(((val - 102) / 51) * 255)
            g = 255
            b = 0
        elif val < 204:    # 4. Amarelo para Laranja
            r = 255
            g = int(255 - ((val - 153) / 51) * 128)
            b = 0
        else:              # 5. Laranja para Vermelho Puro
            r = 255
            g = int(127 - ((val - 204) / 51) * 127)
            b = 0
        lut.append((r, g, b))
    return lut

def transformar_arquivo_em_pixel(caminho_arquivo, caminho_saida, largura_imagem=512):
    """
    Lê um arquivo binário, mapeia seus bytes na escala térmica e gera uma imagem.
    """
    if not os.path.exists(caminho_arquivo):
        print(f"Erro: O arquivo '{caminho_arquivo}' não foi encontrado.")
        return

    # 1. Ler todos os bytes do arquivo
    with open(caminho_arquivo, "rb") as f:
        dados_binarios = f.read()

    total_bytes = len(dados_binarios)
    if total_bytes == 0:
        print("Erro: O arquivo está vazio.")
        return

    print(f"Lendo {total_bytes} bytes do arquivo...")

    # 2. Calcular a altura da imagem com base na largura fixa
    altura_imagem = math.ceil(total_bytes / largura_imagem)
    total_pixels_necessarios = largura_imagem * altura_imagem

    # 3. Gerar a paleta térmica de 0 a 255
    tabela_cores = gerar_tabela_cores()

    # 4. Mapear cada byte para sua respectiva cor RGB
    pixels_rgb = [tabela_cores[byte] for byte in dados_binarios]

    # Preencher o resto da última linha com preto (0,0,0) se o arquivo acabar antes
    if len(pixels_rgb) < total_pixels_necessarios:
        pixels_rgb += [(0, 0, 0)] * (total_pixels_necessarios - len(pixels_rgb))

    # 5. Criar a imagem usando a biblioteca Pillow
    img = Image.new("RGB", (largura_imagem, altura_imagem))
    img.putdata(pixels_rgb)

    # 6. Salvar no formato desejado (.png ou .jpg)
    img.save(caminho_saida)
    print(f"Sucesso! Imagem gerada com dimensões {largura_imagem}x{altura_imagem} em: {caminho_saida}")

# --- CONFIGURAÇÃO DE USO ---
if __name__ == "__main__":
    # Altere para o arquivo que você quer analisar (pode ser um .bin, .img, .exe, etc)
    arquivo_alvo = "recovery.img" 
    
    # Nome do arquivo de saída (use .png para manter a nitidez perfeita de cada pixel)
    arquivo_resultado = "mapa_termico_recovery.png" 
    
    # Largura da imagem. 512 ou 1024 são ótimos para ver padrões de alinhamento de código
    largura = 512 

    transformar_arquivo_em_pixel(arquivo_alvo, arquivo_resultado, largura)

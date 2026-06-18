import math
import os
from PIL import Image

def gerar_tabela_cores():
    """Gera uma tabela de consulta (LUT) com 256 cores (Frio ao Quente)."""
    lut = []
    for val in range(256):
        if val < 51:
            r, g, b = 0, int((val / 51) * 255), 255
        elif val < 102:
            r, g, b = 0, 255, int(255 - ((val - 51) / 51) * 255)
        elif val < 153:
            r, g, b = int(((val - 102) / 51) * 255), 255, 0
        elif val < 204:
            r, g, b = 255, int(255 - ((val - 153) / 51) * 128), 0
        else:
            r, g, b = 255, int(127 - ((val - 204) / 51) * 127), 0
        lut.append((r, g, b))
    return lut

def transformar_arquivo_em_quadrado(caminho_arquivo, caminho_saida):
    """Lê um arquivo binário e gera uma imagem estritamente quadrada."""
    if not os.path.exists(caminho_arquivo):
        print(f"Erro: O arquivo '{caminho_arquivo}' não foi encontrado.")
        return

    with open(caminho_arquivo, "rb") as f:
        dados_binarios = f.read()

    total_bytes = len(dados_binarios)
    if total_bytes == 0:
        print("Erro: O arquivo está vazio.")
        return

    print(f"Lendo {total_bytes} bytes do arquivo...")

    # --- O SEGREDO DO QUADRADO ESTÁ AQUI ---
    # Calcula a raiz quadrada dos bytes e arredonda para cima
    largura_imagem = math.ceil(math.sqrt(total_bytes))
    altura_imagem = math.ceil(total_bytes / largura_imagem)
    
    total_pixels_necessarios = largura_imagem * altura_imagem

    # Mapear bytes para RGB
    tabela_cores = gerar_tabela_cores()
    pixels_rgb = [tabela_cores[byte] for byte in dados_binarios]

    # Preencher o restante da última linha para fechar o quadrado perfeito
    if len(pixels_rgb) < total_pixels_necessarios:
        pixels_rgb += [(0, 0, 0)] * (total_pixels_necessarios - len(pixels_rgb))

    # Criar e salvar a imagem
    img = Image.new("RGB", (largura_imagem, altura_imagem))
    img.putdata(pixels_rgb)
    img.save(caminho_saida)
    
    print(f"Sucesso! Imagem quadrada gerada: {largura_imagem}x{altura_imagem} em: {caminho_saida}")

# --- CONFIGURAÇÃO DE USO ---
if __name__ == "__main__":
    arquivo_alvo = "recovery.img" 
    arquivo_resultado = "mapa_termico_quadrado.png" 

    transformar_arquivo_em_quadrado(arquivo_alvo, arquivo_resultado)

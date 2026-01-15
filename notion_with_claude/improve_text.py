#!/usr/bin/env python3
import sys
import subprocess
import tempfile
import os

def call_claude(text):
    """
    Chama Claude Code para melhorar o texto
    """
    # Cria arquivo temporário com o texto
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
        f.write(text)
        temp_file = f.name
    
    try:
        # Chama claude code com instrução para melhorar o texto
        cmd = [
            'claude', 
            '--message', 
            f'Melhore este texto sem alterar dados, apenas formatação, gramática e organização:\n\n{text}'
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            return result.stdout.strip()
        else:
            print(f"Erro ao chamar Claude: {result.stderr}")
            return text
            
    except FileNotFoundError:
        print("Erro: Claude Code não encontrado. Certifique-se de que está instalado.")
        return text
    except Exception as e:
        print(f"Erro: {e}")
        return text
    finally:
        # Remove arquivo temporário
        if os.path.exists(temp_file):
            os.unlink(temp_file)

def copy_to_clipboard(text):
    """
    Copia o texto para o clipboard
    """
    try:
        # Tenta usar xclip (Linux)
        subprocess.run(['xclip', '-selection', 'clipboard'], 
                      input=text.encode(), check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        try:
            # Tenta usar pbcopy (macOS)
            subprocess.run(['pbcopy'], input=text.encode(), check=True)
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            return False

def main():
    if len(sys.argv) < 2:
        print("Uso: python improve_text.py 'improve: seu texto aqui'")
        sys.exit(1)
    
    input_text = ' '.join(sys.argv[1:])
    
    # Verifica se começa com "improve:"
    if not input_text.lower().startswith('improve:'):
        print("Erro: O texto deve começar com 'improve:'")
        sys.exit(1)
    
    # Remove o "improve:" e processa o texto
    text_to_improve = input_text[8:].strip()
    
    if not text_to_improve:
        print("Erro: Nenhum texto fornecido após 'improve:'")
        sys.exit(1)
    
    improved_text = call_claude(text_to_improve)
    
    print("Texto original:")
    print(f"'{text_to_improve}'")
    print("\nTexto melhorado:")
    print(f"'{improved_text}'")
    
    # Copia para clipboard
    if copy_to_clipboard(improved_text):
        print("\n✅ Texto copiado para o clipboard!")
    else:
        print("\n⚠️  Não foi possível copiar para o clipboard (instale xclip no Linux)")
    
    return improved_text

if __name__ == "__main__":
    main()
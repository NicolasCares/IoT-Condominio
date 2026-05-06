# Sistema de Gerenciamento IoT (Projeto Integrador)

Este projeto consiste em um sistema de gerenciamento de dispositivos IoT utilizando **Flask**, **Docker** e a biblioteca **TinyTuya**.

## 🚀 Como configurar o ambiente

Para manter a segurança do projeto, arquivos de credenciais e configurações locais não são enviados para o repositório. Siga os passos abaixo para rodar o projeto:

### 1. Variáveis de Ambiente
Crie um arquivo chamado `.env` na raiz do projeto e adicione as seguintes chaves:
- `TUYA_API_KEY`: Sua chave de API do portal Tuya.
- `TUYA_SECRET`: Seu Secret da API Tuya.
- `DEVICE_ID`: ID do dispositivo para teste.

### 2. Arquivos JSON de Dispositivos
O sistema utiliza os arquivos `snapshot.json` e `tinytuya.json` para o mapeamento dos dispositivos. Eles são gerados automaticamente ao executar o script de scan ou devem ser configurados manualmente conforme o padrão da biblioteca TinyTuya.

## 🛠️ Tecnologias Utilizadas
- **Linguagem:** Python
- **Framework Web:** Flask
- **Containerização:** Docker
- **Integração IoT:** TinyTuya Cloud API

## 📋 Como Executar
```bash
# Para rodar com Docker
docker-compose up --build
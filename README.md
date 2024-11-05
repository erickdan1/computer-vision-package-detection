# Protótipo Hackathon Correios - Campus Party 2024

Este repositório apresenta parte do protótipo desenvolvido para o **Hackathon dos Correios** na **Campus Party de 2024**. O projeto utiliza visão computacional com **Python** e modelos de IA da **Roboflow** para agilizar e otimizar o processo de envio de pacotes, abordando questões de insatisfação dos clientes, impacto na imagem da empresa, tempo de atendimento e falta de ferramentas eficientes.

## Problema

Identificamos as seguintes dores no processo atual de atendimento dos Correios:
- **Insatisfação dos clientes** devido à demora e complexidade.
- **Impacto negativo na imagem** da empresa por conta do tempo de espera.
- **Tempo elevado de atendimento** nas agências.
- **Falta de ferramentas eficientes** para facilitar o processo de envio.

## Solução

Nossa solução integra visão computacional e automação para otimizar o processo de pré-atendimento e atendimento nas agências dos Correios. Com essa tecnologia, oferecemos:
- **Redução do tempo de espera:** o usuário realiza grande parte do processo em casa ou no totem, economizando tempo nas agências.
- **Precisão e eficiência:** as dimensões do pacote são capturadas automaticamente e o cálculo dos custos é feito com precisão.
- **Agilidade no atendimento:** a integração com os sistemas internos dos Correios agiliza o fluxo de trabalho.

### Funcionalidades da Solução Proposta

1. **Abertura do Aplicativo:**
   - O usuário abre o aplicativo e escolhe a opção de pré-atendimento.
   
2. **Preenchimento das Informações:**
   - Dados como remetente, destinatário e descrição do pacote são inseridos.

3. **Captura Automática das Dimensões:**
   - O usuário utiliza a câmera para capturar as dimensões do pacote, processadas pela IA para cálculo preciso.

4. **Estipulação do Peso do Pacote:**
   - Baseado nas dimensões e tipo de material, a solução estima o peso do pacote automaticamente.

5. **Cálculo dos Custos de Envio:**
   - O aplicativo calcula o custo considerando dimensões, peso estimado, tipo de serviço e destino.

6. **Geração de Etiqueta e Código QR:**
   - Uma etiqueta e um código QR são gerados com todos os dados para facilitar o atendimento na agência.

7. **Apresentação na Agência:**
   - O usuário apresenta o código QR, agilizando o processo de verificação e finalização do envio.

### Fluxo do Atendimento

1. **Recepção e Escaneamento do Código QR:**
   - O atendente escaneia o QR code do usuário, que carrega automaticamente os dados no sistema dos Correios.

2. **Verificação e Pagamento:**
   - O atendente confirma as dimensões e processa o pagamento (caso não tenha sido feito no aplicativo).

3. **Aplicação da Etiqueta e Finalização:**
   - A etiqueta é aplicada ao pacote, e o envio é finalizado no sistema dos Correios.

## Tecnologias Utilizadas

- **Python** para o desenvolvimento do backend.
- **Roboflow** para modelagem de visão computacional.
- **OpenCV** e bibliotecas auxiliares para processamento de imagens.

## Como Executar

1. **Instale as dependências**

2. **Configure o acesso ao modelo Roboflow:**
   - Configure as chaves de API do Roboflow para integrar os modelos de visão computacional.

3. **Execute o aplicativo:**
   ```bash
   python app.py
   ```

## Demonstração:

[![Video](https://img.youtube.com/vi/RTB9IlHWQEU/maxresdefault.jpg)](https://www.youtube.com/watch?v=RTB9IlHWQEU)

**Nota:** Este é um protótipo desenvolvido para fins de demonstração no hackathon.

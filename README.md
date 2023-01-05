# Sistema de Câmeras de Segurança com Detecção de Objetos

O objetivo deste projeto é detectar movimentos suspeitos em imagens de câmeras de segurança usando detecção de objetos para prevenir possíveis invasões em casas e estabelecimentos.

O sistema para Windows permite que sejam criados gatilhos desenhando áreas na imagem em que detecções serão analisadas, assim como configurar por quanto tempo uma detecção poderá permanecer nesta área e em quais horários. Se as condições de um gatilho forem satisfeitas, uma notificação ou alarme é enviado para um smartphone. Este sistema também age como servidor para o aplicativo Android.

A partir do aplicativo Android, é possível receber as notificações e visualizar as imagens das câmeras via rede local.

## Screenshots

### Principal
<img src="./sreenshots/Interface_Principal.png">

### Gerenciamento de Gatilhos
<img src="./sreenshots/Interface_Gerenciamento_Gatilhos.png">

### Adicionar Gatilhos
<img src="./sreenshots/Interface_Adicionar_Gatilho.png">

### Interface Android
<img src="./sreenshots/Interfaces_Android.png">

## Tecnologias Utilizadas

| Nome                        | Uso                       |
| --------------------------- | ------------------------- |
| [**PyQt5**](https://www.riverbankcomputing.com/software/pyqt/) | Interface para Windows |
| [**OpenCV**](https://opencv.org/) | Manipulação de Imagens e Aplicação da Rede Neural |
| [**Flutter**](https://flutter.dev/) | Interface para Android |
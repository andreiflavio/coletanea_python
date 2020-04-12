Montar ambiente virtual python e instalar via pip install -r requiments.txt as dependências necessárias.

No arquivo web_scraping.py fazer as seguintes mudanças:

> Alterar linha 20: base_path = "downloads/magi/" para o nome de pasta desejado para salvar arquivos baixados durante download.

> Alterar linha 28 url_manga = "https://unionleitor.top/leitor/Magi:_The_Labyrinth_of_Magic"
para indicar o mangá desejado. Esta url deve ser buscada no site unionleitor,
acessando um capítulo do mangá desejado e copiando a url sem o número do capítulo.

> Alterar linha 29(chapter_start = 220) e 30 (chapter_end = 370) para indicar o capítulo inicial e final para download.

> Alterar linha 31 (generate_pdf_after_downloads = True) para False, caso não deseje a geração do capítulo do mangá em pdf.

No cmd, com virtualenv ativado, executar o comando python web_scrapping.py para efetuar download.
Ao final do processo os arquivos baixados e o pdf gerado estarão disponíveis na pasta indicada em base_path (linha 20).



def get_clean_text(texto):
    return texto.replace('\n','').replace('\t','').replace('.','').replace(',','.').replace('$','')
